# CodePilot OS — Product Requirements Document

| Document control | Value |
|---|---|
| Product | CodePilot OS |
| Tagline | Your AI Engineering Team, Not Just an AI Assistant. |
| Status | Phase 1 MVP baseline |
| Owner | Product Management |
| Intended audience | Product, design, engineering, security, DevOps, and AI teams |
| Last updated | 2026-07-24 |

## 1. Executive Summary

CodePilot OS is a web-based engineering workspace in which a developer supervises a coordinated set of specialized AI agents. Rather than asking a single chat assistant to produce isolated code, a user imports a GitHub repository, describes an outcome, reviews a proposed plan, and watches planner, architect, developer, reviewer, QA, and documentation agents execute a transparent workflow. The result is a reviewable change set, test evidence, updated documentation, and a persistent record of human decisions.

The Phase 1 product is intentionally a high-quality MVP for individual developers and small teams. It validates the critical loop: **repository → request → plan → human approval → agent execution → evidence → human review**. CodePilot OS will not merge or deploy production changes autonomously in the MVP. Its value is trustworthy orchestration, clear status, and a useful output that users can take back to GitHub.

## 2. Product Vision

Make software development feel like leading a capable, visible engineering team. CodePilot OS should turn a vague feature request into a traceable engineering workflow while keeping a developer in control of scope, decisions, and source changes.

In the long term, CodePilot OS becomes an operating layer over a software project: it understands the repository, maintains architectural context, coordinates expert agents, continuously evaluates quality, and learns from approved human feedback. The product must earn this role through transparency, not through opaque automation.

## 3. Problem Statement

AI coding tools accelerate code authoring but leave most engineering work fragmented. Developers still reconstruct repository context, decide implementation boundaries, coordinate reviews and tests, update documentation, and judge whether generated output is safe. A single assistant conversation makes delegation implicit: users cannot easily see what was assumed, what files were inspected, what agent is responsible, or whether validation occurred.

This creates three failures: generated code may violate local architecture; quality tasks are skipped under time pressure; and users cannot confidently delegate multi-step work. CodePilot OS addresses these failures with repository intelligence, explicit task handoffs, approval gates, evidence, and an auditable timeline.

## 4. Goals

| ID | Goal | Measure of success |
|---|---|---|
| G1 | Shorten the path from feature request to a reviewable implementation package. | Median time from approved plan to completed run is under 20 minutes for supported sample repositories. |
| G2 | Make multi-agent work understandable and controllable. | At least 80% of usability-test participants can identify current agent, next action, and approval state without help. |
| G3 | Produce changes that respect repository context. | At least 80% of completed MVP runs pass automated checks supplied by the repository or configured runner. |
| G4 | Keep humans accountable for consequential decisions. | 100% of write-capable execution runs have an approved plan and recorded approver. |
| G5 | Provide credible hackathon-quality product polish. | A new user can connect, import, request, approve, and inspect a first run in one session. |

## 5. Non Goals

The MVP will not provide autonomous production deployment, direct merging to protected branches, enterprise SSO/SCIM, organization-wide policy management, billing, self-hosted runners, mobile apps, full project-management replacement, or an agent marketplace. It will not claim semantic understanding of every language or guarantee that generated changes are correct. It is also not a general-purpose chat product; chat is supporting context, not the primary workflow.

## 6. Success Metrics

| Metric | Definition | MVP target |
|---|---|---|
| Activation rate | Users who complete repository analysis and create a request / users who connect a repository | ≥ 55% |
| Plan approval rate | Approved plans / plans generated | ≥ 60% |
| Run completion rate | Runs reaching a terminal state with artifacts / started runs | ≥ 75% |
| Validation pass rate | Completed runs whose configured checks pass | ≥ 70% initially |
| Time to first value | Time from sign-in to first repository intelligence summary | ≤ 10 minutes p50 |
| Human intervention clarity | Users correctly describing why a run paused in moderated tests | ≥ 80% |
| Trust score | “I understand what CodePilot changed and why” rating (4–5/5) | ≥ 75% |

Metrics are segmented by repository size, language, request type, and whether the run required clarification. A successful run is not merely one that emits code; it must provide an inspectable diff and a recorded validation outcome.

## 7. User Personas

