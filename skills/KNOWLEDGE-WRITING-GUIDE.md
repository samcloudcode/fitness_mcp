# Knowledge File Writing Guide

Best practices for creating actionable, coaching-focused knowledge files.

---

## Core Principles

### 1. Actionable With Mechanism (Not Academic)

**Good**: "Use 3-4 week progression stages for Nordic curls (tendon adaptation lags muscle by 3-4 weeks)"
**Bad**: "Research shows that tendon collagen synthesis rates are slower than myofibrillar protein synthesis due to lower vascularity..."

**Why**: Coaches need to make decisions AND adapt when circumstances change. Include enough "why" to enable intelligent modification, not so much that it buries the action.

**The Balance**: "What to do" + "minimal viable mechanism for adaptation" + specific numbers.

---

### 2. Programming-Centric Organization

Structure around **workout design decisions**, not anatomical systems.

**Good structure**:
- Exercise Selection for [Problem]
- Progression Rules for [Exercise]
- Volume Guidelines for [Goal]
- Cueing Strategies for [Common Issue]

**Bad structure**:
- Anatomy of the Knee Joint
- Biomechanics of Flexion
- Physiological Adaptations to Training

**Why**: The file gets loaded when programming workouts. Organize around that task.

---

### 3. Signal-to-Noise Ratio

**Target length**: 150-250 lines for major topics
- Any longer = diluted signal, harder to scan
- Any shorter = probably too narrow to warrant separate file

**Compression techniques**:
- Replace paragraphs with bullet points
- Cut "how it works" if "what to do" is clear
- Merge related subsections
- Use examples to teach principles (not both separately)

---

## Structure Template

```markdown
# [Topic]: [Frame as Practical Outcome]

One-line description focusing on application.

---

## Core Principle: [Key Insight]

**Key Insight**: The counterintuitive or most important thing.

**Programming Implications**:
- What this means for workout design
- 2-4 bullets max

---

## [Muscle Group/Movement Pattern]: [What It Does]

**Programming Priority**:
- Specific exercises
- Key variables (sets, reps, progression)
- **Why**: One-sentence mechanism

**Common Pattern**: Symptom → Root cause → Solution

---

## [Decision Framework/Checklist]

**If [Scenario] → [Action]**

**Variables**:
- List key decision points
- Specific thresholds or checkpoints

**Example Path**: Starting point → progression steps → endpoint

---

## When to Use This Knowledge

**Load when**:
- [Specific programming scenario]
- [Type of user question]
- [Particular exercise selection need]

**Remember**: [How this relates to user-specific MCP knowledge entries]
```

---

## Writing Guidelines

### Lead with "What" and "When", Follow with "Why"

**Good**:
"Use box squats to control depth (deep flexion issue). Why: Builds capacity in pain-free range before expanding ROM."

**Bad**:
"The biomechanical advantage of box squats relates to the ability to modulate depth at the eccentric-concentric transition point, which is relevant because..."

**Pattern**: ACTION (context) + Why: MECHANISM

---

### Use Hierarchical Information Density

**Most important** (top of section):
- The decision rule or action item
- Specific numbers (sets, reps, weeks, RPE)

**Supporting** (middle):
- Why it works (one sentence)
- Common patterns/examples

**Optional** (bottom/cut if needed):
- Edge cases
- Advanced nuances
- Historical context

---

### Examples Should Teach Principles

**Good example** (teaches pattern):
"Cyclist with knee pain: Strong concentric quads (cycling) but weak eccentric → add step-downs → pain resolves as eccentric capacity builds."

**Bad example** (just anecdote):
"I once worked with a cyclist who had knee pain and we tried several things and eventually the pain got better."

**Why**: Good examples compress "symptom → diagnosis → solution → outcome" into pattern recognition.

---

### Compress Mechanisms (But Keep Them)

**Full version** (cut this):
"The vastus medialis obliquus, particularly its oblique fiber orientation at approximately 50-55 degrees, provides a medial vector force on the patella which counteracts the natural lateral tracking tendency created by the Q-angle..."

