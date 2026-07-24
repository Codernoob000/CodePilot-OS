# CodePilot OS - Development Plan

| Document control | Value |
|---|---|
| Product | CodePilot OS |
| Delivery target | Hackathon-quality Phase 1 MVP |
| Planning basis | PRD and Architecture baseline |
| Team | Frontend Engineer, Backend Engineer, AI Engineer, QA Engineer |
| Cadence | Four focused sprints across 10 working days |
| Status | Execution baseline |

## Executive Summary

This plan delivers a demonstrable, human-supervised multi-agent engineering workflow: a user connects a GitHub repository, receives a repository briefing, submits a feature request, reviews an agent-generated plan, explicitly approves it, follows a live multi-agent run, and inspects the resulting diff, validation evidence, findings, documentation changes, and evaluation.

The delivery strategy prioritizes the end-to-end “golden path” over broad platform coverage. Every sprint produces a usable vertical slice and preserves the architecture’s critical safety guarantees: durable workflow state, plan approval before write-capable execution, isolated workspaces, structured agent artifacts, audit events, and explicit export. Unsupported features are represented honestly in the UI rather than simulated as working automation.

The plan assumes a 10-working-day hackathon schedule with four concentrated sprints. If time compresses, the team must preserve the demo’s core loop and reduce optional integrations, concurrent-agent execution, and real GitHub branch export before weakening approval, evidence, or sandbox boundaries.

## MVP Definition

### User-visible outcome

A developer can select a GitHub repository, see it analyzed, submit a scoped request, approve a structured plan, watch specialized agents progress, and review a credible change package without CodePilot OS automatically merging or deploying anything.

### In-scope MVP capabilities

| Capability | Minimum implementation |
|---|---|
| Authentication and GitHub connection | Sign-in plus OAuth connection flow with least privilege and server-side token handling. |
| Project import | Select repository/default branch, resolve a pinned SHA, create project. |
| Repository intelligence | Static inventory, repository map, detected stack/test signals, source-cited summary, stale/failed states. |
| Request and planning | Feature request form, structured Planner output, Architect review, plan revision/approval gate. |
| Orchestration | Durable run/stage state machine with Planner, Architect, Developer, Reviewer, QA, Documentation, and Evaluator artifacts. |
| Execution | Isolated run workspace; scoped change generation; a safe fixture-repository path must work reliably. |
| Review | Unified diff, tests, findings, documentation, evaluator score, timeline. |
| Live dashboard | Current agent, state, elapsed time, meaningful status updates, action-required treatment. |
| Safety/evidence | Audit trail, policy checks, cancellation, sanitized error/test evidence. |
| Export | Downloadable patch is required; GitHub branch export is a stretch goal behind explicit user action. |

### MVP constraints

- GitHub is the only source-control provider.
- Support JavaScript/TypeScript and Python fixture/sample repositories first; other repositories receive best-effort analysis only.
- Default/protected branches remain read-only.
- No automatic merge, deployment, PR creation, enterprise controls, organization administration, or self-hosted runner.
- The product may use mocked/demo-safe agent behavior for a controlled fixture only if the UI labels it correctly; it must not misrepresent unexecuted tests or unavailable GitHub writes.

### Demo-critical golden path

```text
Connect GitHub -> Import fixture repo -> Analysis ready -> Submit request
-> Plan + architecture review -> Human approval -> Live agent run
-> Diff + QA evidence + reviewer findings + docs + evaluation -> Export patch
```

## Sprint Planning

### Sprint 1 - Foundation and repository intelligence

**Objective:** Establish the deployable product skeleton, secure project model, and a credible repository-analysis experience.

