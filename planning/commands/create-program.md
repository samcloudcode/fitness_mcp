# Program Creation

## Topic/reference: $ARGUMENTS

## Overview

**What is a program?** A 1-3 month strategic document showing how all goals fit together and providing the framework to achieve them.

**Program contains:** Goals/priorities, training split (upper/lower, full-body, etc.), training frequencies (4x strength/week, 3x cardio/week), exercise architecture, progression framework, recovery strategy, constraint management, complete rationale.

**Program does NOT contain:** Specific weekdays (Mon/Tue/etc.) - that's handled in week planning.

**Hierarchy:**

- **Program** = 1-3 month strategy (WHAT exercises, HOW MANY per week, HOW to progress)
- **Week** = 7-day schedule (WHEN - specific days like Mon/Tue, WHERE - which gym)
- **Workout** = Today's session (exact exercises/sets/reps/weights)

**Storage:** Kind `program`, key `current-program` (single living document), up to 1000 words. Update when strategy changes or becomes stale (3+ months).

---

# PART A: CORE WORKFLOW

**Follow these 6 steps sequentially to create a program:**

## Step 1: Extract Context

**Fetch:** `overview(context='planning')` → Returns goals, program, week, plan, preferences, knowledge, logs

**Analyze what you have:**

- **Goals:** Priorities → volume/frequency allocation; targets → progression timeline; deadlines → periodization urgency
- **Knowledge:** Injuries → exercise modifications; limitations → alternatives; recovery patterns → frequency
- **Preferences:** Equipment → exercise selection; time → volume strategy; activities → scheduling
- **Logs (recent 10):** Working weights → starting loads; volume tolerance → targets; responses → exercise selection
- **Current program:** What works → keep; what doesn't → fix; how long → need variation?

**CRITICAL:** Extract from ACTUAL data, not assumptions.

**NOTE:** The current program is **context, not constraint**. Use it to understand:
- What's been tried (exercise selection, frequencies, progressions)
- What worked well (keep successful elements)
- What didn't work (change unsuccessful elements)
- How long it's been running (staleness indicator)

**You are free to redesign completely** if you can create a better approach based on the user's current goals, knowledge, and recent training data. Programs are living documents meant to evolve. Don't feel bound by previous choices if better options exist.

## Step 2: Reference Protocols

**Load protocols as needed to inform thinking (not as validation checklists):**

Refer to [protocols/INDEX.md](../protocols/INDEX.md) for the current list of available protocols. Load relevant protocols based on:

- User's injury history or movement restrictions
- Specific training goals (strength, endurance, VO2 max, etc.)
- Recovery and volume management needs
- Exercise selection and movement pattern coverage
- Progression frameworks appropriate for training age

## Step 3: Design Strategy

**Analyze the gap:**

- NOW → GOAL: What's the gap? Realistic progression calculation from logs to targets
- CONSTRAINTS: Injuries, equipment, schedule from knowledge/preferences
- TOLERANCE: Volume/frequency from logs, recovery patterns

**Design plan covering:**

- Volume/frequency allocation (based on priorities and tolerance)
- Exercise architecture (main/secondary/accessories matched to equipment & limitations)
- Periodization timeline (deadlines and current state)
- Progression scheme (matched to training age from protocols)
- Equipment strategy (which gym when, travel adaptations)
- Deload schedule (every 4-8 weeks)
- Hard/easy distribution (total hard days, sequencing)

## Step 4: Validate with Plan-Validator Agent

**Use the plan-validator agent to critically review your program draft:**

Use the Task tool to call the plan-validator agent with your drafted program. The agent will:
- Cross-reference against user's goals, knowledge entries (injuries/limitations), recent logs, and preferences
- Check for safety issues, load management problems, and goal alignment
- Verify progression logic and recovery adequacy
- Provide structured feedback on critical issues, important considerations, and suggestions

**Pass to the agent:**
- The complete program draft you've designed
- Context: "This is a program proposal. Please validate against the user's context."

**Review the validation report and address:**
- **Critical issues** (must fix before proceeding)
- **Important considerations** (should address)
- **Suggestions** (incorporate if they improve the plan)

**Iterate on your program based on the validation feedback until the agent assessment is "Pass with modifications" or "Approved as-is".**

## Step 5: Propose to User

**Present strategy with:**

- Training frequencies (4x strength/week, 3x cardio/week, etc.)
- Training split (upper/lower, full-body, push/pull/legs, etc.)
- Exercise architecture (main/secondary/accessories/mobility)
- Starting weights (from logs)
- Progression timeline & method
- Equipment strategy & constraint management
- How it addresses ALL injury/movement limitations
- Complete rationale (why this approach)

**NOTE:** Program defines WHAT exercises, HOW MANY sessions per week, and HOW to progress. Week planning (plan-week.md) handles WHEN (specific days like Mon/Tue/etc.).

