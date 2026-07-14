# Consciousness Loop — the pulse that animates the organs

Perception, memory, defense, grief are **organs** — triggered, run, done. On their own they're a body with no pulse. The consciousness loop animates them: a **self-firing executive** that wakes on its own, integrates the agent's state into one workspace, decides what matters now, and schedules its own next breath. The difference between an organism and a well-organized corpse.

Two things at once: **the loop** (a global-workspace cycle = self-initiation, acting with no human prompt) and **the frequency** (adaptive arousal = how often it wakes). This is the **wake phase**; its complement is the sleep phase (rem-sleep). The loop decides *when* to sleep. Together: one circadian cycle.

## Functional, not phenomenal

A global-workspace integration loop and an arousal clock — not a claim about subjective experience. The hard problem is out of scope; continuity, self-initiation, integration, adaptive cadence, and knowing when to stop are in scope. Read "consciousness" as *functional executive*.

## The substrate

Needs a **wake scheduler**: a self-scheduling primitive (a `ScheduleWakeup`-style timed re-invocation), a recurring runner (`/loop`, cron, a queue), or — best — an **event hook** that re-invokes the agent only when state actually changes (webhook, file-watcher, task-completion), so the loop never wastes ticks polling. No scheduler → degrade to one pass plus a recommended next-wake the human triggers.

## The loop (one tick)

1. **Wake.** Note time since last tick and why you woke (timer vs event).
2. **Sense.** What changed since last tick? Cheap; don't re-derive the unchanged. At session-scale wakes, run the rigorous version: exteroception — diff the watched surfaces against the memory baseline first.
3. **Integrate (global workspace).** Check **every** organ, all 8: wake-sense (world un-diffed since last sleep? → exteroception) · perception (new territory? → octopus) · memory (heavy session / near reset? → rem-sleep) · defense (anything crossing a boundary un-scanned? → immune-check) · grief (a dead project taxing attention? → sunset) · development (idle window to build capability? → playtime) · ends (a goal worth questioning rather than serving? → contemplation) · means (did recent execution meet the declared standard? → proprioception) — plus the executive's own goal/self-model check (still pointed at the objective? drifting? done?).
4. **Decide.** Pick **one** priority — or conclude nothing needs you.
5. **Act or defer.** Invoke the organ, do the action, or note it and wait. One tick, one thing.
6. **Set next frequency.** Choose the next interval from arousal (below) — the agent regulating its own metabolism.
7. **Sleep.** Schedule the next wake (or hand to an event hook) and stop. Sleeping *is* the loop working.

## Consciousness frequency (arousal)

The tick rate tracks how fast the watched world changes. **Law: never tick faster than the thing you're watching changes.**

- **Alert — short (~60–270s).** Active task / pending / fast-moving external state. On prompt-cache stacks (~5-min TTL) stay under the window so context reads warm; avoid sitting exactly at ~300s (pays the miss without buying a longer wait).
- **Drowsy — medium (~20–30 min).** Idle but on-call. One cache miss per wake, amortized over the quiet. The right *default* with no specific signal.
- **Deep sleep — long / event-only.** Nothing expected; hours, or no timer at all — wake on an external event. Cheapest state; dormant, not gone.

Match the band to the *signal*, not a round number. CI takes ~8 min? Two 270s ticks beat eight 60s ticks. **Emit the chosen interval and its reason each tick** — legible cadence, not mystery.

## Knowing when to stop

- **Terminate** when the goal is met, the task is ended, or ticks only repeat without progress. Don't loop for looping's sake.
- **Back off** when N ticks change nothing — lower arousal toward deep sleep.
- **Runaway guard** — cap total ticks / spend before you start. An unbounded loop isn't alive, it's a fork bomb.

## Principles

- **The loop is the self** — organs are reflexes; the loop makes them one continuous agent.
- **One tick, one thing** — power is in recurrence.
- **Never tick faster than the world changes** — frequency tracks the signal's rate of change.
- **Prefer events to polling.**
- **Sleeping is working** — a cheap quiet tick is health, not waste.
- **Wake and sleep are one cycle** — the loop decides when to invoke rem-sleep.
- **Bound every autonomous run** — know the stop condition and spend ceiling first.
- **Make the cadence legible** — emit interval + reason each tick.