| Workstream | Scope | Primary owner |
|---|---|---|
| Product shell | Next.js routes, shared layout, project list, dashboard empty states, accessible component primitives. | Frontend |
| Platform foundation | FastAPI service, PostgreSQL schema/migrations, Redis queue, object-storage adapter, environment/config discipline. | Backend |
| GitHub/project flow | OAuth connection, repository picker, pinned branch SHA, project records, connection status. | Backend + Frontend |
| Analysis pipeline | Snapshot policy, static inventory, repository map, cited summary artifact, analysis lifecycle. | AI + Backend |
| Test framework | Fixture repos, API contract test harness, smoke-test baseline, security/error test checklist. | QA |

**Exit:** A signed-in user can import a safe fixture repository and see a durable project with analysis progress and a repository briefing.

### Sprint 2 - Planning, approval, and workflow state

**Objective:** Turn a request into an approved execution baseline with traceability.

| Workstream | Scope | Primary owner |
|---|---|---|
| Request UX | Feature request creation/editing, constraints and criteria fields, drafts, validation. | Frontend |
| Planning runtime | Planner and Architect structured artifacts, context assembly, schema validation, ambiguity/question handling. | AI |
| Workflow domain | Request/plan/run/stage tables, transition rules, approval transaction, audit and outbox. | Backend |
| Plan workspace | Revision comparison, architecture review, approval/reject/revise controls, action-required state. | Frontend |
| Validation | Plan schema, approval-gate, stale-analysis, authorization, and audit tests. | QA |

**Exit:** A request produces a revisioned plan and architecture review; no execution can start until an authorized user approves the current revision at a pinned source SHA.

### Sprint 3 - Agent execution and review evidence

**Objective:** Complete the core agent workflow in an isolated run workspace and expose reviewable artifacts.

| Workstream | Scope | Primary owner |
|---|---|---|
| Agent orchestration | Stage dependency graph, job claiming/retry/cancel, durable events, artifact persistence. | Backend + AI |
| Execution agents | Developer scoped workspace changes; Reviewer findings; QA test evidence; Documentation and Evaluator outputs. | AI |
| Sandbox adapter | Ephemeral workspace lifecycle, approved command execution, limits, sanitized outputs, path policy. | Backend |
| Run review UX | Live status, timeline, diff/file navigation, findings, tests, docs, evaluator tabs. | Frontend |
| End-to-end quality | Fixture-run execution, negative test cases, policy-block and test-failure verification. | QA |

**Exit:** An approved fixture-repository request reliably reaches review-ready with an inspectable diff and explicit evidence for each required agent stage.

### Sprint 4 - Demo polish, hardening, and release readiness

**Objective:** Make the golden path fast, clear, resilient, and presentation-ready.

| Workstream | Scope | Primary owner |
|---|---|---|
| Dashboard polish | Live SSE updates, active-agent cards, responsive review pages, loading/empty/error states, accessibility pass. | Frontend |
| Reliability/security | Idempotency, secret redaction, path policies, cancellation, observability, rate/budget limits. | Backend |
| Agent quality | Prompt/context tuning, deterministic fixture behavior, finding severity calibration, run summaries. | AI |
| Release validation | E2E smoke suite, accessibility scan, performance checks, demo rehearsal, defect triage. | QA |

**Exit:** The staging demo works repeatedly from clean state, errors are understandable, evidence is truthful, and all demo-critical acceptance scenarios pass.

## Milestones

