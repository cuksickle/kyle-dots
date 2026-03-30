---
name: curriculum-builder
description: >
  Build biology curriculum modules (lessons, handouts, exit tickets, assessments) from the master spec.
  Use when the user asks to build, create, generate, or write biology lessons, modules, curriculum content,
  exit tickets, transfer tasks, handouts, or assessments. Also use for fixing, auditing, or quality-checking
  existing curriculum modules. Triggers on: "build module", "create lesson", "generate exit ticket",
  "write handout", "curriculum", "M01" through "M12", "E01" through "E06", "5E lesson", "NGSS alignment".
---

# Curriculum Builder — Subagent Orchestration Guide

Build 9th grade biology curriculum modules from `Work/Biology/BIOLOGY_CURRICULUM_OVERHAUL.md`.

**Master spec:** `Work/Biology/BIOLOGY_CURRICULUM_OVERHAUL.md`
**Modules dir:** `Work/Biology/modules/`
**Quality references:** `modules/M07-arms-race/` (best lessons), `modules/M06-rewriting-life/` (post-review fixes)
**Handoff context:** `Work/Biology/HANDOFF-NEXT-AGENT.md` — read this first for project state

---

## Critical Rules (Memorize These)

1. **Handouts FIRST, overview LAST.** Never write a lesson referencing a handout that doesn't exist yet.
2. **No placeholders.** Every `[[path/file]]` link must resolve to an actual file with real content.
3. **Verify all claims.** No hallucinated studies, URLs, or statistics. Use @librarian for verification.
4. **53-minute periods.** All section timings must sum to ≤53 min.
5. **Answer keys required.** Every exit ticket needs questions AND answers with point values.
6. **Real URLs only.** No `https://example.com` — find actual videos, articles, papers.

---

## Phase 1: Research (Dispatch @librarian + @explorer)

Before writing ANY content, gather real-world materials.

### 1a. Read the spec
- Read `BIOLOGY_CURRICULUM_OVERHAUL.md` for the target module's phenomena, NGSS standards, lesson count, and notes
- Read `HANDOFF-NEXT-AGENT.md` section 8 for the module's build order and status

### 1b. Research (parallel dispatch)
- **@librarian:** Find real studies, papers, datasets related to the module's phenomena. Verify scientific claims. Find actual journal citations (author, year, journal, DOI if possible).
- **@explorer:** Search the vault for existing legacy materials in `_legacy_source/`. Find any related handouts, datasets, or resources already created.

### 1c. Video resources
Find 2-4 real video URLs per module from:
- HHMI BioInteractive (biointeractive.org)
- Amoeba Sisters (YouTube)
- Crash Course Biology (YouTube)
- Nature Video (YouTube)
- World Science Festival (YouTube)

**Record actual URLs — verify they load before including them.**

### 1d. Module Brief
Create a mental (or written) Module Brief before building:
- Lesson sequence with phenomena for each
- Activities planned (physical/digital/cognitive/creative)
- Handouts needed (list every file that will be referenced)
- Standards mapping (which NGSS standard appears in which lesson)

---

## Phase 2: Build (Dispatch @fixer for parallel work)

Build in this EXACT order. Do not skip or reorder.

### Step 1: Handouts (parallel @fixer dispatch OK)
Create ALL handouts BEFORE any lesson that references them.

**Handout quality bar:**
- Actual content, not stubs — real data, real sequences, real descriptions
- If a handout contains data tables, fill them with real data
- If it contains diagrams, describe them with enough detail to be useful
- File naming: `resources/handouts/{descriptive-filename}.md`

**Parallelization:** If 3+ handouts are independent, dispatch multiple @fixers simultaneously.

### Step 2: Lessons (L01 → L{N}, sequential)
Each lesson MUST contain:
- Learning objective (1 sentence, measurable)
- Phenomenon/hook (engaging, real-world, ≤3 sentences)
- Materials checklist
- Agenda with 5E timing: OPEN/EXPLORE/EXPLAIN/ELABORATE/CLOSE
- At least 2 interactivity tiers (physical/digital/cognitive/creative)
- Differentiation table (Support | Extension)
- Assessment section (formative + exit ticket reference)
- Teacher Notes (common errors, prep warnings, pacing tips)
- All timings sum to ≤53 min

**Reference these for quality:**
- `modules/M07-arms-race/lessons/L01.md` — simulation-based, physical interactivity
- `modules/M07-arms-race/lessons/L04.md` — lab with real data
- `modules/M06-rewriting-life/lessons/L01.md` — hands-on paper model
- `modules/M06-rewriting-life/lessons/L04.md` — case study jigsaw

### Step 3: Exit Tickets (parallel @fixer dispatch OK)
One per lesson. Each MUST have:
- 2-3 questions aligned to the learning objective
- Complete answer key with point values
- Mix of question types (recall + application)

**Template:** `modules/_templates/exit-ticket-template.md`

### Step 4: Transfer Task
Pick Your Path format with 3 options (Write/Design/Debate). Include CER rubric.

**Template:** `modules/_templates/transfer-task-template.md`