| Persona | Context and need | Primary jobs | Product implications |
|---|---|---|---|
| Solo builder Sam | Ships quickly with limited review capacity. | Turn ideas into safe pull-request-ready changes. | Fast setup, plain language, clear artifacts. |
| Startup engineer Aisha | Works in a small, fast-moving codebase. | Preserve architecture while delivering features. | Repository map, plan controls, review and test evidence. |
| AI engineer Diego | Experiments with agents and model behavior. | Inspect prompts, assumptions, and failures. | Detailed timeline, agent inputs/outputs, rerun controls. |
| Student Priya | Learns through building and lacks project context. | Understand how a change affects a codebase. | Explanatory plans, accessible terminology, safe defaults. |
| Tech lead Morgan | Needs confidence before accepting AI-produced work. | Evaluate scope, risk, and quality. | Approval gate, change summary, reviewer findings. |

## 8. User Stories

| ID | User story | Priority |
|---|---|---|
| US-01 | As a developer, I can connect a GitHub repository so CodePilot has a bounded project context. | Must |
| US-02 | As a developer, I can see analysis status and repository facts before delegating work. | Must |
| US-03 | As a developer, I can submit a feature request with constraints and acceptance criteria. | Must |
| US-04 | As a developer, I can inspect and edit the execution plan before code can be changed. | Must |
| US-05 | As a developer, I can approve, reject, or request changes to a plan. | Must |
| US-06 | As a developer, I can watch agent progress and understand pauses or failures. | Must |
| US-07 | As a reviewer, I can inspect a file-level diff, tests, and findings in one place. | Must |
| US-08 | As a developer, I can receive documentation changes with implementation output. | Should |
| US-09 | As a user, I can rerun a failed stage without silently discarding prior evidence. | Should |
| US-10 | As a user, I can export a completed change package to GitHub. | Should |

## 9. Functional Requirements

### 9.1 Repository import and connection

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-01 | Support GitHub OAuth connection and repository selection for accounts the user can access. | User can connect, view a searchable repository list, choose a repository and default branch, or disconnect. |
| FR-02 | Request least-privilege GitHub access. | The UI explains requested scopes before authorization; tokens are never displayed in logs or activity content. |
| FR-03 | Create a project record for each imported repository. | Project has name, repository URL, default branch, import time, analysis state, and visible connection status. |
| FR-04 | Handle inaccessible or oversized repositories safely. | Import fails with a specific, actionable message; no partial write run begins. Supported MVP limits are documented in-product. |

### 9.2 Repository intelligence

On import, the Intelligence service indexes the default branch and presents a repository briefing. It must identify root files, languages, package/build manifests, test locations, CI configuration when detectable, major directories, entry points when inferable, and a concise architecture summary. The system must label inferences as inferences.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-05 | Show analysis progress and terminal state. | Dashboard shows queued, analyzing, ready, failed, or stale; failure includes retry guidance. |
| FR-06 | Produce a browsable repository map. | User can view directory hierarchy, detected technologies, test commands if discovered, and generated summary. |
| FR-07 | Preserve source citations for AI claims. | Architecture summary links each important claim to one or more paths where feasible. |
| FR-08 | Detect context staleness. | A changed default-branch SHA marks analysis stale and prompts re-analysis before a new write run. |

### 9.3 Request and planning workflow

The request form contains a title, desired outcome, optional context, constraints, and acceptance criteria. It should guide users to provide observable behavior instead of implementation dictates. A Planner Agent transforms the request and repository briefing into a plan. An Architect Agent reviews the plan for boundaries, dependencies, data/API implications, and risks.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-09 | Create a feature request. | Required title and outcome are validated; request is saved as a draft until submitted. |
| FR-10 | Generate a structured execution plan. | Plan includes objective, assumptions, impacted files/modules, ordered steps, risks, test strategy, and agent assignments. |
| FR-11 | Surface ambiguity. | If essential information is missing, Planner creates a blocking question rather than inventing a behavior. |
| FR-12 | Permit plan editing and revision. | User can edit plan text, regenerate with feedback, and compare plan revisions. Approval applies to a specific revision. |
| FR-13 | Require explicit approval before write-capable work. | Execution control remains disabled until current revision is approved; audit records approver and timestamp. |