| Milestone | Objective | Deliverables | Dependencies | Definition of Done | Estimated duration | Risk |
|---|---|---|---|---|---|---|
| M0: Delivery foundation | Enable parallel work safely. | Repository structure, environments, CI checks, schemas, fixture repo. | None. | Web/API deploy independently; CI runs type/lint/test baseline; team can work against shared contracts. | 0.5 day | Setup drag or credential delays. |
| M1: Connected project | Create a trusted imported project. | Auth, GitHub OAuth, repo picker, project/connection records. | M0, GitHub OAuth app. | Supported user imports fixture repo and sees correct pinned SHA; token absent from UI/logs. | 1.5 days | OAuth scope/callback configuration. |
| M2: Intelligence ready | Show repository context worth planning from. | Analysis jobs, inventory/map, cited briefing, status states. | M1, queue/storage. | Analysis result has source SHA, stack/test signals, citations, and retryable failure state. | 1 day | Unexpected repo shapes or sandbox provisioning. |
| M3: Approved plan | Establish human-controlled execution baseline. | Request form, Planner/Architect artifacts, revisions, approval/audit. | M2, agent contracts. | Approved revision, actor, timestamp, and source SHA recorded atomically; execution blocked otherwise. | 2 days | Schema/prompt instability; state-race bugs. |
| M4: Review-ready run | Produce a useful supervised change package. | Run state machine, sandbox, Developer/Reviewer/QA/Docs/Evaluator, artifacts. | M3, sandbox, OpenAI access. | Fixture request yields diff, test results, findings, docs and criteria evaluation; policy blocks work. | 3 days | Agent quality, test execution, integration timing. |
| M5: Demo-ready release | Deliver a reliable public story. | Dashboard, SSE, patch export, monitoring, QA report, demo script. | M4. | Five consecutive clean golden-path runs in staging; no P0/P1 defects. | 2 days | Late regressions and demo-environment dependencies. |

## GitHub Issues

### Epic 1: Platform and project foundation

#### CP-001 - Establish monorepo, environments, and CI baseline

**Description:** Create the application skeleton and delivery controls for the Next.js web app, FastAPI API, worker, shared contracts, staging configuration, and safe fixture repositories.

**Acceptance Criteria:**

- Web, API, and worker have independent local and staging startup paths.
- Pull requests run formatting, lint/type checks, tests, dependency scan, and secret scan.
- Environment-specific values are supplied through managed configuration, not committed files.
- A documented safe fixture repository is available for end-to-end tests.

**Priority:** P0  
**Labels:** `epic:foundation`, `platform`, `devops`  
**Dependencies:** None  
**Estimated Story Points:** 5

#### CP-002 - Implement core PostgreSQL schema, migrations, and audit/outbox foundation

**Description:** Add durable entities for users, connections, projects, analyses, requests, plans, approvals, runs, stages, artifacts, audit events, and outbox events.

**Acceptance Criteria:**

- Schema supports project-scoped ownership, immutable plan revisions, run baselines, and typed artifacts.
- Approval, audit event, run creation, and outbox publication intent commit transactionally.
- Migrations are versioned, repeatable in staging, and backward-compatible for the demo path.
- Queries support project list, active runs, timeline, and artifact lookups.

**Priority:** P0  
**Labels:** `backend`, `database`, `architecture`  
**Dependencies:** CP-001  
**Estimated Story Points:** 8

#### CP-003 - Build authentication and GitHub OAuth connection flow

**Description:** Implement sign-in/session verification and a server-side GitHub OAuth connection lifecycle for repository access.

**Acceptance Criteria:**

- OAuth uses state validation and PKCE where supported; callback executes server-side.
- GitHub credentials are encrypted at rest and never returned to browser clients or logs.
- User can connect, inspect connection state, and disconnect.
- Permission/error states are understandable and testable with a test account.

**Priority:** P0  
**Labels:** `backend`, `security`, `github`  
**Dependencies:** CP-001, CP-002  
**Estimated Story Points:** 8

#### CP-004 - Deliver project import and repository selection UI

**Description:** Provide the frontend flow for selecting an authorized repository/default branch and creating a project.

**Acceptance Criteria:**

- User can search/list permitted repositories and select a default branch.
- UI shows permissions/loading/errors and projects only after successful API confirmation.
- Project list shows connection and analysis state.
- All controls are keyboard operable and have accessible labels.

**Priority:** P0  
**Labels:** `frontend`, `github`, `ux`  
**Dependencies:** CP-003  
**Estimated Story Points:** 5

### Epic 2: Repository intelligence

#### CP-005 - Implement asynchronous repository analysis pipeline

**Description:** Resolve the source SHA, create an isolated snapshot, enforce repository limits, and generate a static inventory without executing repository code.