### Step 5: Summative Assessment (optional but recommended)
10 multiple choice + 15 short answer. Include answer key.

### Step 6: Overview (ALWAYS LAST)
Written after ALL content exists so all references are real. Must include:
- Module summary
- Lesson sequence table
- NGSS standards alignment table
- Complete materials list (aggregated from all lessons)
- Common misconceptions for the topic
- Teacher notes and prep timeline
- Links to all handouts, exit tickets, assessments

---

## Phase 3: Quality Gate (Run Before Declaring Done)

Execute ALL checks. Do not skip any.

### Automated checks
```bash
# URL verification
bash modules/_templates/verify-urls.sh modules/M{NN}-{slug}/
```

### Manual checklist
- [ ] **URL check:** Every link loads and matches described content
- [ ] **Claim check:** Every study name, date, journal, statistic is verified
- [ ] **Cross-reference check:** Every `[[path/file]]` resolves to an actual file
- [ ] **Timing check:** All section timings sum to ≤53 min per lesson
- [ ] **Interactivity audit:** Every lesson has ≥2 interactivity tiers
- [ ] **Misconception check:** Overview addresses common misconceptions
- [ ] **NGSS alignment:** Every listed standard appears in at least one lesson
- [ ] **Answer keys:** Every exit ticket and assessment has complete answer keys
- [ ] **Handout existence:** Every referenced handout file actually exists with content

**Reference:** `modules/_templates/VERIFICATION-CHECKLIST.md` for detailed verification steps

---

## M06 Gap Warnings (Do Not Repeat These Mistakes)

| Gap | Prevention |
|-----|-----------|
| Handouts didn't exist | Build handouts FIRST, before any lesson |
| No video URLs | Research real videos in Phase 1, include actual links |
| Missing answer key | Write answer key immediately after exit ticket questions |
| No actual data for simulations | Include real sequences/data, not descriptions of them |
| Unverified scientific claims | @librarian verifies every study citation before inclusion |
| No summative assessment | Include in build plan, create in Step 5 |
| Unclear lesson transitions | Add homework/bridge activities between lessons |
| No prep timeline | Calculate prep time in overview (Step 6) |

---

## File Structure & Naming Conventions

Every module follows this structure:
```
modules/M{NN}-{slug}/
├── overview.md
├── lessons/
│   ├── L01.md
│   └── ...
├── assessments/
│   ├── exit-tickets/
│   │   ├── L01-exit-ticket.md
│   │   └── ...
│   ├── transfer-task.md
│   └── summative-assessment.md
└── resources/
    ├── handouts/
    │   ├── M{NN}-L{XX}-{descriptive-slug}.md
    │   └── ...
    └── slides/
```

### Handout Naming Rule
**Every handout MUST follow this pattern:** `M{NN}-L{XX}-{descriptive-slug}.md`
- `M{NN}` = module number (e.g., `M08`)
- `L{XX}` = lesson number that primarily uses it (e.g., `L01`, `L03`)
- `{descriptive-slug}` = lowercase-hyphenated description (e.g., `fossil-timeline-cards`)

**Examples:**
- `M08-L01-fossil-timeline-cards.md` ✅
- `M08-L03-cytochrome-c-sequences.md` ✅
- `M08-L05-evidence-case-file.md` ✅
- `fossil-formation-steps.md` ❌ (missing module/lesson prefix)
- `handout1.md` ❌ (not descriptive)

**Module-wide handouts** (used across multiple lessons) use `L01` as default:
- `M08-L01-evidence-graphic-organizer.md` ✅

### Cross-Reference Rule
All `[[path/file]]` links in lessons MUST use the same filename as the actual file. Before writing a lesson, confirm handout filenames. After building, run the cross-reference check:
```bash
rg -o '\[\[([^\]]+)\]\]' -r '$1' modules/M{NN}-{slug}/lessons/ --no-filename | sort -u | while read ref; do
  path="modules/M{NN}-{slug}/${ref}.md"
  [ -f "$path" ] && echo "✅ $ref" || echo "❌ $ref — MISSING"
done
```

---

## Subagent Dispatch Summary

| Phase | Task | Agent | Parallelizable? |
|-------|------|-------|-----------------|
| 1 | Research studies/papers | @librarian | Yes (with @explorer) |
| 1 | Find legacy materials | @explorer | Yes (with @librarian) |
| 2 | Create handouts | @fixer | Yes (3+ independent) |
| 2 | Write lessons | Self (orchestrator) | No (sequential) |
| 2 | Create exit tickets | @fixer | Yes (3+ independent) |
| 2 | Write transfer task | Self or @fixer | No |
| 2 | Write overview | Self (orchestrator) | No (always last) |
| 3 | Run URL verification | Self (bash) | — |
| 3 | Verify claims | @librarian | — |

---

## Teacher Context (Don't Ask Again)

- **Period length:** 53 minutes
- **Has codon charts** — don't create generic ones
- **Lab setup:** Microscopes, hot plates, full lab equipment
- **Devices:** Chromebooks + Google Classroom
- **Class:** 9th grade intro biology
