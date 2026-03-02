# Team Workflows

Detailed guide to multi-agent composition chains using the riRoUtils dev support team.

## Overview

The dev support team consists of 5 specialized agents that can be composed into workflows. Each agent has a focused role, specific tools, and references particular skills. The main agent (or user) orchestrates these workflows by dispatching to the right agent at the right time.

For the team roster and dispatch rules, see `.claude/team.md`.

## Workflow 1: Build & Document

**Scenario:** Starting a new project or adding a significant component, then capturing everything as documentation.

```
project-architect → (implement) → documentarian → conversation-to-memory
```

### Steps

1. **Dispatch to project-architect**
   - Provide: project name, tech stack, infrastructure needs
   - Agent scaffolds the project structure, sets up GitHub isolation, creates microservice skeletons
   - Output: complete project directory with AGENT.md, README, Dockerfile, config files

2. **Implement features** (user or main agent)
   - Write the actual business logic, tests, infrastructure config
   - This is the "build" phase that happens between scaffolding and documentation

3. **Dispatch to documentarian**
   - Agent scans the full conversation and codebase
   - Generates: `docs/architecture-diagrams.md` (Mermaid diagrams), component catalog, relationship maps
   - Uses `post-implementation-docs` skill

4. **Dispatch to documentarian** (conversation-to-memory)
   - Agent extracts stable patterns, decisions, and preferences
   - Persists to memory files (MEMORY.md, architecture.md, patterns.md, etc.)
   - Uses `conversation-to-memory` skill

### Example

```
User: "Set up a new data processing project with Python, RabbitMQ, and MongoDB"

→ project-architect: scaffolds project, creates docker-compose.yml, sets up GitHub isolation
→ (user implements processing logic, tests, message handlers)
→ documentarian: generates architecture diagrams, documents components
→ documentarian: extracts learnings to memory files
```

## Workflow 2: Debug & Fix

**Scenario:** Something is broken. Investigate, fix, review, and document.

```
debugger → (fix) → code-reviewer → documentarian
```

### Steps

1. **Dispatch to debugger**
   - Provide: error description, affected component, logs if available
   - Agent follows 5-phase RCA methodology: explore → collect evidence → correlate → root cause → propose fix
   - Output: RCA report with fix options ranked by risk/effort

2. **Implement the fix** (user or main agent)
   - Choose from the debugger's proposed options
   - Implement the code changes

3. **Dispatch to code-reviewer**
   - Agent reviews the fix against project conventions
   - Produces PASS/FAIL checklist with specific code references
   - Flags any convention violations introduced by the fix

4. **Dispatch to documentarian** (optional)
   - For significant incidents, generate a formal RCA document
   - Persist learnings about the failure mode to memory

### Example

```
User: "The image processor is failing with a timeout on large files"

→ debugger: investigates, finds unbounded memory allocation, recommends streaming
→ (user implements streaming fix)
→ code-reviewer: reviews fix — PASS on all sections except logging (missing duration metric)
→ (user adds duration metric)
→ documentarian: creates docs/rca/RCA-2024-01-15-image-processor-timeout.md
```

## Workflow 3: Infrastructure Setup

**Scenario:** Designing and implementing infrastructure components (MQ, DB, pipelines).

```
infra-engineer → project-architect → code-reviewer
```

### Steps

1. **Dispatch to infra-engineer**
   - Provide: what infrastructure is needed and the access patterns
   - Agent designs: MQ topology (exchanges, queues, bindings), DB schema (collections, indexes), or pipeline DAG
   - Output: `definitions.json`, `init.js`, pipeline JSON, docker-compose additions

2. **Dispatch to project-architect**
   - Agent scaffolds the service(s) that use the infrastructure
   - Generates: project structure with correct connection patterns, config, and helpers

3. **Dispatch to code-reviewer**
   - Agent reviews the scaffolded service for convention compliance
   - Ensures infrastructure patterns (connection pooling, publisher confirms, scoped queries) are correct

### Example

```
User: "I need a RabbitMQ topology for an order processing system with events and commands"

→ infra-engineer: designs 4 exchanges (orders.events, orders.commands + DLX for each),
  8 queues, 8 bindings, generates definitions.json
→ project-architect: scaffolds order-processor service with pika connection, publisher, consumer
→ code-reviewer: verifies publisher confirms, DLX routing, message envelope compliance
```

## Workflow 4: Full Project Bootstrap

**Scenario:** Creating a complete project from scratch with infrastructure, services, and documentation.

```
project-architect → infra-engineer → project-architect → documentarian
```

### Steps

1. **project-architect** — creates the project skeleton, AGENT.md, README, GitHub isolation
2. **infra-engineer** — designs the infrastructure layer (MQ, DB, pipeline if needed)
3. **project-architect** — scaffolds microservices that use the infrastructure
4. **documentarian** — generates initial architecture diagrams and project documentation

### Example

```
User: "Bootstrap a complete ML pipeline project with ingestion, preprocessing, inference, and export"

→ project-architect: creates project structure, docker-compose.yml, GitHub isolation
→ infra-engineer: designs MQ topology, DB schema, pipeline DAG with 4 steps
→ project-architect: scaffolds 4 microservices (ingester, preprocessor, inference, exporter)
→ documentarian: generates architecture diagrams, pipeline DAG visualization, component catalog
```

## Workflow 5: Code Quality Pass

**Scenario:** Reviewing all services for convention compliance and fixing issues.

```
code-reviewer → (fix) → code-reviewer → documentarian
```

### Steps

1. **code-reviewer** — reviews all services, generates compliance reports
2. **(fix)** — user or main agent implements fixes for FAIL items
3. **code-reviewer** — re-reviews to verify fixes
4. **documentarian** — updates documentation if conventions evolved

## Tips for Effective Workflows

- **Start with the right agent.** Use the dispatch rules in `.claude/team.md` to pick the right starting agent.
- **Provide context.** Give agents the project name, relevant file paths, and specific requirements.
- **Review between steps.** Check each agent's output before dispatching the next one.
- **Skip unnecessary steps.** Not every workflow needs all steps — skip what doesn't apply.
- **Escalate early.** If an agent is struggling, escalate to the main conversation rather than letting it spin.
