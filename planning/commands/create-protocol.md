# Create Fitness Protocol(s)

## Topic/reference: $ARGUMENTS

Create concise, constraint-based protocol file(s) for multi-agent planning systems. Input can be:
- **Topic(s)**: `"VO2 max training"` or `["threshold training", "zone 2", "tempo runs"]`
- **Knowledge file**: Path to extract protocol from (e.g., `knowledge/aerobic-training.md`)
- **Mixed**: Topic with category hint: `"Yin yoga (Movement Practice)"`

## Protocol Types

**1. Training Stimulus** (VO2 max, strength, threshold)
- Recovery costs, interference effects, trade-offs
- Template A: 80-100 lines

**2. Movement Practice** (yoga, stretching, mobility)
- Purpose-driven, integration contexts
- Template B: 50-65 lines

**3. Exercise Progression** (goblet → back squat)
- Readiness criteria, progression paths
- Template C: 60-70 lines

**4. Injury Prevention/Rehab** (knee health, shoulder prehab)
- Contraindications, dosage ranges, warning signs
- Template D: 65-75 lines

## Execution Process

### Step 1: Parse Input

**If knowledge file provided:**
```bash
# Read the knowledge file
cat $ARGUMENTS
```
- Extract distinct protocol topics from content
- Identify category for each (Training/Movement/Progression/Injury)
- List protocols to create

**If topic(s) provided:**
- Parse single topic or list
- Classify each into category (A/B/C/D)
- Check if any protocols already exist in `planning/protocols/`

**Output:**
```
Analyzing input: [input type]
Protocols to create:
1. [protocol-name] → Category: [type] (Template [A/B/C/D])
2. [protocol-name] → Category: [type] (Template [A/B/C/D])

Existing protocols to skip: [list if any]
```

### Step 2: Research Phase (Per Protocol)

**Universal research** (all):
1. Mechanism/purpose - What does this address? Why?
2. Application contexts - When relevant? What conditions?
3. Practical guidance - How applied? Key parameters?
4. Boundaries - When NOT appropriate? Contraindications?
5. Common errors - What goes wrong? Why?

**Category-specific research:**

**Training Stimulus** (add):
- Time windows (adapt time, plateau point)
- Recovery cost (CNS/cardiac/muscular/systemic)
- Interference effects (conflicts with other training)
- Trade-off surfaces (gains vs losses when combined)

**Movement Practice** (add):
- Purpose hierarchy (what goals served)
- Integration contexts (fits with training how)
- Frequency/dosage guidelines

**Exercise Progression** (add):
- Readiness criteria (when progress)
- Regression options (when step back)
- Load/complexity scaling

**Injury/Rehab** (add):
- Contraindications (red flags)
- Dosage ranges (safe parameters)
- Warning signs (when stop)

**Research sources:**
- WebSearch for exercise science, meta-analyses
- Exercise physiology mechanisms
- Clinical practice guidelines (injury/rehab)
- Strength & conditioning research

**Output per protocol:**
```
Researching: [protocol-name]
✓ Core mechanism identified: [1-sentence summary]
✓ Application contexts defined
✓ Practical guidance extracted
✓ Boundaries/contraindications identified
✓ Category-specific elements: [list]
```

### Step 3: Synthesis (Per Protocol)

Extract from research into structure:

**REQUIRED** (all):
1. Purpose/Mechanism (1-2 paragraphs)
2. Application (5-10 lines: when/how/frequency/variants)
3. Boundaries (3-5 bullets: when NOT)
4. Common Errors (3-5 errors with mechanism)
5. Application Logic (decision tree OR checklist)

**OPTIONAL** (category-specific):
- **Training Stimulus**: Adaptation timeline, recovery cost, integration constraints, trade-offs, priority hierarchy
- **Movement Practice**: Purpose hierarchy, integration contexts, dosage guidelines
- **Exercise Progression**: Readiness/progression/regression criteria
- **Injury/Rehab**: Contraindications, dosage ranges, warning signs

### Step 4: Write Protocol

Select template based on category and write protocol.