### 9.4 Agent orchestration

The MVP has seven named agents: Planner, Architect, Developer, Reviewer, QA, Documentation, and Evaluator. Agent labels represent clear responsibilities, even where early implementation shares an underlying model runtime. The orchestration engine executes a directed workflow and persists inputs, outputs, state changes, and artifacts.

| Agent | Responsibility | May modify source? | Required output |
|---|---|---:|---|
| Planner | Convert request to executable plan; ask blocking questions. | No | Plan and assumptions |
| Architect | Assess design fit and risks. | No | Architecture review |
| Developer | Implement approved scoped changes in isolated workspace. | Yes | Diff and implementation notes |
| Reviewer | Inspect diff for correctness, regressions, and maintainability. | No | Findings with severity |
| QA | Create/run relevant tests and summarize results. | Yes, tests only | Test evidence |
| Documentation | Update impacted docs/comments as appropriate. | Yes, docs only | Documentation diff |
| Evaluator | Score completeness against plan and acceptance criteria. | No | Run score and gaps |

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-14 | Execute agents in an explicit state machine. | Each run exposes queued, running, waiting_for_human, failed, cancelled, or completed; each agent stage has same states. |
| FR-15 | Isolate source modifications. | Developer, QA, and Documentation operate on a run-specific working branch/workspace; default branch is read-only. |
| FR-16 | Constrain agent scope. | Developer receives approved plan, relevant repository context, and policy; attempts to edit excluded sensitive paths are blocked and logged. |
| FR-17 | Support human clarification. | Any blocking question pauses run and presents response field; resume creates a traceable new event. |
| FR-18 | Preserve failure evidence. | A failed stage records error category, relevant sanitized logs, inputs reference, and retry eligibility. |
| FR-19 | Support cancellation. | User can cancel queued/running run; in-flight work is stopped safely and terminal state retains artifacts already created. |

### 9.5 Review, testing, documentation, and evaluation

Reviewer findings use severity levels: blocker, high, medium, low, and informational. Blocker or high findings pause before final completion until explicitly resolved, waived with rationale, or the run is cancelled. QA selects relevant tests from repository evidence and plan; it must never report a test as passed when it was not executed.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-20 | Show unified change review. | User can inspect changed files, line diff, agent rationale, test result, and review findings without leaving run view. |
| FR-21 | Generate or update tests when feasible. | QA proposes or commits targeted tests; if infeasible, it states why and identifies manual verification. |
| FR-22 | Execute configured validation in sandbox. | Results include command label, status, duration, truncated sanitized output, and environment constraints. |
| FR-23 | Update documentation selectively. | Documentation Agent changes only relevant existing docs or creates a clearly named new doc when no appropriate home exists. |
| FR-24 | Evaluate against acceptance criteria. | Evaluator maps every criterion to pass, partial, fail, or not verifiable, with evidence links. |
| FR-25 | Package/export results. | Completed run offers a branch/commit reference or downloadable patch and summary; export never occurs without user action. |

### 9.6 Dashboard, timeline, and notifications

The dashboard is the supervisory surface. It has project health, active runs, agent cards, approval queue, recent activity, and completed-run history. “Live” means state updates delivered without full page refresh; it does not imply token-by-token model output.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-26 | Present live agent status. | Each active agent displays role, current task, state, elapsed time, and last meaningful update. |
| FR-27 | Maintain chronological activity timeline. | Timeline records requests, approvals, agent starts/stops, questions, artifacts, retries, and export actions. |
| FR-28 | Make action required unmissable. | Approval/clarification states show a clear call to action and reason; they are accessible by keyboard and screen reader. |
| FR-29 | Retain run history. | User can filter prior runs by status, repository, date, and request; each history item opens immutable run details. |

## 10. Non-Functional Requirements

| Area | Requirement |
|---|---|
| Performance | Standard dashboard views load within 2.5 seconds p75 on supported broadband; status update visible within 5 seconds of backend event. |
| Reliability | Persist state before advancing agent stages; target 99% successful event persistence for MVP. |
| Observability | Every run has correlation ID, stage timings, model/runtime version, sanitized errors, and audit events. |
| Usability | Core path is operable without documentation by a developer familiar with GitHub. |
| Maintainability | Agent interfaces use versioned structured schemas; changing one agent’s prompt/output must not require rewriting UI history. |
| Localization | English-only MVP, but UI strings are externalized and timestamps use user locale/time zone. |

