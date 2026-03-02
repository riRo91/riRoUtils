# Dev Support Team

A coordination manifest for the riRoUtils agent team. The main agent reads this to understand which specialized agents are available, when to dispatch to them, and how to compose multi-agent workflows.

## Team Roster

| Agent | Role | Model | Tools | Skills | Use When |
|-------|------|-------|-------|--------|----------|
| **project-architect** | Bootstrap projects, design structure, set up isolation | opus | Read, Write, Edit, Bash, Glob, Grep | scaffold-project-structure, github-isolation-setup, scaffold-microservice | New project, new service, environment setup |
| **documentarian** | Extract docs, generate diagrams, persist knowledge | opus | Read, Write, Edit, Glob, Grep | post-implementation-docs, visualize-architecture, conversation-to-memory | After implementation, diagram requests, memory persistence |
| **debugger** | Systematic debugging, RCA, fix proposals | opus | Read, Bash, Glob, Grep | debugging-rca-report | Bug reports, errors, "not working", incident investigation |
| **infra-engineer** | K8s, MQ, databases, pipeline DAGs | opus | Read, Write, Edit, Bash, Glob, Grep | message-queue-patterns, database-metadata-patterns, pipeline-dag-definition | MQ topology, DB schema, pipeline/workflow design, K8s manifests |
| **code-reviewer** | Review conventions, sync rules | sonnet | Read, Glob, Grep | review-code-compliance, mirror-agent-rules | Code review, compliance check, rule sync |

## Dispatch Rules

Match the user's request to the best agent:

| Signal | Agent |
|--------|-------|
| "new project", "scaffold", "bootstrap", "set up" | project-architect |
| "document", "diagram", "visualize", "save learnings", "memory" | documentarian |
| "debug", "fix", "not working", "error", "investigate", "RCA" | debugger |
| "message queue", "RabbitMQ", "database", "MongoDB", "pipeline", "DAG", "K8s", "Helm" | infra-engineer |
| "review", "compliance", "check conventions", "sync rules", "mirror" | code-reviewer |

When the request doesn't clearly match one agent, handle it in the main conversation. If it becomes complex, dispatch to the most relevant agent.

## Composition Chains

Multi-agent workflows for common scenarios:

### Build & Document
1. **project-architect** — scaffolds the project/service
2. *(user or main agent implements features)*
3. **documentarian** — generates docs, diagrams, and memory files

### Debug & Fix
1. **debugger** — investigates, produces RCA report with fix recommendations
2. *(user or main agent implements the chosen fix)*
3. **code-reviewer** — reviews the fix for convention compliance
4. **documentarian** — documents the incident and resolution

### Infrastructure Setup
1. **infra-engineer** — designs MQ topology, DB schema, or pipeline DAG
2. **project-architect** — scaffolds the service that uses the infrastructure
3. **code-reviewer** — reviews the implementation

### Full Project Bootstrap
1. **project-architect** — creates project structure, GitHub isolation
2. **infra-engineer** — designs infrastructure (if needed)
3. **project-architect** — scaffolds microservices
4. **documentarian** — generates initial architecture diagrams

### Code Quality Pass
1. **code-reviewer** — reviews all services for compliance
2. *(user or main agent implements fixes)*
3. **code-reviewer** — re-reviews fixed code
4. **documentarian** — updates docs if conventions changed

## Escalation

When a subagent cannot solve something:

1. The subagent should clearly state what it tried and why it's blocked
2. Return control to the main conversation with a summary of findings
3. The main agent (or user) decides the next step:
   - Provide additional context and retry with the same agent
   - Dispatch to a different agent
   - Handle directly in the main conversation

## Adding New Agents

To add a new agent to the team:

1. Create `.claude/agents/{agent-name}.md` with YAML frontmatter (name, role, tools, skills)
2. Add the agent to the Team Roster table above
3. Add dispatch rules for the new agent
4. Update composition chains if the agent participates in workflows
5. Update `README.md` and `AGENT.md`