**Template A: Training Stimulus** (80-100 lines)
```markdown
# [Protocol Name]

## Core Mechanism
[1 paragraph: what adapts, why, key constraints]

**Adaptation timeline:**
- [% gains by week X]
- [Plateau point]
- [Maintenance dose]

**Minimum effective dose:** [floor constraint]

## Prescription
**When to apply:** [3-4 conditions]

**Standard format:** [workout with numbers]
- **Key parameters**: [values/ranges]
- **Variants**: [alternatives]

**Context modifiers:** [4-6 modifications]

**Recovery cost:** [High/Moderate/Low - relative to baseline]
- CNS/Cardiac/Muscular/Systemic: [Low/Moderate/High/Maximal]

**Integration constraints:**
- **Requires**: [prerequisites]
- **Spacing**: [time separation]
- **Interference**: [quantified effects]
- **Compatible**: [what works together]

## Boundaries & Trade-offs
**Skip if:** [3-5 exclusion criteria]

**Trade-off surface:** [X vs Y: +A%, -B%] × 3-4

**Priority hierarchy:** [ordered list]

## Common Errors
**"[Error]"** - [mechanism explanation] × 3-5

## Application Logic
[binary decision tree, 8-10 lines]
```

**Template B: Movement Practice** (50-65 lines)
```markdown
# [Protocol Name]

## Purpose
[1-2 paragraphs: what addresses, mechanisms, when valuable]

## Application
**Primary goals:**
- [Goal 1] - [why serves it]
- [Goal 2] - [why serves it]

**When to apply:** [2-3 contexts]

**How to apply:**
- **Duration**: [range]
- **Frequency**: [guideline]
- **Intensity**: [guidance]

**Integration contexts:**
- **[Phase 1]**: [how fits]
- **[Phase 2]**: [how fits]

## Boundaries
**Skip if:** [3-5 conditions]

**Lower priority than:** [what takes precedence]

## Common Errors
**"[Error]"** - [why wrong, how correct] × 3-4

## Application Checklist
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

**Template C: Exercise Progression** (60-70 lines)
```markdown
# [Protocol Name]

## Purpose
[1 paragraph: movement pattern, why progression matters]

## Progression Path
**Stage 1**: [exercise]
- Readiness: [criteria]
- Load range: [parameters]

**Stage 2**: [exercise]
- Readiness: [criteria]
- Load range: [parameters]

[Continue as needed]

## Readiness Criteria
**Progress when:** [3-4 criteria]

**Regress when:** [2-3 warning signs]

## Common Errors
**"[Error]"** - [why problematic, correct] × 3-4

## Application Logic
[flowchart: stage → check → progress/maintain/regress]
```

**Template D: Injury Prevention/Rehab** (65-75 lines)
```markdown
# [Protocol Name]

## Purpose
[1-2 paragraphs: addresses what, mechanisms, why important]

## Application
**When to apply:** [2-3 conditions]

**How to apply:**
- **Exercises**: [list with sets/reps/load]
- **Frequency**: [guideline]
- **Progression**: [how advance]

**Dosage ranges:**
- **Volume/Intensity/Frequency**: [safe ranges]

## Contraindications
**Do NOT apply if:** [3-4 red flags]

**Warning signs:** [2-3 signs to stop/modify]

## Integration with Training
**Sequencing:** [when in session/week]

**Compatible with:** [what training]

**Reduce if:** [conditions]

## Common Errors
**"[Error]"** - [why problematic, correct] × 3-4