## 11. Technical Constraints

1. GitHub is the sole source-control provider for the MVP; GitLab and Bitbucket are explicitly deferred.
2. Source analysis and execution occur in ephemeral isolated environments with no credentials from the imported repository exposed to model prompts.
3. The system must enforce configurable repository-size, file-count, binary-file, run-duration, and output-size limits. Initial defaults: 250 MB repository snapshot, 100,000 files, 30-minute run, 10 MB per artifact.
4. Default branch and protected branches are read-only. Generated work uses an isolated branch named with a CodePilot prefix.
5. Agent execution must accept structured context and return structured artifacts; free-form text alone cannot drive privileged workflow transitions.
6. The UI should target current Chrome, Edge, Firefox, and Safari desktop versions; responsive tablet support is desirable but not launch-blocking.

## 12. Assumptions

| Assumption | Rationale / validation |
|---|---|
| Early users can authorize GitHub OAuth and accept a cloud execution workspace. | Validate during onboarding research; provide clear permission explanation. |
| Initial users work mostly on small-to-medium repositories and feature-sized tasks. | Enforce limits and measure failure/abandonment by repo size. |
| Users value reviewable artifacts over autonomous merging. | Measure export/open-diff behavior and trust score. |
| Repository conventions can be inferred sufficiently from manifests, config, and existing tests. | Show confidence and citations; invite corrections. |
| A single model provider/runtime can support MVP specialist roles. | Preserve role prompts and schemas so models can be swapped later. |

## 13. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---:|---:|---|
| Incorrect or insecure generated code | Medium | High | Approval gates, review agent, sandbox tests, sensitive-path policies, clear limitations. |
| Hallucinated repository understanding | Medium | High | Cite paths, expose confidence, re-index stale context, ask questions for ambiguity. |
| GitHub permission concerns | Medium | High | Least privilege, transparent scopes, encrypted tokens, easy disconnect/delete. |
| Long-running agents create user uncertainty | High | Medium | Milestone updates, elapsed time, cancel/retry, meaningful waiting states. |
| Cost and runaway execution | Medium | High | Token/time budgets, output caps, concurrency quotas, cancellation. |
| Tests depend on unavailable services | High | Medium | Detect prerequisites; label skipped/blocked distinctly from passed. |
| Scope creep toward autonomous SDLC | High | Medium | Strict MVP boundaries and MoSCoW review. |

## 14. Competitive Analysis

| Category | Examples | Strengths | CodePilot OS differentiation |
|---|---|---|---|
| AI coding assistants | GitHub Copilot, Cursor, Windsurf | Fast in-editor generation and chat | Project-level orchestration with visible role handoffs and approval gates. |
| Autonomous coding agents | Devin, OpenHands, SWE-agent | Long-horizon task execution | Transparent dashboard, artifact evidence, constrained human-supervised workflow. |
| Developer platforms | GitHub, Linear, Jira | Source/work tracking systems of record | Complements rather than replaces them; turns requests into engineering evidence. |
| AI review/testing tools | CodeRabbit, Codium-style test tools | Focused review or test automation | Connects planning, implementation, review, QA, docs, and evaluation in one run. |

The positioning must avoid claiming uniqueness of “agents.” The differentiator is an understandable operating model for supervision: plan first, explicit agents, evidence at every stage, and human authority over consequential changes.

## 15. User Journey

1. **Connect:** User signs in, reads GitHub permission explanation, connects GitHub, and selects a repository/default branch.
2. **Understand:** Repository analysis runs. User sees status, then reviews technologies, architecture map, conventions, and caveats.
3. **Request:** User submits “Add CSV export to the invoices page,” including expected behavior and constraints.
4. **Plan:** Planner and Architect produce a scoped plan, affected paths, questions, risks, and test approach.
5. **Approve:** User edits or approves the plan. Approval creates the immutable execution baseline.
6. **Execute:** Developer implements in isolated workspace; Reviewer and QA inspect changes; Documentation updates relevant material; Evaluator checks criteria.
7. **Supervise:** At any point user views live status, opens events, answers a question, cancels, or retries an eligible failed stage.
8. **Review:** User sees combined diff, test evidence, reviewer issues, and criteria score. High-severity findings demand a resolution decision.
9. **Export:** User exports an approved result to a branch/commit or patch, then continues review in their existing GitHub workflow.