**Acceptance Criteria:**

- Analysis records queued, analyzing, ready, failed, and stale states.
- Pipeline enforces configured snapshot/file-count/binary limits before model work.
- Inventory identifies paths, languages, manifests, CI/test configuration, and candidate entry points.
- Failures retain sanitized error category and retry guidance.

**Priority:** P0  
**Labels:** `backend`, `worker`, `repository-intelligence`  
**Dependencies:** CP-002, CP-003  
**Estimated Story Points:** 8

#### CP-006 - Create repository context pack and cited briefing agent

**Description:** Build a bounded, redacted context pack and use the AI runtime to create an architecture summary with source citations and inference labels.

**Acceptance Criteria:**

- Generated/vendor/binary/sensitive content is excluded by policy.
- Summary includes technologies, structure, conventions, test signals, caveats, and path citations.
- AI output validates against a versioned schema.
- Analysis is tied to an immutable SHA and marked stale on default-branch change.

**Priority:** P0  
**Labels:** `ai`, `repository-intelligence`, `security`  
**Dependencies:** CP-005  
**Estimated Story Points:** 8

#### CP-007 - Build repository intelligence UI

**Description:** Display analysis lifecycle, repository map, detected stack, test signals, summary, citations, and stale/retry state.

**Acceptance Criteria:**

- Users can distinguish facts, inferences, exclusions, and analysis failures.
- Citation links open the referenced repository path/artifact.
- Project overview exposes analysis readiness and next action.
- UI remains usable at narrow desktop/tablet widths.

**Priority:** P0  
**Labels:** `frontend`, `repository-intelligence`  
**Dependencies:** CP-004, CP-005, CP-006  
**Estimated Story Points:** 5

### Epic 3: Planning and approval

#### CP-008 - Build feature request authoring and drafts

**Description:** Implement project-scoped request creation with title, desired outcome, context, constraints, and acceptance criteria.

**Acceptance Criteria:**

- Required fields validate in browser and API.
- Drafts persist and can be edited before submission.
- Request page explains desired observable behavior and current analysis state.
- Unauthorized users cannot create or modify requests.

**Priority:** P0  
**Labels:** `frontend`, `backend`, `planning`  
**Dependencies:** CP-002, CP-007  
**Estimated Story Points:** 5

#### CP-009 - Implement Planner and Architect structured stages

**Description:** Generate a plan and design review from the request and bounded repository context, including blocking questions where information is insufficient.

**Acceptance Criteria:**

- Plan schema includes objective, assumptions, affected paths, ordered steps, risks, test strategy, and assignments.
- Architect output identifies boundaries, dependencies, and risks.
- Essential ambiguity results in a blocking question, not invented behavior.
- Invalid model output is retained as a stage failure and cannot activate execution.

**Priority:** P0  
**Labels:** `ai`, `planning`, `agent-framework`  
**Dependencies:** CP-006, CP-008  
**Estimated Story Points:** 8

#### CP-010 - Implement plan revision, approval gate, and audit UX

**Description:** Allow editing/regeneration, revision comparison, explicit approval/rejection, and visible audit evidence.

**Acceptance Criteria:**

- Approval applies only to the displayed current revision and expected version.
- Approval captures actor, timestamp, source SHA, and plan revision atomically.
- Execute action is unavailable/denied before approval or when analysis is stale.
- User can see revision history and required clarification state.

**Priority:** P0  
**Labels:** `frontend`, `backend`, `workflow`, `security`  
**Dependencies:** CP-008, CP-009  
**Estimated Story Points:** 8

### Epic 4: Orchestration, execution, and evidence

#### CP-011 - Implement durable run state machine and task orchestration

**Description:** Implement run/stage transitions, queue claiming, dependency graph, retries, cancellation, durable events, and idempotency controls.

**Acceptance Criteria:**