**Compressed version** (keep this):
"VMO pulls patella medially, preventing lateral tracking issues. Target with terminal knee extensions."

**Rule**: Include mechanism in one sentence if it enables adaptation. Cut it if it's purely explanatory.

**Examples of useful mechanisms**:
- "Tendon adapts 3-4× slower than muscle" → Informs progression timing for ANY tendon exercise
- "Hip mobility prevents knee compensatory rotation" → Explains why hip work helps knee pain
- "Eccentric strength controls deceleration" → Shows when to prioritize eccentric vs concentric

**Examples to cut**:
- Anatomical detail that doesn't change exercise selection
- Historical research context
- Mechanisms LLMs already know from general training

---

### Use Formatting for Scanning

**Bold** for key terms and decision points:
- "**Programming Priority**: Full ROM quad exercises"
- "**Critical Rule**: Earn hip mobility BEFORE loading deep flexion"

**Arrows** for cause-effect:
- "Weak VMO → lateral patellar tracking → pain"
- "Box squat @ parallel → lower box 1" every 2-3 weeks → full depth"

**Numbers** for specifics:
- "3-4 weeks per progression stage"
- "RPE 6-7 for rehab"
- "8-10 sets/week for maintenance"

---

## Quality Checks

Before finalizing, ask:

### 1. Programming Test
"If I'm designing a workout for someone with [relevant issue], can I quickly find the answer?"
- If you need to read >50% of the file → too much noise
- If the answer requires synthesis across multiple sections → restructure

### 2. Density Test
Pick any 10-line section. Can you cut it to 7 lines without losing key information?
- If yes → do it
- If no for most sections → good density

### 3. Actionability Test
Count "what to do" items vs "how it works" explanations. Ratio should be 2:1 or higher.

### 4. Adaptation Test
Pick a principle and ask: "If the standard recommendation doesn't work, does this file give me enough mechanism to adapt intelligently?"
- If yes → good balance of action + mechanism
- If no → add one-sentence "why" to key recommendations

### 5. Duplication Test
Does this overlap heavily with other knowledge files?
- If yes → merge or split differently
- General principles go in one file, specific applications in others

---

## Common Mistakes

### ❌ Textbook Syndrome
Writing what you learned in school vs what coaches need in the gym.

**Fix**: Ask "What decision does this help me make?" If unclear, cut it.

---

### ❌ Everything in One File
Trying to cover an entire domain comprehensively.

**Fix**: Split by programming context (rehab vs performance, beginner vs advanced, different movement patterns).

---

### ❌ Under-Compression
Keeping interesting information that doesn't affect decisions.

**Fix**: Every paragraph should answer "what should I do differently because I know this?"

---

### ❌ Missing Specifics
Vague guidance like "progressive overload" or "listen to your body."

**Fix**: Give actual numbers (weeks, sets, RPE, ROM checkpoints).

---

### ❌ Orphaned Principles
Principles without application examples, or examples without principles.

**Fix**: Every principle needs "Programming Implications" section. Every example should teach a pattern.

---

### ❌ Missing Mechanisms
Pure "what to do" without "why" that prevents intelligent adaptation.

**Fix**: Add one-sentence mechanism to key recommendations. Test: "If this doesn't work, can the coach modify intelligently?"

**Example**:
- ❌ "Use 3-4 week progression stages for Nordics"
- ✅ "Use 3-4 week progression stages for Nordics (tendon adapts 3-4× slower than muscle)"

The mechanism ("tendon lag") teaches the coach to apply 3-4 week staging to OTHER tendon exercises, not just Nordics.

---

## Evolution Over Time

Files should **get shorter**, not longer:
- Initial draft: Brain dump everything relevant (300+ lines OK)
- First edit: Cut to essential decisions (200-250 lines)
- Second edit: Compress mechanisms, merge sections (150-200 lines)
- Mature version: Dense, scannable, actionable (<200 lines)

**Test**: Can an experienced coach read this in 3-5 minutes and extract what they need? If no, keep compressing.