## 16. Information Architecture

```text
CodePilot OS
├── Home / Projects
│   ├── Project list
│   └── Create/import project
├── Project workspace
│   ├── Overview (health, active runs, approvals, activity)
│   ├── Repository Intelligence (map, stack, conventions, analysis)
│   ├── Requests (draft, planned, running, completed)
│   ├── Runs (live dashboard, timeline, agents, artifacts)
│   ├── Changes (diffs, tests, findings, exports)
│   └── Settings (connection, limits, deletion)
└── Global
    ├── Notifications / action required
    └── Account
```

The primary navigation must preserve project context. A run deep-link opens to the live overview first, with tabs for plan, timeline, changes, tests, documentation, and evaluation. Empty states explain the next concrete action.

## 17. Feature Prioritization (MoSCoW)

| Must | Should | Could | Won’t for MVP |
|---|---|---|---|
| GitHub import; repository analysis; feature request; plan and approval; role-based agent workflow; isolated changes; diff; QA evidence; activity timeline; live dashboard; cancellation | Plan revision; rerun stage; branch/patch export; searchable history; documentation changes; basic notifications | User-configurable agent instructions; cost estimates; inline comments; multiple concurrent runs per project; lightweight collaboration | Autonomous merge/deploy; enterprise identity/admin; GitLab/Bitbucket; marketplace; mobile; custom self-hosted execution |

## 18. MVP Scope

### In scope

The MVP delivers the full supervised workflow for one GitHub repository at a time: OAuth connection; default-branch analysis; request creation; planner/architect output; approval; orchestrated developer/reviewer/QA/documentation/evaluator run; sandbox validation; reviewable artifacts; and a polished dashboard/timeline. The product will support common JavaScript/TypeScript and Python repositories first, with language detection for others shown as best effort.

### Explicit delivery slices

| Slice | Outcome | Exit criterion |
|---|---|---|
| Foundation | Auth, projects, GitHub connection, audit model | Import and secure project record work end-to-end. |
| Intelligence | Repository map and briefing | User can make a planning decision with cited context. |
| Planning | Request, plan, architecture review, approval | No write run begins without an approved revision. |
| Execution | Isolated developer workflow and artifacts | A supported repo produces a reviewable diff. |
| Quality | Reviewer, QA, docs, evaluator | Completion includes severity findings and criterion-by-criterion evidence. |
| Experience | Dashboard, timeline, errors, export | User can supervise and recover from common failure states. |

## 19. Post-MVP Roadmap

| Horizon | Capabilities | Decision trigger |
|---|---|---|
| Next | Pull-request creation, GitHub checks/statuses, collaboration comments, richer language support, user policies. | MVP completion and trust metrics meet targets. |
| Later | Organization workspaces, RBAC, SSO, audit export, private networking, managed secrets, spend controls. | Demonstrated team demand and security review. |
| Future | Continuous repository memory, proactive issue triage, dependency/security agents, release planning, multi-repository change coordination. | Reliable agent quality, policy maturity, and user consent model. |

## 20. Acceptance Criteria

The release is acceptable only when the following end-to-end scenarios pass in a staging environment using supported fixture repositories.

| Scenario | Acceptance criteria |
|---|---|
| First import | User connects GitHub, imports a supported repository, sees analysis progress, and receives a repository briefing with at least three source-backed facts. |
| Plan gate | User submits a request; plan includes all required sections; execution cannot start until current revision is approved. |
| Successful run | Approved request produces a run-specific workspace, visible agent transitions, a diff, test results, review findings, docs output, and evaluator score. |
| Blocking question | Missing requirement pauses execution, asks a clear question, and only resumes after recorded answer. |
| Test failure | Failed test displays command/status/evidence and is never represented as pass; run details remain reviewable. |
| Sensitive path | Proposed source modification to configured sensitive path is blocked before write and event appears in timeline. |
| Cancellation | User cancellation yields terminal cancelled status within 60 seconds and preserves prior artifacts. |
| Accessibility | Keyboard-only user can import, submit, approve, navigate run, and export; automated checks show no critical issues. |