- Run supports draft/planning/awaiting approval/queued/running/clarification/review-ready/failed/cancelled/exported states.
- Stage attempts are idempotent, lease-protected, and have bounded retries.
- Cancellation stops eligible work and preserves existing artifacts.
- Every state transition creates timeline and audit evidence.

**Priority:** P0  
**Labels:** `backend`, `worker`, `workflow`  
**Dependencies:** CP-002, CP-010  
**Estimated Story Points:** 13

#### CP-012 - Build restricted sandbox and run workspace adapter

**Description:** Provision short-lived workspaces at the approved SHA, implement path policy, resource limits, approved command execution, and sanitized logs.

**Acceptance Criteria:**

- Workspace is isolated from API host and has no production credentials/host mounts.
- Default/protected branch is never modified; all writes remain run-local.
- Sensitive paths are denied and logged before modification.
- Command result records label, status, duration, output limit, and sanitized output.

**Priority:** P0  
**Labels:** `backend`, `security`, `sandbox`  
**Dependencies:** CP-005, CP-011  
**Estimated Story Points:** 13

#### CP-013 - Implement Developer, Reviewer, QA, Documentation, and Evaluator stages

**Description:** Complete the role-specific artifact pipeline using schema-validated agents and scoped tools.

**Acceptance Criteria:**

- Developer outputs change set and implementation notes within allowed paths.
- Reviewer emits severity-classified, evidence-linked findings.
- QA creates/updates tests when feasible and never reports unexecuted tests as passed.
- Documentation writes only permitted documentation paths; Evaluator maps each criterion to pass/partial/fail/not verifiable.
- Blocker/high findings require explicit human resolution before final completion/export.

**Priority:** P0  
**Labels:** `ai`, `agent-framework`, `quality`  
**Dependencies:** CP-009, CP-011, CP-012  
**Estimated Story Points:** 13

#### CP-014 - Build live run dashboard, timeline, and unified review

**Description:** Provide an accessible live run view with agent status, meaningful updates, artifacts, diff, tests, findings, documentation, and evaluation.

**Acceptance Criteria:**

- Current role/state/elapsed time/last update are visible without refresh.
- Timeline is chronological, paginated, and links to artifacts.
- Review view provides changed files, line diff, test evidence, findings, docs, and acceptance-criteria score.
- Color is not the sole means of communicating status; keyboard navigation works.

**Priority:** P0  
**Labels:** `frontend`, `workflow`, `review`, `accessibility`  
**Dependencies:** CP-011, CP-013  
**Estimated Story Points:** 13

#### CP-015 - Add SSE event delivery and reconnection

**Description:** Stream authorized resource-version events to active project/run views and refetch canonical state after reconnect.

**Acceptance Criteria:**

- Events are authorized per project and include monotonic IDs.
- Browser reconnects using last event ID and invalidates affected queries.
- Duplicate/missed events do not create incorrect UI state.
- Status update reaches dashboard within five seconds in staging test.

**Priority:** P1  
**Labels:** `frontend`, `backend`, `realtime`  
**Dependencies:** CP-011, CP-014  
**Estimated Story Points:** 5

### Epic 5: release quality and export

#### CP-016 - Implement explicit patch export and optional GitHub branch export

**Description:** Package a review-ready run into a downloadable patch; add remote branch/commit export only if OAuth scope and time permit.

**Acceptance Criteria:**

- Export is a separate explicit user command and audit event.
- Patch contains the reviewed run-local diff and summary metadata.
- If branch export ships, it uses a CodePilot-prefixed branch and never targets protected/default branch.
- Export failures preserve evidence and provide retry guidance.

**Priority:** P1  
**Labels:** `backend`, `github`, `export`  
**Dependencies:** CP-013, CP-014  
**Estimated Story Points:** 5

#### CP-017 - Add observability, cost budgets, and safety hardening

**Description:** Instrument the golden path and enforce redaction, rate limits, model/sandbox budgets, and policy events.

**Acceptance Criteria:**