## Application Checklist
- [ ] No contraindications
- [ ] Dosage safe
- [ ] [Other criteria]
```

**Writing rules:**
- **Numbers over words**: "3-8 min" not "three to eight"
- **Dense bullets**: One line per point
- **No beginner content**: Assume intermediate+ fitness
- **No references**: Agents don't need citations
- **Quantify**: Percentages, ratios, time scales
- **Mechanism-first**: Explain why

### Step 5: Validate

**Universal checks:**
- [ ] All REQUIRED components present
- [ ] Length within target (40-100 lines)
- [ ] Purpose/mechanism clear
- [ ] Application specific
- [ ] Boundaries explicit
- [ ] Errors explain mechanism
- [ ] Application logic scannable (< 30 sec)

**Category-specific checks:**

**Training Stimulus:**
- [ ] Adaptation timeline quantified
- [ ] Recovery cost by system
- [ ] Integration constraints explicit
- [ ] Trade-offs quantified
- [ ] Priority hierarchy ordered

**Movement Practice:**
- [ ] Purpose hierarchy clear
- [ ] Integration contexts identified
- [ ] Dosage guidelines specific

**Exercise Progression:**
- [ ] Readiness criteria clear
- [ ] Progression path complete
- [ ] Regression criteria identified

**Injury/Rehab:**
- [ ] Contraindications detailed
- [ ] Dosage ranges safe
- [ ] Warning signs clear
- [ ] Integration addressed

**Batch checks** (if multiple):
- [ ] Cross-references identified
- [ ] Priority hierarchy across batch
- [ ] Consistent terminology
- [ ] No duplication
- [ ] Each stands alone

### Step 6: Save Protocol(s)

**Single protocol:**
```bash
# Save to planning/protocols/
cat > planning/protocols/[topic-name].md
```

**Output:**
```
✓ Protocol created: [protocol-name].md
Domain: [domain covered]
Category: [Training Stimulus/Movement Practice/Exercise Progression/Injury Prevention]
Length: [X lines]
Recovery cost: [if Training Stimulus]
Integration constraints: [list related protocols]
```

**Multiple protocols:**

For each protocol:
1. Complete research → synthesis → write → validate
2. Save to `planning/protocols/[name].md`
3. Output summary
4. Continue to next

**Batch summary:**
```
Batch complete: [N] protocols created

Created:
1. [name].md ([category], [X lines])
2. [name].md ([category], [X lines])

Cross-references:
- [p1] ↔ [p2]: [relationship]

Priority hierarchy:
1. [Protocol] - [why first]
2. [Protocol] - [why second]

Agents that should use:
- program-creator: [protocols]
- week-planner: [protocols]
- workout-creator: [protocols]
```

## Examples

**Single topic:**
```
/create-protocol "threshold training"
```

**Multiple topics:**
```
/create-protocol ["zone 2", "threshold", "tempo runs"]
```

**From knowledge file:**
```
/create-protocol knowledge/aerobic-zones.md
```

**With category hint:**
```
/create-protocol "Yin yoga (Movement Practice)"
```

## Reference Example

See `planning/protocols/vo2max-development.md` for ideal Training Stimulus protocol:
- 88 lines (concise)
- Core mechanism explains cardiac window (3-8 min) + mitochondrial volume (12-20 min)
- Adaptation timeline: 60% gains by week 4, 95% by week 12
- Recovery cost quantified by system
- Integration constraints explicit (-15% strength interference)
- Trade-off surface quantified (+10% gains, +50% injury risk @ 2x/week)
- Priority hierarchy clear
- Errors mechanism-based
- **Includes protocol application checklist** (see below)

---

## Protocol Application Checklist (Required)

**Every protocol MUST include either an Application Checklist OR Application Logic decision tree to help agents apply the protocol correctly.**

### Checklist Format (for Movement Practice & Injury/Rehab)

Use when the protocol has prerequisites and safety checks that must ALL be verified:

```markdown
## Protocol Application Checklist

When programming [protocol name], verify:

- [ ] [Prerequisite 1 - what must be true before using]
- [ ] [Prerequisite 2 - base capability or training state]
- [ ] [Safety check 1 - contraindication ruled out]
- [ ] [Safety check 2 - dosage appropriate]
- [ ] [Integration check 1 - spacing from other training]
- [ ] [Integration check 2 - recovery adequate]
- [ ] (if concurrent training) [Specific interference consideration]
- [ ] (if same-day unavoidable) [Sequencing rule]
- [ ] Common errors avoided (see section above)
```

**Example from vo2max-development.md:**

```markdown
## Protocol Application Checklist

When programming VO2 max work, verify:

