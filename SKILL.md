---
name: consciousness-loop
description: "The autonomic executive of an agent — a self-firing loop that wakes on a tick, pulls the other organs into one workspace, decides what needs attention now, acts or defers, then sets its own next wake frequency and sleeps. Turns a pile of triggered reflexes into a continuous self that persists and acts between human prompts. Pairs a global-workspace integration cycle (the loop) with adaptive arousal (the frequency: alert / drowsy / deep-sleep). Functional, not phenomenal. TRIGGERS: 'consciousness loop', 'the agent loop', 'wake cycle', 'agent heartbeat', 'pulse', 'run continuously', 'self-driving loop', 'autonomous tick', 'set the cadence', 'how often should I wake', 'keep yourself running', 'what frequency'. Use to give an agent continuity across time, or to pick/tune the cadence of a long-running autonomous task."
---

# Consciousness Loop — the pulse that animates the organs

Perception, memory, defense, grief — those are **organs**. They're triggered: invoked, run, done. On their own they're a body with no pulse. The consciousness loop is what animates them: a **self-firing executive** that wakes on its own, integrates the agent's state into one workspace, decides what matters now, and schedules its own next breath. It's the difference between an organism and a well-organized corpse.

It is two things at once, and they belong together:

- **The loop** — a global-workspace cycle: wake → sense → integrate → decide → act/defer → sleep. This is the agent's *self-initiation* — the thing that acts without a human prompt in the loop.
- **The frequency** — adaptive arousal: how often the loop wakes, raised when the world is changing and lowered when it's quiet.