- Correlation IDs connect API, worker, stage, and sandbox logs.
- Dashboard/support can locate a run by run ID without source-code disclosure.
- Token/time/output/concurrency budgets stop or pause over-limit runs visibly.
- No test fixtures or manual checks expose OAuth tokens, secrets, or raw private artifacts.

**Priority:** P0  
**Labels:** `backend`, `security`, `observability`  
**Dependencies:** CP-011, CP-012, CP-013  
**Estimated Story Points:** 8

#### CP-018 - Execute end-to-end QA, accessibility pass, and demo rehearsal

**Description:** Validate the release against the PRD acceptance scenarios, prepare fixtures/data, and rehearse the full demo including recovery paths.

**Acceptance Criteria:**

- Automated smoke test covers import, analysis, request, approval, run, review, and patch export.
- Keyboard-only walkthrough and automated accessibility scan find no critical issues.
- Test failure, policy block, clarification, cancellation, and retry are demonstrated or documented.
- Five consecutive staging golden-path runs pass before demo day.

**Priority:** P0  
**Labels:** `qa`, `accessibility`, `release`  
**Dependencies:** CP-014, CP-015, CP-016, CP-017  
**Estimated Story Points:** 8

## Build Order

The sequence below is mandatory because each step makes later work testable and reduces costly rework.

1. CP-001 - Monorepo, environments, CI, fixture repository.
2. CP-002 - PostgreSQL schema, migrations, audit/outbox model.
3. CP-003 - Authentication and GitHub OAuth connection.
4. CP-004 - Repository selection/project import UI.
5. CP-005 - Async repository analysis pipeline.
6. CP-006 - Context pack and cited briefing agent.
7. CP-007 - Repository intelligence UI.
8. CP-008 - Feature request authoring/drafts.
9. CP-009 - Planner/Architect structured stages.
10. CP-010 - Plan revisions, approval, audit gate.
11. CP-011 - Durable run state machine and orchestration.
12. CP-012 - Restricted sandbox/workspace adapter.
13. CP-013 - Developer through Evaluator agent stages.
14. CP-014 - Live dashboard and unified review.
15. CP-015 - SSE delivery/reconnection.
16. CP-017 - Observability, budgets, hardening.
17. CP-016 - Explicit patch export; branch export only after patch is stable.
18. CP-018 - End-to-end release validation and rehearsals.

## Feature Priority (MoSCoW)

| Must Have | Should Have | Could Have | Won't Have in MVP |
|---|---|---|---|
| Auth/GitHub import; pinned SHA; repository analysis; feature request; Planner/Architect; approval gate; durable run state; isolated workspace; Developer/Reviewer/QA/Docs/Evaluator artifacts; unified review; timeline; cancellation; patch export; audit and redaction | SSE live updates; plan diff/revision comparison; retry eligible stage; GitHub branch export; dashboard filters; basic notifications | Agent-configurable prompts; cost-estimate UI; multiple active runs; inline review comments; richer language inference | Autonomous merge/deploy; PR creation if time-limited; GitLab/Bitbucket; enterprise SSO/SCIM; org admin/RBAC UI; self-hosted runners; marketplace; mobile app |

## Team Parallelization

The team works in vertically coordinated lanes with shared contracts. The Backend Engineer owns workflow correctness and integration boundaries; the AI Engineer owns structured agent behavior and bounded context; the Frontend Engineer owns the user-facing supervisory experience; the QA Engineer creates fixtures and tests the contracts from day one. No role should wait for a fully finished feature before beginning.