- [ ] Aerobic base established (minimum 8 weeks Zone 2 training)
- [ ] Interval structure specified (3-8min work intervals @ 90-100% max HR)
- [ ] Total work time appropriate (12-20min high-intensity volume)
- [ ] Frequency limited to 1-2x/week maximum
- [ ] Recovery between intervals adequate (3-4min active recovery)
- [ ] Zone 2 training maintained (2:1 ratio, Zone 2:VO2max volume)
- [ ] (if concurrent training) Separated from heavy lower body strength by 48-72hr
- [ ] (if same-day unavoidable) Strength scheduled first
- [ ] Common errors avoided (see section above)
```

### Decision Tree Format (for Training Stimulus)

Use when the protocol has branching logic based on goals, training state, or context:

```markdown
## Application Logic
```
[Goal/context question]?
├─ [Condition A] → [Action A + parameters]
├─ [Condition B] → [Action B + parameters]
├─ [Condition C] → [Action C + parameters]
└─ [Condition D] → [Action D + parameters]

[Secondary question]?
├─ [Condition X] → [Modification X]
├─ [Condition Y] → [Modification Y]
└─ [Condition Z] → [Modification Z]
```
```

**Example from greasing-the-groove.md:**

```markdown
## Application Logic
```
Primary goal?
├─ Hypertrophy → Skip GTG (insufficient tension), snacks OK if >6h from sessions, NEAT always
├─ Max strength → GTG compatible (neural focus), snacks low priority, NEAT always
├─ Skill development (pull-ups, handstands) → GTG primary tool, snacks optional, NEAT always
├─ General fitness → All three compatible, prioritize adherence
└─ Maintenance → Snacks primary (91% adherence), GTG optional, NEAT always

Current training phase?
├─ Accumulation/Volume → GTG low volume (3-5 sets), snacks moderate, NEAT always
├─ Intensification → GTG compatible, snacks reduce intensity, NEAT always
├─ Taper → NEAT only, skip GTG and vigorous snacks
└─ Deload → Snacks at low intensity, GTG reduced volume (2-3 sets), NEAT always
```
```

### When to Use Which Format

**Use Checklist when:**

- Protocol has clear prerequisites (must establish base before progressing)
- Safety checks are critical (contraindications, dosage limits)
- All items must be verified (AND logic, not branching OR logic)
- Common in: Movement Practice, Injury/Rehab, Exercise Progression protocols

**Use Decision Tree when:**

- Protocol application varies by goal, training state, or context
- Multiple valid paths exist (different approaches for different situations)
- Agents need to select appropriate variant (branching logic)
- Common in: Training Stimulus, Complex integration protocols

**Both formats should:**

- Be scannable in <30 seconds
- Include specific parameters (not vague "adequate" - use "3-4min recovery")
- Reference conditional logic (if concurrent training, if same-day, if injury present)
- Direct agent to avoid common errors
- Enable agent to apply protocol without ambiguity

## Key Principles

**Training Stimulus** protocols enable constraint satisfaction:
- Recovery cost → budget limited capacity
- Integration constraints → identify dependencies/conflicts
- Trade-off surfaces → rational compromises
- Priority hierarchies → conflict resolution
- Adaptation timelines → optimal block scheduling

**Movement Practice** protocols enable context selection:
- Purpose hierarchy → what goals served
- Integration contexts → fits with training phases
- Dosage guidelines → frequency/duration/intensity

**Exercise Progression** protocols enable skill development:
- Readiness criteria → objective thresholds
- Bidirectional paths → progress AND regress
- Load/complexity scaling → parameters per stage
- Safety gates → prevent premature progression

**Injury/Rehab** protocols enable safe application:
- Contraindications → red flags prevent use
- Dosage ranges → safe parameters
- Warning signs → early detection
- Integration guidance → program alongside training

## Quality Standards

**Assume intermediate+ fitness** - no beginner adaptations
**Concise** - every sentence earns its place
**Mechanism-first** - explain why, not just what
**Quantified** - use numbers (%, ratios, time scales)
**Actionable** - agents can apply without ambiguity

Target: 40-100 lines depending on category
Scan time: < 60 seconds to grasp everything
Density: No fluff, no obvious advice

## Output Location

All protocols saved to: `planning/protocols/[protocol-name].md`

Filename format: `lowercase-with-hyphens.md`
- Good: `threshold-training.md`, `knee-health.md`, `squat-progression.md`
- Bad: `ThresholdTraining.md`, `knee_health.md`, `Squat Progression.md`
