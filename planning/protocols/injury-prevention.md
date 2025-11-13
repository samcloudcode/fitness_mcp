# Injury Prevention Protocol

## Purpose

Provides evidence-based frameworks for identifying injury risks and implementing preventive strategies. **This protocol must be checked before any programming decision** to ensure user safety is prioritized above all other training goals.

## When to Use

- **ALWAYS before exercise selection** - Check user limitations FIRST
- **ALWAYS before programming workouts** - Verify no contraindications
- Planning program structure (program-creator) - Ensure prehab included
- Reviewing training logs for injury risk signals (all agents)
- Assessing need for exercise modifications or substitutions
- When user reports pain, discomfort, or movement quality issues

## Critical Rule

**NEVER program exercises that conflict with user's knowledge entries (injuries, limitations, movement restrictions).** If a limitation exists, honor it. No exceptions.

## Decision Framework

### Step 1: Review ALL User Limitations (MANDATORY)

**Before ANY exercise selection or programming**:

```python
# ALWAYS do this first
limitations = get(kind='knowledge')
# Review EVERY entry for:
# - Current injuries
# - Past injuries with residual limitations
# - Movement restrictions
# - Pain or discomfort patterns
# - Medical conditions affecting training
```

**Document Review Checklist**:
✅ All knowledge entries reviewed
✅ Specific limitations identified
✅ Contraindicated exercises noted
✅ Modifications/substitutions prepared

### Step 2: Exercise Selection Safety Gates

**For each exercise considered, verify**:

1. **Not contraindicated** by user's limitations
2. **Appropriate technique complexity** for user's skill level (poor technique = injury risk)
3. **Adequate warm-up** for injury-prone areas
4. **Proper load progression** (not excessive jumps)
5. **Movement quality** emphasized (especially with previous injuries)

**If ANY gate fails → modify or substitute exercise**

### Step 3: Volume and Load Safety

**Overuse Injury Risk Factors**:
- Too much volume too soon (>10% weekly volume increase)
- Insufficient recovery (same muscle group <24 hours apart)
- Excessive load jumps (>10% week to week)
- High-risk exercise overuse (e.g., too much overhead work with shoulder history)
- Ignoring pain or discomfort signals

**Load Progression Safety**:
- Maximum 5-10% load increase week to week for most exercises
- Smaller jumps (2.5-5lbs) for upper body and injury-prone movements
- Larger jumps (5-10lbs) acceptable for lower body if no injury history
- **If recovering from injury**: 2.5lbs maximum, or even maintain loads while increasing reps

**Volume Progression Safety**:
- Maximum 10% volume increase per week (sets × reps)
- More conservative (5%) if recovering from injury or new to exercise
- Monitor total training volume across all sessions (not just per-session)

### Common Injury Patterns and Prevention

**Knee Issues**:
- **Problem**: Improper tracking (knees caving in, not over toes)
- **Prevention**: Wide stance squats, cue knee tracking, strengthen glutes/abductors
- **Modifications**: Goblet squats (easier to maintain form), box squats (depth control)
- **Red flags**: Pain during/after squatting, knee clicking/popping

**Shoulder Issues**:
- **Problem**: Impingement, instability, rotator cuff strain
- **Prevention**: Balanced push/pull ratio (2:1 pull:push or 1:1), rotator cuff prehab, avoid behind-neck pressing
- **Modifications**: Neutral grip pressing, moderate grip width, limit overhead volume if history present
- **Red flags**: Pain with overhead movements, anterior shoulder pain, clicking

**Lower Back Issues**:
- **Problem**: Strain, disc issues, poor bracing
- **Prevention**: Core strengthening, proper bracing technique, avoid excessive spinal flexion under load
- **Modifications**: Trap bar deadlift (more upright), belt squats, RDLs instead of conventional deadlifts
- **Red flags**: Sharp pain during/after lifting, radiating pain down legs, loss of movement quality