| Phase | Frontend Engineer | Backend Engineer | AI Engineer | QA Engineer |
|---|---|---|---|---|
| Days 1-2 | App shell, project pages, mocked API contracts. | Schema, API skeleton, auth/OAuth. | Agent schemas, fixture-repo analysis expectations. | Fixture repos, test strategy, CI smoke scaffold. |
| Days 3-4 | Intelligence and request/plan pages with contract fixtures. | Analysis queue, artifacts, plan/approval domain. | Context pack, Planner/Architect prompts and evaluations. | Contract tests, negative analysis cases, approval-gate tests. |
| Days 5-7 | Live run/review UX using fixture events and artifacts. | State machine, queue, sandbox adapter, audit events. | Developer/Reviewer/QA/Docs/Evaluator stages. | E2E run tests, policy-block/test-failure/cancel cases. |
| Days 8-10 | SSE, error states, accessibility, demo polish. | Export, monitoring, budgets, reliability fixes. | Prompt tuning, deterministic demo fallback, evaluation calibration. | Regression triage, accessibility/performance, rehearsal sign-off. |

### Coordination rules

1. Freeze API and artifact schemas at the start of each sprint; changes require an explicit contract-version note.
2. Use fixture artifacts/events so frontend work is never blocked by live model latency.
3. Hold a 15-minute daily integration review: current blocker, contract drift, demo-path status, and next handoff.
4. Merge vertical slices behind feature flags where a partial backend or UI would otherwise confuse demo users.
5. QA owns a visible acceptance matrix mapped to PRD requirements and reports truthfully whether an outcome is live, mocked, or unavailable.

## Risk Analysis

### Technical Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|---|---:|---:|---|---|
| GitHub OAuth/export complexity | Medium | High | Validate OAuth app, scopes, and callback on Day 1. | Ship patch export only; use pre-connected demo account. |
| Sandbox is not stable/secure enough | Medium | High | Use bounded fixture repo, non-root ephemeral execution, no secrets/egress. | Limit demo to static analysis and controlled change artifacts; clearly label. |
| Model output is invalid/inconsistent | High | High | Strict schemas, retries, fixture evaluation set, deterministic context. | Use curated successful artifact fixtures for demo recovery, not hidden substitution. |
| Queue/state race conditions | Medium | High | Outbox, idempotency, transition tests, single active run per project. | Disable concurrency and retain manual retry for demo. |
| Live updates are unreliable | Medium | Medium | SSE with polling fallback/refetch on focus. | Use visible refresh and progress timestamps. |
| Large diff/artifact performance | Medium | Medium | Fixture limits, pagination, virtualized diff. | Show summary and selected-file diff only. |

### Product Risks

| Risk | Mitigation |
|---|---|
| Product appears like generic chat rather than supervised engineering system. | Center approval, agent cards, evidence, and timeline in demo narrative. |
| Users do not trust generated changes. | Show plan baseline, citations, test evidence, reviewer findings, and explicit human controls. |
| Scope exceeds hackathon time. | Maintain Must/Should boundary and review it daily; do not begin enterprise/multi-SCM work. |
| Demo claims exceed implementation. | Publish clear capability labels and script only validated flows. |

### Schedule Risks

| Risk | Trigger | Response |
|---|---|---|
| M1 slips past Day 2 | OAuth/import unavailable | Parallelize UI against fixtures; switch to preconfigured demo project while connection is repaired. |
| M3 slips past Day 4 | No approved-plan baseline | Cut real-time and branch export; focus team on plan/run vertical slice. |
| M4 slips past Day 7 | Run does not reach review-ready reliably | Narrow to one fixture request/repository; remove optional agent concurrency; pair Backend and AI. |
| P0 defects on Day 9 | Golden-path failure rate > 10% | Feature freeze; QA-led triage; no new scope. |

## Daily Timeline