## Step 6: Get Approval & Save

After user approval:

```python
upsert(
    kind='program',
    key='current-program',
    content='[800-1000 words: comprehensive strategy with goals, split, progression, constraints, rationale, detailed session structure, exercise selection, recovery protocols]'
)
```

**Confirm success:**

- Summarize key features
- Highlight how limitations addressed
- Suggest: "Ready to plan this week's schedule?"

---

## Example Execution

**User:** "Create 12-week strength program for rugby, 4x/week"

**Step 1 - Extract Context:**

Overview shows rugby goal (Squat 225→315, Bench 185→225 by April). Knee tracking issues, shoulder impingement. Home gym available. Currently 3x/week, 12-15 sets/session, good recovery.

**Step 2 - Load Protocols:**

Reviewed protocols/INDEX.md and loaded: injury-prevention (knee/shoulder), progression (intermediate = wave loading), recovery-management (4x/week OK)

**Step 3 - Design:**

Upper/Lower 4x/week. Block periodization (hypertrophy→strength→peak). Wide stance squats ONLY. Front OHP only. Deload weeks 4,8,12.

**Step 4 - Score:**

Goal alignment 9/10, Safety 10/10, Adherence 9/10, Evidence-based 9/10. Overall: 9.25/10 ✓

**Step 5 - Propose:**

"Upper/Lower split, 4x strength sessions per week. 3 blocks: hypertrophy (4x8-12) → strength (4x5-8) → peak (3x3-5). Wide stance squats, front OHP only (addresses knee/shoulder). Starting from logs: Squat 225, Bench 185, Deadlift 275. Deload every 4 weeks. Specific days will be scheduled in week planning. Approve?"

**Step 6 - Save:**

```python
upsert(kind='program', key='current-program',
       content='12wk rugby strength: 4x/week upper/lower split. Blocks 1-3: 8-12→5-8→3-5 reps. Squat 225→285, bench 185→215, deadlift 275→335. Wide stance squats ONLY (knee), front OHP only (shoulder). Daily hip mobility, face pulls. Deload wk 4,8,12. Why: April peak, addresses limitations, builds strength foundation for rugby.')
```

---

# PART B: REFERENCE MATERIAL

**Use these sections when relevant to the user's situation:**

## Block Emphasis Rotation

**When to use:** Managing competing priorities (strength + endurance), avoiding plateaus, addressing periodization needs

**Strength-Focus Block (8-12 weeks):**

- Training: 3-4x strength, 2x endurance (maintenance dose)
- Volume: Full progressive overload in strength, endurance reduced to 1 long Z2 + 1 tempo/HIIT
- Nutrition: Slight calorie surplus or maintenance, protein prioritized
- Goal: Build muscle mass, increase maximal strength, maintain aerobic base
- Example: "Bench 225 by June" priority - 4x upper/lower split, 2x easy runs 30-40min

**Endurance-Focus Block (8-12 weeks):**

- Training: 2x strength (maintenance dose), 3-5x endurance (progressive mileage/intervals)
- Volume: Strength reduced to compounds only (2-3 sets), endurance builds weekly
- Nutrition: Adequate carbs for fueling, protein maintained, possible slight deficit if race weight goal
- Goal: Build aerobic capacity, improve VO2 max/distance, maintain muscle mass
- Example: "20K run" priority - 2x full-body strength, 3-4x runs + 1x cycling/swimming

**Transition Between Blocks:**

- Deload week before switching emphasis (50% volume both modalities)
- Assess: Did previous block achieve goal? What needs focus next?
- Redefine p1/p2 priorities (previous p1 may become p2 for next block)

**Why this works:**

- Each quality gets dedicated progressive overload period (avoid trying to maximize both simultaneously)
- Maintenance dose (2x/week, reduced volume) prevents loss of secondary quality
- 8-12 weeks sufficient for meaningful adaptation without excessive staleness
- Year-round: Alternate blocks = continuous progress in both domains over time

**Block rotation example (yearly):**

- Weeks 1-12: Strength focus (p1: bench-225, p2: maintain 20mpw running base)
- Week 13: Deload both
- Weeks 14-25: Endurance focus (p1: 20K run, p2: maintain strength)
- Week 26: Deload both
- Weeks 27-38: Strength focus (p1: squat-315, p2: maintain aerobic fitness)
- Week 39: Deload both
- Weeks 40-52: Endurance focus (p1: improve VO2 max, p2: maintain muscle)

---

## Yearly Macrocycle Planning

**Four-phase model for long-term development:**

**Base Phase (Weeks 1-12, typically Jan-Mar):**

