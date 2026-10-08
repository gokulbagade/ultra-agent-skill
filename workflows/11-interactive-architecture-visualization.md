# 🗺️ Agentic Workflow 11: Interactive Architecture Visualization (Archify)

> **Purpose:** Turn system descriptions, codebases, and Mermaid diagrams into interactive standalone HTML diagrams with inline SVG, dark/light themes, and export capabilities.

---

## 📋 Prerequisites
- Node.js runtime installed.
- System description, codebase structure, or Mermaid diagram source available.
- Reference CLI script available (`skills/ultra-skill/references/archify/bin/archify.mjs`).

---

## 🧭 Workflow State Machine

```mermaid
graph TD
    A["Request: System Description / Repo / Mermaid"] --> B["1. Type Selection (5 Diagram Modes)"]
    B --> C["2. Source Evidence Tracing (For Codebases)"]
    C --> D["3. Author Candidate JSON"]
    D --> E["4. Archify Finalize CLI Validation"]
    E --> F{"Gates Passed?"}
    F -->|"Failed Layout / Schema"| G["Repair Geometry & Rerun Finalize"]
    G --> E
    F -->|"Passed"| H["5. Deliver Standalone Interactive HTML"]
```

---

## Step-by-Step Execution

### Step 1: Type Selection
Classify the visual intent into one of the 5 Archify types:
- **`architecture`**: Components, services, containers, databases, cloud & security boundaries.
- **`workflow`**: Step-by-step processes, approval gates, agent tool execution paths, CI/CD runbooks.
- **`sequence`**: API call chains, request/response lifecycles, async message traces between participants.
- **`dataflow`**: Pipelines, ETL/ELT flows, data lineage, producer-consumer networks.
- **`lifecycle`**: State machines, lifecycle transitions, retry states, terminal outcomes.

### Step 2: Mermaid Conversion (If User Provided Mermaid)
- `flowchart` / `graph` → `workflow` (or `architecture` for infrastructure).
- `sequenceDiagram` → `sequence` (messages, async replies, participants).
- `stateDiagram` → `lifecycle` (states, transitions, guard conditions).
*Extract semantics and topology; do not mechanically copy Mermaid's flat styling.*

### Step 3: Author Candidate JSON
Create `.archify/<type>-<slug>-<timestamp>/candidate.json`:
- Structure nodes with clear labels, semantic icons, and boundary groupings.
- Link relationships with explicit directional flows (`from` → `to`).
- Set `meta.quality_profile` to `"showcase"`.
- For real codebases, attach source evidence pointers (`file` and line references).

### Step 4: Finalize CLI Validation
Run the Archify validation and packaging command:
```bash
node skills/ultra-skill/references/archify/bin/archify.mjs finalize <type> <candidate.json> <output.html> --quality showcase --json
```

### Step 5: Verification Gate & Delivery
- Confirm exit code `0`.
- The generated `<output.html>` is completely self-contained with:
  - Dark/Light theme toggle
  - Pan & zoom controls
  - Interactive click-to-highlight node connectivity
  - Export to SVG, PNG, WebP, and WebM

---

## 🔗 Related Workflows
- **Prerequisite / Topology:** [Workflow 01: Agent Graph Orchestration](01-agent-graph-orchestration.md)
- **Asset Production:** [Workflow 09: Brand Asset Production](09-brand-asset-production.md)
- **Planning:** [Workflow 12: Implementation Planning & Checklists](12-implementation-planning-and-checklists.md)
- **Gate Enforcement:** [Workflow 10: Gate-Function Verification](10-gate-function-verification.md)