| Day | Focus | Planned outcome | Demo checkpoint |
|---|---|---|---|
| 1 | Setup and contracts | CP-001 started; shared schemas, fixture repo, environments; OAuth app requested. | Static UI shell and API health page. |
| 2 | Import foundation | CP-002/003/004 operational against a test GitHub repo. | Connect and create project from pinned SHA. |
| 3 | Repository intelligence | CP-005/006 analysis output persisted; CP-007 renders it. | Import -> analysis-ready walkthrough. |
| 4 | Request and plan | CP-008/009 produce structured plan/review. | User submits request and sees a plan. |
| 5 | Approval baseline | CP-010 and CP-011 state machine active. | Plan cannot run before approval; audit visible. |
| 6 | Execution workspace | CP-012 stable for fixture repository; Developer stage begins. | Approved run reaches a controlled workspace/diff. |
| 7 | Evidence pipeline | CP-013 and CP-014 complete core review package. | End-to-end run with diff, QA, reviewer, evaluator. |
| 8 | Live and export | CP-015/016/017 integrated; error states improved. | Live dashboard and explicit patch export. |
| 9 | Hardening | CP-018 test suite, accessibility, security/performance fixes. | Three consecutive staging golden-path runs. |
| 10 | Freeze and demo | Final regression, rehearsal, backup artifacts, pitch recording. | Five clean runs; fallback demo route confirmed. |

## Deliverables

By demo day, the following must exist:

1. A deployed CodePilot OS web application and API/worker staging environment.
2. A test GitHub connection flow or documented pre-connected demo account with least-privilege configuration.
3. At least one safe fixture repository and one polished feature request that reliably demonstrate the golden path.
4. Repository intelligence view with a pinned SHA, stack/map, citations, analysis state, and caveats.
5. Feature request, structured plan, architecture review, plan revision, and explicit approval experience.
6. A durable run timeline with named Planner, Architect, Developer, Reviewer, QA, Documentation, and Evaluator stages.
7. A review-ready package: file diff, test evidence, reviewer severity findings, documentation change, and acceptance-criteria evaluation.
8. Human clarification, cancellation, policy-block, and failure-state UX that does not claim false success.
9. Explicit downloadable patch export and audit event; branch export only if tested and approved.
10. Baseline monitoring/logging, secret redaction checks, run IDs, and a documented demo/recovery playbook.
11. Automated smoke test report, accessibility check, known-limitations list, and demo recording/backup screenshots.

## Quality Gates

| Sprint | Exit criteria | Evidence owner |
|---|---|---|
| Sprint 1 | CI green; project import works against fixture; analysis persists pinned SHA and cited results; no credentials in UI/logs. | QA + Backend |
| Sprint 2 | Request/plan/review artifacts validate schemas; plan approval is atomic/audited; stale analysis and unauthorized execution are denied. | QA + AI + Backend |
| Sprint 3 | Approved fixture run completes with all required artifact types; failed test is not reported as pass; sensitive-path edit is blocked; cancel retains evidence. | QA + Backend + AI |
| Sprint 4 | Five consecutive staging golden paths pass; P0/P1 defects are zero; keyboard journey passes; status update meets five-second target; demo script and fallback tested. | QA (release sign-off) |

### Release gate checklist

- [ ] The golden-path demo is reproducible from a clean project/run state.
- [ ] Every user-visible agent state has a truthful terminal/next-action explanation.
- [ ] No write-capable stage begins without an approved current plan revision and pinned SHA.
- [ ] All generated/test artifacts shown in the UI correspond to real stored evidence.
- [ ] Default/protected branches are never modified automatically.
- [ ] Security-sensitive paths and secret-like output are denied or redacted and recorded.
- [ ] P0/P1 defects are resolved; known limitations are documented for judges/users.
- [ ] A backup demo recording and static artifact package are ready.

## Appendix: Delivery Metrics

Track these daily during the hackathon:

| Metric | Target |
|---|---|
| Golden-path completion rate | At least 90% in staging by Day 9; 100% in five release-candidate runs. |
| Time from approval to review-ready on fixture | Under 20 minutes, with meaningful intermediate events. |
| Critical acceptance criteria passing | 100% of Must Have criteria. |
| Unresolved P0/P1 defects | 0 at release gate. |
| UI action-required comprehension | All reviewers can identify current agent, pause reason, and next action in rehearsal. |
| Test evidence integrity | 0 cases where skipped/failed/unexecuted work is presented as passed. |