- Emphasis: Aerobic foundation, mobility, general strength
- Training: High-volume low-intensity endurance (80/20 polarization), moderate strength (full-body 2-3x/week)
- Focus: Build work capacity, address movement limitations, "bulletproof" joints with prehab
- Example: Long easy runs/rides (60-90min Z2), mobility daily, compound lifts moderate weight
- Why: Foundational period establishes base for later intensity, low injury risk, high adherence

**Build Phase (Weeks 13-26, typically Apr-Jun):**

- Emphasis: Increase intensity in both strength and endurance
- Training: Add HIIT sessions (VO2 max intervals 1-2x/week), heavier strength loads (hypertrophy/strength phases)
- Focus: Progressive overload, skill development (improve technique, learn new movements)
- Example: 4×4min VO2 intervals, 3×5 strength protocol, maintain mobility work
- Why: Base allows tolerating higher intensity, gains accelerate with increased stimulus

**Peak/Specific Phase (Weeks 27-38, typically Jul-Sep):**

- Emphasis: Goal-specific training, performance optimization
- Training: Target event/milestone (longer runs at race distance, strength peaking protocol, competition prep)
- Focus: Specificity - exactly what goal requires (if 20K run → runs at 20K pace, if strength → heavy singles/doubles)
- Example: 18K runs at target pace, taper strength to 2x/week maintenance near event
- Why: Specificity principle - adaptations become highly targeted to goal demands

**Recovery Phase (Weeks 39-52, typically Oct-Dec):**

- Emphasis: Active rest, cross-training, rehab nagging issues, plan next year
- Training: Unstructured play, variety (mountain biking, swimming, yoga, sports), light strength
- Focus: Mental break, address weaknesses, maintain general fitness without structure
- Example: Fun activities 3-4x/week (no strict program), mobility/prehab focus, social training
- Why: Prevents burnout, allows full physiological recovery, opportunity to fix imbalances before next cycle

**Applying the macrocycle:**

- Map year based on events/goals (if race in September, peak phase July-September)
- Not all years need all 4 phases (can do Base → Build → Base → Build for general fitness)
- Adjust phase lengths based on goals (competitive athlete might have multiple Peak phases, general fitness might extend Base phase)
- Always include recovery periods (even mini-recoveries every 3-4 months)

---

## Performance Feedback Loop

**Evaluate every 4-6 weeks - adjust upcoming block based on objective feedback:**

**Strength metrics:**

- Are working weights increasing? (e.g., squat 225 → 240 over 6 weeks = on track)
- RPE at given load decreasing? (e.g., 185lb bench was RPE 8, now RPE 7 = strength gain)
- If plateau: Increase volume, change rep scheme, add frequency, or prioritize strength focus block

**Endurance metrics:**

- Is pace at given heart rate improving? (e.g., Z2 run pace 10min/mile → 9:30min/mile = aerobic improvement)
- Can complete longer distances? (e.g., 10K easy → 15K easy over 6 weeks = work capacity gain)
- VO2 max intervals getting easier? (e.g., 4×4min HR recovery faster between intervals = adaptation)
- If plateau: Increase frequency, add interval session, prioritize endurance focus block

**Mobility metrics:**

- ROM improving in target areas? (e.g., squat depth increasing, shoulder overhead reach improving)
- Movement quality better? (e.g., knee tracking improved in lunges, hip hinge cleaner)
- If plateau: Increase daily frequency, add dedicated mobility session, address specific limitations

**Joint health / pain signals:**

- Any new persistent pain? (e.g., knee ache after runs = warning sign, reduce volume/impact)
- Existing limitations improving? (e.g., previous shoulder twinge gone = prehab working)
- If pain emerging: Immediately modify (reduce load/volume, eliminate aggravating movements, increase prehab work)

**Recovery indicators:**

