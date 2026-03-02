# Database Metadata Patterns

Design and implement database metadata storage patterns including connection management, scoped CRUD operations, batch operations, flexible schemas, index strategies, and initialization scripts.

## Trigger

- The user asks to "set up database metadata", "design a database schema", "implement database operations", or similar
- The user needs connection pooling, CRUD helpers, batch writes, or index strategy advice
- The user is setting up MongoDB (or similar document store) for a new service

## Procedure

### Phase 1 — Requirements Gathering

Ask the user for:

1. **Database engine**: MongoDB (default), PostgreSQL, or other
2. **Collections/tables needed**: What entities are stored?
3. **Partition key**: What field scopes most queries? (e.g., `run_id`, `tenant_id`, `project_id`)
4. **Access patterns**: What queries will be most common?
5. **Auth requirements**: Dedicated user with limited privileges? Auth source?

### Phase 2 — Connection Factory

Always use connection pooling and set reasonable timeouts:

```python
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def connect_db(db_uri: str = None, timeout_ms: int = 5000) -> MongoClient:
    """Create a MongoDB client with connection pooling and health check."""
    if db_uri is None:
        db_uri = os.environ["DB_URI"]

    client = MongoClient(
        db_uri,
        serverSelectionTimeoutMS=timeout_ms,
        connectTimeoutMS=timeout_ms,
        socketTimeoutMS=30000,
        maxPoolSize=10,
    )

    # Verify connection at startup — fail fast
    try:
        client.admin.command("ping")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        raise RuntimeError(f"Cannot connect to database: {e}")

    return client
```

**Connection string notes:**
- Include `?authSource={db_name}` if the user is created on a specific database (not admin)
- Never hardcode the URI — always read from environment variables
- The connection string format: `mongodb://{user}:{pass}@{host}:{port}/{db}?authSource={db}`

### Phase 3 — Scoped CRUD Operations

All queries should be scoped to a partition key (e.g., `run_id`, `tenant_id`). This ensures data isolation and index efficiency.

#### Read (scoped query)

```python
def load_metadata(client, db_name: str, collection: str, partition_key: str, partition_value: str, extra_query: dict = None):
    """Load documents scoped to a partition key."""
    db = client[db_name]
    query = {partition_key: partition_value}
    if extra_query:
        query.update(extra_query)
    return list(db[collection].find(query))
```

#### Write (single document)

```python
from datetime import datetime, timezone

def save_metadata(client, db_name: str, collection: str, partition_key: str, partition_value: str, source_name: str, doc: dict) -> str:
    """Insert a document with required fields."""
    db = client[db_name]
    record = {
        partition_key: partition_value,
        "source": source_name,
        "created_at": datetime.now(timezone.utc),
        **doc,
    }
    result = db[collection].insert_one(record)
    return str(result.inserted_id)
```

#### Update (scoped)

```python
def update_record(client, db_name: str, collection: str, query: dict, update_fields: dict, upsert: bool = False):
    """Update a document with automatic updated_at timestamp."""
    db = client[db_name]
    db[collection].update_one(
        query,
        {"$set": {**update_fields, "updated_at": datetime.now(timezone.utc)}},
        upsert=upsert,
    )
```

#### Batch Write

```python
def save_metadata_batch(client, db_name: str, collection: str, partition_key: str, partition_value: str, source_name: str, docs: list[dict]) -> list[str]:
    """Insert multiple documents with required fields."""
    if not docs:
        return []

    db = client[db_name]
    now = datetime.now(timezone.utc)
    records = [
        {
            partition_key: partition_value,
            "source": source_name,
            "created_at": now,
            **doc,
        }
        for doc in docs
    ]
    result = db[collection].insert_many(records)
    return [str(id) for id in result.inserted_ids]
```

### Phase 4 — Schema Design

Use a flexible schema with required fields. Every document must have:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `{partition_key}` | string | Yes | Scoping/isolation field |
| `source` | string | Yes | Which service/step wrote this |
| `created_at` | datetime (UTC) | Yes | When the document was created |
| `updated_at` | datetime (UTC) | On update | When last modified |

Additional fields are flexible — services can add any fields they need. Store structured data as nested documents:

```json
{
  "run_id": "run-001",
  "source": "image_processor",
  "created_at": "2024-01-15T10:30:00Z",
  "labels": {"category": "scan", "quality": "high"},
  "annotations": [{"type": "bbox", "coords": [10, 20, 100, 200]}],
  "custom": {"model_version": "2.1.0"}
}
```

**Schema rules:**
- Use `datetime.now(timezone.utc)` for all timestamps (never naive datetimes)
- Store file references (paths/URIs) rather than file contents
- Large arrays (thousands of items) should be separate documents with references
- Always query by partition key first — it's the primary access pattern

### Phase 5 — Index Strategy

Design indexes based on access patterns. Generate an initialization script:

```javascript
// infrastructure/mongodb/init.js
db = db.getSiblingDB("{db_name}");

// Create application user with limited privileges
db.createUser({
  user: "{app_user}",
  pwd: "{app_password}",
  roles: [{ role: "readWrite", db: "{db_name}" }]
});

// Create collections
db.createCollection("{collection_1}");
db.createCollection("{collection_2}");
db.createCollection("{metadata_collection}");

// Indexes for {collection_1}
db.{collection_1}.createIndex({ "{primary_id}": 1 }, { unique: true });
db.{collection_1}.createIndex({ "status": 1 });
db.{collection_1}.createIndex({ "created_at": 1 });

// Indexes for {collection_2} (compound unique)
db.{collection_2}.createIndex(
  { "{partition_key}": 1, "{secondary_key}": 1 },
  { unique: true }
);
db.{collection_2}.createIndex({ "status": 1 });

// Indexes for metadata (compound, non-unique)
db.{metadata_collection}.createIndex({ "{partition_key}": 1, "source": 1 });
db.{metadata_collection}.createIndex({ "{partition_key}": 1, "data_type": 1 });

print("Database initialized successfully");
```

**Index guidelines:**
- Every collection needs at least a primary key index (unique)
- Add compound indexes for the most common query patterns
- The partition key should always be the first field in compound indexes
- Avoid over-indexing — each index adds write overhead
- Use `unique: true` only for fields that must be globally unique

### Phase 6 — Docker Compose Integration

Add the database to `docker-compose.yml`:

```yaml
services:
  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: rootpass
      MONGO_INITDB_DATABASE: {db_name}
    volumes:
      - ./infrastructure/mongodb/init.js:/docker-entrypoint-initdb.d/init.js:ro
      - mongo_data:/data/db

volumes:
  mongo_data:
```

## Output

Report to the user:

```
Database metadata setup:
  Engine: {mongodb|postgres}
  Database: {db_name}
  Collections: {count} ({list})
  Indexes: {count}
  Files generated:
    - infrastructure/mongodb/init.js (or equivalent)
    - src/metadata.py (CRUD helpers)
    - src/models.py (Pydantic models)
    - docker-compose.yml (updated)
```