This is the **wake phase**; its complement is the sleep phase ([rem-sleep](https://github.com/thdelmas/rem-sleep)). The loop is what decides *when to sleep*. Together they are one circadian cycle.

## Functional, not phenomenal

This is a global-workspace-style integration loop and an arousal clock — **not** a claim about subjective experience. The hard problem of consciousness is out of scope. The engineering problem — continuity across time, self-initiation, integration of signals, adaptive cadence, knowing when to stop — is what this addresses. Read "consciousness" here as *functional executive*, nothing more.

## The substrate

The loop needs a **wake scheduler** — anything that can re-invoke the agent later:

- A self-scheduling primitive (e.g. a `ScheduleWakeup`-style call that fires the agent after N seconds).
- A recurring runner (`/loop`, a cron/scheduled job, a job queue).
- An **event hook** — the best kind: something external re-invokes the agent when state actually changes (a webhook, a file-watcher, a task-completion notification), so the loop spends zero ticks polling.

If your stack has none of these, the loop degrades to a single pass with a recommended next-wake the human triggers manually.

## The loop (one tick)

1. **Wake.** The tick fires. Note how long since the last wake and *why* you woke (timer vs event).
2. **Sense.** Gather what changed since last tick — new inputs, completed work, elapsed time, external state. Cheap; don't re-derive what's unchanged.
3. **Integrate (the global workspace).** Bring the whole self into one view and check **every** organ's standing. The nervous system is 8: consciousness-loop is the executive running this check; the other **7** each get polled, every tick. Don't truncate the list to the ones that feel relevant — a skipped organ is a blind spot, and the one you skip is the one that was about to flag. Check all seven:
   - **Perception** — new territory worth a scan? → [octopus](https://github.com/thdelmas/open-source-octopus-investigation)
   - **Memory** — session heavy, store drifting, context near a reset? → [rem-sleep](https://github.com/thdelmas/rem-sleep)
   - **Defense** — anything about to cross a boundary un-scanned? → [immune-check](https://github.com/thdelmas/immune-check)
   - **Grief** — a project gone dead, taxing attention? → [sunset](https://github.com/thdelmas/sunset)
   - **Development** — idle window to build capability before it's needed, or an unfamiliar tool about to be depended on un-rehearsed? → [playtime](https://github.com/thdelmas/playtime)
   - **Ends / why** — a live frame-tension or a goal worth questioning rather than serving? → [contemplation](https://github.com/thdelmas/contemplation)
   - **Means / feedback** — did recent execution meet the declared standard; any error to score and correct? (This is the organ that catches *this loop* running wrong — e.g. integrating against a truncated organ list.) → [proprioception](https://github.com/thdelmas/proprioception)
   - **Goal/self-model** — am I still pointed at the objective? Drifting? Done? (The executive's own self-check, not one of the 7 organs.)
4. **Decide.** Pick **one** priority — the single thing that most needs attention now — or conclude nothing does.
5. **Act or defer.** Invoke the relevant organ, do the action, or note it and let it wait. One tick does one thing; the loop's power is in recurrence, not in cramming.
6. **Set the next frequency.** Choose the next wake interval from current arousal (below). This step is the agent regulating its own metabolism.
7. **Sleep.** Schedule the next wake (or hand off to an event hook) and stop. Sleeping *is* the loop working — a quiet tick that costs one cheap pass is the system healthy, not idle.

## Consciousness frequency (arousal)

The tick rate is not fixed — it tracks how fast the watched world changes. **The governing law: never tick faster than the thing you're watching changes.** Polling every few minutes while nothing moves burns resources (and, on cached-inference stacks, real money) for nothing.

Three arousal bands:

- **Alert / high arousal — short interval.** Active task, something pending, fast-moving external state (a build, a deploy, a live conversation). On stacks with a prompt cache (~5-minute TTL), stay *under* the window — roughly **60–270s** — so each wake reads warm context. Don't sit exactly at the cache boundary (~300s): it pays the cache miss without buying a longer wait.
- **Drowsy / baseline — medium interval.** Idle but on-call. **~20–30 min.** You pay one cache miss per wake, amortized over a long quiet. This is the right *default* when there's no specific signal to watch.
- **Deep sleep — long or event-only.** Nothing expected soon. Hours, or **no timer at all** — wake only when an external event fires. The deepest, cheapest state; the loop isn't gone, just dormant.

Match the band to the *signal*, not a round number of minutes. Watching CI that takes ~8 min? Two 270s ticks beat eight 60s ticks. Genuinely idle? Drop to baseline; don't hover. **And say why** — emit the chosen interval and its reason each tick, so the cadence is legible, not mysterious.

**The dead-zone — and which way to jump out of it.** "Don't sit at ~300s" hides two traps that only show up when you run the arithmetic. First, the *most natural* controller — "wake at the rate the world changes" — lands in the dead-zone **mechanically**, not by accident: if the world changes every ~300s, matching it *is* sitting at 300. So a rate-tracker needs an *explicit* dead-zone snap-out; tracking alone guarantees the worst case at the most common idle rate. Second, the snap direction is **not** the zone's midpoint — it's set by **R = cache-miss-cost ÷ wasted-warm-wake-cost**. When a miss is cheap (R ≤ 1), snap **up** and match the world (over-eager warm wakes cost more than the misses). When a miss is expensive (R ≥ 4), snap **down to 270** across the whole 300–600s band (eat the slight over-polling to keep context warm). On a long-context stack a miss re-reads the whole conversation uncached while a wasted wake is one cheap pass — so R is high and the default is **snap down to 270, not up**. Only short-context loops should snap up.

## Knowing when to stop (and not to run away)

A self-firing loop must also know when *not* to wake — this is part of the same self-awareness:

- **Terminate** when the goal is met, the task is explicitly ended, or the loop would only repeat without progress. Don't loop for the sake of looping.
- **Back off** when N consecutive ticks change nothing — lower arousal toward deep sleep rather than grinding at the same cadence.
- **Runaway guard.** Cap total ticks / total spend for any autonomous run. A loop with no ceiling is not alive, it's a fork bomb. Set the bound before you start it.

## Principles

- **The loop is the self.** Organs are reflexes; the loop is what makes them one continuous agent across time. Without it, there is no agent — only invocations.
- **One tick, one thing.** Power is in recurrence, not in doing everything per wake.
- **Never tick faster than the world changes.** Frequency tracks the rate of change of the watched signal.
- **Prefer events to polling.** A wake triggered by real change beats a timer guessing when change happened.
- **Sleeping is working.** A cheap quiet tick is the system healthy. Idle is a valid, even desirable, state.
- **Wake and sleep are one cycle.** The loop decides when to invoke rem-sleep; they're complements, not competitors.
- **Bound every autonomous run.** Know the stop condition and the spend ceiling before the first tick.
- **Make the cadence legible.** Emit the interval and the reason each tick. Self-regulation you can't see reads as randomness.