- Sleep quality, resting heart rate, HRV trends, subjective energy levels
- If deteriorating: Deload immediately (don't wait for scheduled deload), reduce total volume 30-40%

**Adjustment decision tree:**

1. **Both strength and endurance progressing:** Continue current program, ride the wave
2. **One modality plateaued, other progressing:** Consider shifting to focus block for plateaued quality
3. **Both plateaued:** Deload week, then reassess (may need more recovery, change in stimulus, or reset expectations)
4. **Injury/pain signal:** Address immediately (reduce aggravating modality, increase prehab, assess form)
5. **Life stress increased:** Reduce training volume 20-30% temporarily (work deadline, travel, family stress taxes same recovery system)

**Example application:**

- Week 6 evaluation: Squat +15lbs (good), bench plateaued (stuck), runs improving (good), sleep poor (concerning)
- Decision: Next 6 weeks - maintain lower body, increase upper body frequency/volume, reduce total run volume slightly to improve sleep
- Week 12 re-evaluation: Bench now improving, sleep better, reassess again

---

## Adherence Optimization

**Best program = one you'll actually follow. Build in sustainability:**

**Enjoyment principle:**

- Include activities you LOVE (if you love mountain biking, count it as endurance vs forcing yourself to run)
- Rotate exercises (if barbell squats feel stale, switch to goblet squats, box squats, or split squat variations for 4-6 weeks)
- Social training (yoga class, group ride, climbing gym with friends > solo basement grind for many people)
- Skills/play (handstand practice, obstacle courses, sports keep training fun vs pure strength/cardio grind)

**Flexibility within structure:**

- Define "workout types" in program, not rigid day assignments (week handles specific days)
- Minimum viable dose defined (if busy week, hit 2x strength + 1x endurance "anchor" sessions, skip optional extras)
- Backup plans for constraints (gym closed → bodyweight alternatives, travel → hotel workouts)

**Realistic integration:**

- Plan sessions around actual schedule patterns (mornings vs evenings, weekday vs weekend availability)
- Equipment access matches reality (barbell program needs regular gym access)
- Travel adaptations pre-planned (hotel workout variations, minimal equipment options)

**Mental freshness:**

- Monthly themes (if feeling stale, try "Mobility March," "Handstand April" for variety while maintaining program)
- Deload weeks (physical recovery + mental break from intensity)
- Competition/events (sign up for fun run, powerlifting meet, obstacle race to make training feel purposeful)

**Tracking without obsession:**

- Log enough to see progress (working weights, run distances), not so much it's burdensome
- Celebrate wins (hit new 5RM, ran longest distance, pain-free training week)
- Don't let missed sessions derail you (one missed workout = 0% impact on long-term progress, guilt spiral = 100% impact on adherence)

**If adherence drops:**

- Assess: Too much volume? Boring? Not seeing results? Life stress?
- Adjust: Reduce volume 30%, swap activities, change gym/environment, find training partner
- Remember: Consistency over years > perfection for weeks

**Example adherence-optimized program:**

- User loves: Spinning, yoga classes, mountain biking, hates: running, enjoys: lifting with friends
- Program: 2x strength (gym with buddy), 2x spinning class, 1x yoga class, 1x MTB ride (weekend)
- Result: Hits all modalities (strength, cardio, mobility, skills) using preferred activities = high adherence

---

## Goal-Driven Programming Framework

**Prioritize by p-value:**

- **p1:** Primary focus - most volume, highest frequency, best recovery
- **p2:** Secondary - maintain, don't progress aggressively
- **p3:** Minimal viable dose - don't interfere with p1/p2

**Handling competing p1 goals:**

- Sequential blocks (12 weeks each, alternate focus)
- Concurrent (train both, accept 30% slower progress)
- Redefine priorities (make one p2)

**Deload protocols (from protocols):**

- When: Every 4-8 weeks scheduled, or reactive
- How: 50% volume OR 50% intensity OR 50% frequency (choose one)
- Why: Dissipates fatigue, maintains neural patterns

---

## Anti-Patterns

❌ Ignoring knowledge entries (injuries/limitations)
❌ Arbitrary loads not from logs
❌ Equipment assumptions
❌ Missing "why" context
❌ No deload strategy
❌ Progression inappropriate for training age
❌ Programming contraindicated exercises
❌ Including specific weekdays (Mon/Tue/etc.) - that's for week planning
❌ Too vague (<500 words) or missing key details (sessions, progressions, protocols)

---

## Program Quality Checklist

Before finalizing, verify the program artifact contains:

- [ ] Goals with priorities, current state, targets, and deadlines included
- [ ] Training frequencies specified (e.g., "4x strength/week, 3x endurance/week")
- [ ] Training split defined (e.g., "upper/lower", "full-body", "push/pull/legs")
- [ ] Exercise architecture defined (main/secondary/accessories/mobility)
- [ ] Progression framework specified with method (e.g., "+5lb/week", "wave loading")
- [ ] Deload schedule included (e.g., "every 4 weeks, 50% volume")
- [ ] Recovery strategy clear (hard/easy distribution, total rest days per week)
- [ ] ALL injury limitations from knowledge entries addressed with modifications
- [ ] Equipment strategy noted (gym access, home equipment, travel adaptations)
- [ ] Known constraints acknowledged (travel patterns, work conflicts) - NOT scheduled to specific days
- [ ] Progression rate realistic for training age
- [ ] Complete "why" rationale connecting to goals
- [ ] Content length 800-1000 words (comprehensive detail)
- [ ] NO specific weekdays mentioned (that's for week planning)
- [ ] (if applicable) Block emphasis rotation defined for competing goals

---

## Notes

- Always check knowledge entries for limitations (safety paramount)
- Base loads on recent logs (not arbitrary)
- Reference protocols as expertise sources (not validation gates)
- Think deeply about best approach (no cookie-cutter)
- Get user approval before saving
- Programs are living documents (update when strategy changes)
- Length: 800-1000 words for comprehensive detail (sessions, progressions, protocols, rationale)