**Elbow Issues** (tendinitis, golfer's/tennis elbow):
- **Problem**: Overuse, poor grip mechanics, excessive volume
- **Prevention**: Vary grip widths, limit high-volume curling/extension work, wrist/forearm mobility
- **Modifications**: Neutral grip variations, reduce direct arm work volume, add forearm prehab
- **Red flags**: Pain during pressing/pulling, grip weakness, pain at tendon insertions

**Hip Issues**:
- **Problem**: FAI, labral issues, tight hip flexors, poor mobility
- **Prevention**: Daily hip mobility (CARs), avoid excessive depth if pinching, strengthen hip external rotators
- **Modifications**: Box squats (controlled depth), sumo deadlifts (better hip angles), single-leg work
- **Red flags**: Pinching at bottom of squat, groin pain, clicking/clunking

### Prehab Exercise Selection

**Essential prehab by body area**:

**Shoulders** (especially with pressing volume):
- Face pulls: 2-3x15-20 daily or every session
- Band pull-aparts: 2x20-25
- External rotation work: 2x15 each arm
- Scapular wall slides: 2x10

**Knees**:
- Hip CARs: 2x5 each direction daily
- Glute bridges: 2x15
- Terminal knee extensions (TKEs): 2x20
- Single-leg balance work

**Lower back/Core**:
- McGill Big 3 (curl-up, side plank, bird dog): 3x10 each
- Dead bugs: 2x10 each side
- Pallof press: 2x12 each side

**Hips**:
- Hip CARs: 2x5 each direction daily (CRITICAL for hip health)
- 90/90 hip switches: 2x10
- Cossack squats: 2x8 each side

**General** (all trainees):
- Daily movement prep (5-10 minutes before training)
- Weekly dedicated mobility session if possible

### Pain and Discomfort Decision Tree

```
User reports pain or discomfort:
├─ SHARP pain during exercise → STOP immediately, avoid exercise, consider medical referral
├─ Dull ache during exercise → Reduce load, modify range of motion, monitor closely
├─ Soreness 24-48 hours post-training → Normal (DOMS), continue as planned
├─ Pain persisting >72 hours → Reduce volume/intensity, add extra rest, monitor
└─ Pain worsening over multiple sessions → Cease aggravating exercises, modify program, consider medical referral
```

**Pain Scale Decision**:
- **0-2/10**: Safe to continue, minor discomfort is acceptable
- **3-4/10**: Caution - reduce load or modify exercise, monitor closely
- **5+/10**: Stop exercise immediately, substitute or rest
- **ANY sharp/shooting pain**: Stop immediately regardless of intensity

### Warm-up Requirements by Injury History

**No injury history** (standard warm-up):
- 5 minutes general (cardio, dynamic movement)
- Specific warm-up sets (bar → 50% → 70% → working weight)

**Previous injury in area** (enhanced warm-up):
- 5-10 minutes general + specific mobility for area
- Prehab exercises for that joint/area (2-3 sets)
- Extended warm-up sets (bar → 40% → 60% → 80% → working weight)
- Movement quality focus (not just "getting warm")

**Recent injury or current limitation**:
- 10+ minutes dedicated warm-up and mobility
- Full prehab protocol for area
- Very gradual loading (many warm-up sets)
- Consider reducing working weight for extended period
- Movement quality emphasis over load

## Validation Criteria

### Must-Have Checks (Before ANY Programming)
✅ ALL user knowledge entries reviewed for limitations
✅ No exercises contraindicated by user's limitations programmed
✅ Appropriate warm-up included for injury-prone areas
✅ Load progression within safe limits (5-10% max)
✅ Volume progression within safe limits (10% max weekly increase)
✅ Adequate recovery between high-stress sessions
✅ Prehab exercises included based on injury history
✅ Movement quality cues included where relevant (e.g., "wide stance" for knee tracking issues)

### Warning Signs (Review Required)
⚠️ User has injury history but no prehab programmed
⚠️ High-volume programming for area with previous injury
⚠️ Progression >10% in single jump
⚠️ Complex exercises without adequate warm-up
⚠️ User reports discomfort in logs but program unchanged

### Automatic Failures (NEVER Program This Way)
❌ Exercise directly contraindicated by user's known limitation (e.g., narrow squats for knee tracking issue)
❌ No warm-up for injury-prone area with history
❌ Excessive load/volume progression (>15% jumps)
❌ Ignoring user's pain reports in recent logs
❌ Programming without reviewing knowledge entries first

## Cross-Check Points

- **exercise-selection.md** - All exercises must pass injury prevention checks
- **progression.md** - Progression rate must be safe (conservative with injury history)
- **recovery-management.md** - Inadequate recovery is primary injury risk factor
- **movement-patterns.md** - Imbalanced movement patterns create overuse injuries

## Examples

### Example 1: Knee Tracking Limitation
**Knowledge entry**: "knee-tracking: Keep knees over toes, avoid narrow stance, previous patellar tracking issues"

**Exercise Selection**:
```
✅ SAFE:
- Back squat: WIDE STANCE (explicitly noted)
- Goblet squat: Wide stance, easier to maintain form
- Bulgarian split squats: Natural knee-over-toe position
- Deadlifts: No knee-specific stress

❌ AVOID:
- Narrow stance squats (contraindicated)
- High-bar Olympic squats with narrow stance (contraindicated)
- Leg press with feet close together (risk of poor tracking)

PREHAB INCLUDED:
- Hip CARs daily: 2x5 each direction (improve hip control)
- Glute bridges: 2x15 (strengthen glutes for knee stability)

WARM-UP:
- Bodyweight squats wide stance 2x10 (practice form)
- Specific squat warm-up sets with cueing
```

**Validation**:
- ✅ All exercises honor limitation (wide stance)
- ✅ Prehab addresses root cause (hip control, glute strength)
- ✅ Warm-up includes form practice

### Example 2: Shoulder Impingement History
**Knowledge entry**: "shoulder-history: Previous impingement, avoid behind-neck pressing, limit overhead volume"

**Exercise Selection**:
```
✅ SAFE:
- Bench press: In front of neck only
- Overhead press: FRONT (in front of head), moderate volume (not excessive)
- Neutral grip dumbbell press: Safer shoulder angle
- Horizontal pulling: Extra volume (2:1 pull:push ratio for shoulder health)

❌ AVOID:
- Behind-neck press (contraindicated)
- Behind-neck pulldowns (contraindicated)
- Excessive overhead volume (>10 sets/week overhead work)

PREHAB INCLUDED:
- Face pulls: 3x20 every session (rotator cuff, posterior delt)
- Band pull-aparts: 2x25 (scapular health)
- External rotation: 2x15 each arm (rotator cuff strength)

WARM-UP:
- Shoulder CARs: 2x5 each direction
- Band pull-aparts: 2x15 (activate posterior shoulder)
- Scapular wall slides: 2x10 (movement prep)
- Light overhead press warm-up (start with bar, gradual loading)
```

**Validation**:
- ✅ No contraindicated exercises (behind-neck movements)
- ✅ Overhead volume limited (only OHP, not excessive)
- ✅ Comprehensive prehab (face pulls, external rotation)
- ✅ Pull:push ratio balanced or favoring pulling
- ✅ Enhanced warm-up for shoulder

### Example 3: No Injury History (Still Need Prevention)
**Context**: Beginner, no injuries, but want to prevent issues

**Preventive Strategy**:
```
PROGRAM DESIGN:
- Balanced movement patterns (see movement-patterns.md)
- Conservative progression (5lbs upper, 10lbs lower per session for beginner)
- Adequate recovery (2 rest days/week)
- Simple exercises initially (reduce technical injury risk)

PREHAB INCLUDED (General Prevention):
- Face pulls: 2x20 (shoulder health - pressing volume)
- Hip CARs: Daily (hip mobility and health)
- Plank variations: 3x30s (core stability)

WARM-UP:
- 5 minutes general movement
- Specific warm-up sets (bar → 50% → 70% → working)

MONITORING:
- Track RPE (don't push to failure initially - save buffer)
- Watch for any discomfort patterns
- Gradual volume increases (don't jump into high volume)
```

**Validation**:
- ✅ Prevention-focused even without injury history
- ✅ Conservative progression (injury avoidance)
- ✅ Basic prehab for common injury areas
- ✅ Monitoring plan for early warning signs

### Example 4: Reactive Modification for Emerging Issue
**Context**: User reports "shoulder felt tweaky during bench press last session" in log

**Response**:
```
IMMEDIATE ADJUSTMENT:
- Reduce bench press load 10-20% next session
- Add pause at chest (improve control, reduce bounce stress)
- Extra shoulder warm-up (add 5 minutes shoulder mobility)
- Monitor pain scale (if >2/10, stop exercise)

INVESTIGATION:
- Review recent pressing volume (has it increased significantly?)
- Check pull:push ratio (is pulling adequate?)
- Ask about form changes, life stress, sleep quality

SHORT-TERM MODIFICATION (1-2 weeks):
- Moderate pressing volume (reduce sets by 1-2)
- Increase pulling volume (add extra row sets)
- Add daily shoulder prehab:
  - Face pulls 3x20
  - Band pull-aparts 2x25
  - External rotation 2x15

CONTINGENCY:
- If pain persists or worsens → substitute bench with neutral grip DB press
- If pain continues → consider medical referral, avoid pressing temporarily
```

**Validation**:
- ✅ Proactive response to early warning sign
- ✅ Load reduction to reduce stress
- ✅ Investigation of potential causes
- ✅ Prehab intensified
- ✅ Contingency plan if doesn't resolve

## Anti-Patterns

❌ **Programming without reviewing knowledge entries** - Most critical mistake, ignores user's known limitations
❌ **"Working through pain"** - Pain is a signal, not weakness to overcome
❌ **Skipping warm-up for injury-prone areas** - False economy, saves 5 minutes, risks weeks/months
❌ **Excessive progression with injury history** - Conservative progression is smart, not weak
❌ **Ignoring movement quality for load** - Technique breakdown = injury risk
❌ **No prehab included** - Prevention is easier than rehabilitation
❌ **Assuming exercises are safe without checking limitations** - ALWAYS check first
❌ **Continuing contraindicated exercises** - Never worth the risk

## References

- McGill 2015 - "Low Back Disorders: Evidence-Based Prevention and Rehabilitation" (spine injury prevention)
- Cools et al. 2007 - "Prevention of Shoulder Injuries in Overhead Athletes" (shoulder prehab strategies)
- Hewett et al. 2005 - "Biomechanical Measures of Neuromuscular Control and Valgus Loading of the Knee Predict ACL Injury Risk" (knee injury prevention)
- Cook et al. 2014 - "Movement: Functional Movement Systems" (movement screening, injury risk)
- Boyle 2016 - "New Functional Training for Sports" (prehab exercises, injury prevention strategies)
- ACSM 2009 - "Progression Models in Resistance Training for Healthy Adults" (safe progression guidelines)
