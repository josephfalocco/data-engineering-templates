# Phase 1: Discovery Templates

## Purpose
Phase 1 happens before you touch any data. This is where you understand the business problem, define scope, and set expectations. Skipping this phase is why most data projects fail.

## What You're Trying to Answer

| Question | Why It Matters |
|----------|----------------|
| What problem are we solving? | Prevents building the wrong thing |
| Who needs this data? | Identifies stakeholders and their requirements |
| What decisions will this support? | Shapes what data you actually need |
| What does success look like? | Defines how you'll know when you're done |
| What's out of scope? | Prevents scope creep |

## The Process

### Step 1: Stakeholder Interview
Meet with the person who needs this data/report/dashboard. Use `requirements_template.md` to guide the conversation.

**Key questions:**
- What problem are you trying to solve?
- What decisions will this help you make?
- How do you do this today? (manual process, spreadsheets, etc.)
- What's painful about the current process?
- How often do you need this refreshed?
- Who else uses this data?

### Step 2: Document Requirements
Fill out `requirements_template.md` based on the interview. Get stakeholder sign-off before proceeding.

### Step 3: Define Scope
Create the project charter using `project_charter_template.md`. This becomes your contract — anything not in scope requires a separate conversation.

### Step 4: Identify Data Sources
List every system/file/database that might contain relevant data. You'll explore these in Phase 2.

| Source | Owner | Access Method | Notes |
|--------|-------|---------------|-------|
| [System name] | [Who owns it] | [API/CSV/Database] | [Any known issues] |

### Step 5: Get Sign-Off
Review the project charter with stakeholders. Confirm:
- [ ] Requirements accurately captured
- [ ] Scope is agreed upon
- [ ] Timeline is realistic
- [ ] Success criteria are clear

## Deliverables Checklist

Before moving to Phase 2, you should have:

- [ ] Completed requirements document
- [ ] Project charter (signed off by stakeholder)
- [ ] List of data sources to explore
- [ ] Clear understanding of what reports/outputs are needed
- [ ] Defined what's OUT of scope

## Templates in This Folder

| File | Purpose |
|------|---------|
| `requirements_template.md` | Interview guide + requirements documentation |
| `project_charter_template.md` | One-page project scope and summary |

## Common Mistakes to Avoid

1. **Jumping straight to data** — You'll build the wrong thing
2. **Vague requirements** — "I need a dashboard" is not a requirement
3. **No scope boundaries** — Everything becomes urgent and in-scope
4. **Skipping sign-off** — Stakeholder claims "that's not what I asked for"
5. **Assuming you know the business** — Ask dumb questions anyway

## Time Investment

| Project Size | Phase 1 Duration |
|--------------|------------------|
| Small (1 source, 1 report) | 1-2 hours |
| Medium (2-3 sources, multiple reports) | 1-2 days |
| Large (enterprise, multiple stakeholders) | 1-2 weeks |

Phase 1 is never wasted time. It's the cheapest place to find problems.