## 21. Edge Cases

| Condition | Expected behavior |
|---|---|
| Empty repository | Complete import, explain insufficient context, permit request but require user-provided project setup before execution. |
| Monorepo | Display detected workspaces; user chooses target package/directory before planning. |
| Binary/generated/vendor files | Exclude by default from prompt context and modification unless user explicitly allows supported target. |
| No test framework detected | QA states no automated runner found, proposes test setup only after approval, and includes manual checks. |
| Existing uncommitted changes | Since cloud imports a remote SHA, show imported commit and explain that local changes are absent. |
| Branch changes during run | Pin run to imported SHA; flag export as potentially behind default branch and offer rebase/re-run guidance. |
| Rate limiting/network outage | Pause/retry bounded operations with visible retry time; preserve state and surface provider status. |
| Circular agent handoff | Enforce stage transition graph and retry limits; escalate to human after limit. |
| Conflicting agent edits | Serialize write stages or apply deterministic merge; conflict pauses run with paths and decision options. |
| Prompt injection in repository files | Treat repository content as untrusted data; never execute instructions embedded in code/docs without policy validation. |

## 22. Security Considerations

1. Use OAuth tokens with minimum GitHub scopes; encrypt tokens at rest using managed key services and rotate/revoke on disconnect.
2. Never include secrets, access tokens, environment variables, or raw credential files in model context, logs, downloadable artifacts, or UI. Scan common secret patterns before each prompt/artifact display.
3. Execute repository code only in ephemeral sandboxed containers with restricted network egress, CPU/memory/time quotas, non-root execution, and no host filesystem access.
4. Implement path allow/deny policies. Default deny `.env`, credential directories, private-key formats, CI secrets, and provider configuration that could cause external side effects.
5. Require user approval for write-capable execution and explicit export. Do not automatically push, merge, create releases, or call production APIs.
6. Maintain immutable audit records for auth changes, imports, approvals, agent transition, policy block, exports, and deletion requests.
7. Apply input validation, output encoding, CSRF protections, secure session handling, rate limits, dependency scanning, and vulnerability management according to the web application threat model.
8. Provide data deletion and repository-disconnect flows. Define retention duration before launch; remove cached repository snapshots and artifacts after approved deletion.

## 23. Accessibility Considerations

Target WCAG 2.2 AA for the MVP. Agent state may not rely on color or animation alone: pair status color with text, icon, and screen-reader label. Live updates use restrained ARIA live regions so they inform rather than interrupt. Every approval, cancel, retry, and diff navigation action is keyboard accessible with visible focus. The diff viewer must offer semantic line navigation, copyable text, adequate contrast, zoom resilience, and a non-visual summary of changed files/findings. Respect `prefers-reduced-motion`; never use countdown-only time limits for approvals.

## 24. Scalability Considerations

Separate interactive dashboard services from asynchronous analysis and execution workers. Use a durable job queue and event stream so worker restarts do not lose runs. Store repository snapshots and artifacts in object storage keyed by project/run and maintain metadata in a transactional database. Horizontally scale stateless API/UI processes; autoscale isolated workers by queue depth and enforce per-user/project concurrency quotas. Backpressure should queue rather than overload model or sandbox services, showing an honest expected state. Establish lifecycle policies for logs/artifacts, and design event schemas for pagination so long histories do not degrade live views.

## 25. Future AI Capabilities

Future capabilities are conditional on clear consent, evaluation quality, and security controls:

| Capability | User value | Guardrail |
|---|---|---|
| Persistent architectural memory | Reduces repeated repository discovery. | Versioned, source-cited memory with expiration and user correction. |
| Issue triage agent | Converts issues into ranked, clarified work. | No execution without request owner approval. |
| Dependency/security agent | Finds vulnerable or stale dependencies. | Evidence from trusted advisories; no automatic upgrades. |
| Release agent | Builds release notes and rollout checklists. | Human approval; deployment remains external until policy matures. |
| Learning from feedback | Improves plans and review precision. | Opt-in data use, privacy controls, and regression evaluation. |
| Cross-repository coordinator | Plans changes across services. | Explicit repo authorization and dependency visualization. |

## 26. KPIs

| KPI | Why it matters | Cadence / owner |
|---|---|---|
| Weekly activated projects | Measures meaningful adoption rather than signups. | Weekly / Product |
| Requests per activated project | Measures workflow pull. | Weekly / Product |
| Approved-plan-to-export conversion | Measures end-to-end value. | Weekly / Product + Engineering |
| Median execution duration | Measures experience and capacity health. | Daily / Engineering |
| Validation and reviewer-blocker rates | Measures output quality and safety. | Weekly / AI Quality |
| Clarification rate | Indicates request UX and planning quality. | Weekly / Product |
| Cancellation/retry rate | Signals trust, reliability, or scope mismatch. | Weekly / Engineering |
| Cost per completed run | Protects sustainable unit economics. | Weekly / Platform |
| Security policy block rate | Detects risk patterns and false positives. | Weekly / Security |
| Accessibility defect escape rate | Measures inclusive quality. | Release / Design + QA |

## 27. Open Questions

| Question | Owner | Decision needed by |
|---|---|---|
| What exact GitHub OAuth scopes are required for read-only import versus branch export? | Security + Platform | Before auth implementation |
| Will the MVP create a remote branch, a commit in an app-managed fork, or only a downloadable patch? | Product + Platform | Before execution slice |
| Which test commands may run automatically, and how are dangerous scripts detected? | Security + DevOps | Before sandbox launch |
| What are the supported repository-size and language limits advertised in onboarding? | Engineering + Product | Before beta |
| How are user-supplied plans distinguished from agent-generated statements in audit/export views? | Design + Product | Before planning slice |
| What retention period applies to code snapshots, logs, prompts, and artifacts? | Legal + Security | Before external users |
| Is model-provider data retention opt-out required for target users? | Legal + AI Platform | Before external users |
| What feedback mechanism best captures reviewer acceptance after export? | Product | Before beta instrumentation |

## 28. Appendix

### A. Run state model

```text
Draft request → Planning → Awaiting plan approval → Queued → Running
                                     │                         │
                                     └──── Rework ─────────────┤
                                                               ├→ Awaiting clarification → Running
                                                               ├→ Failed → Retry queued
                                                               ├→ Cancelled
                                                               └→ Review ready → Exported / Closed
```

`Review ready` requires developer output plus Reviewer, QA, Documentation, and Evaluator terminal artifacts. A run may be review-ready with failed tests only when the failure is explicitly recorded; it must never be presented as fully validated.

### B. Core entities

| Entity | Key fields |
|---|---|
| User | ID, profile, GitHub connection status, preferences |
| Project | ID, repository identity, default branch/SHA, analysis state, policy configuration |
| Repository analysis | Snapshot SHA, detected stack, map, summary, citations, timestamp, confidence |
| Request | Title, outcome, constraints, criteria, status, creator |
| Plan revision | Structured plan, assumptions, scope, risk, agent assignments, author, approval metadata |
| Run | Immutable baseline references, state, timestamps, budget, workspace/branch reference, terminal reason |
| Agent stage | Role, state, input/output references, retries, timings, error category |
| Artifact | Diff, test result, finding, documentation output, evaluation, sanitized log |
| Audit event | Actor, action, target, timestamp, correlation ID, metadata |

### C. Severity definitions

| Severity | Meaning | Default handling |
|---|---|---|
| Blocker | Likely security, data-loss, or inability-to-use defect. | Prevent final completion until resolved/waived with rationale. |
| High | Material regression or incorrect core behavior. | Require explicit user decision before export. |
| Medium | Important quality/edge-case concern. | Visible in review; export allowed with acknowledgment. |
| Low | Minor maintainability, consistency, or non-critical concern. | Informational review action. |
| Informational | Observation or suggested improvement. | No gate. |

### D. Terminology

- **Agent:** A named specialist role with defined input, output, and permissions.
- **Artifact:** Persisted evidence produced by a stage, such as a diff, finding, or test result.
- **Execution baseline:** The approved plan revision and repository commit SHA a run is bound to.
- **Run:** One orchestration attempt for an approved request.
- **Write-capable work:** Any operation that changes a run workspace, branch, test file, or documentation artifact.

