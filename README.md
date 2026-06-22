# Consciousness Loop — a Claude Code skill

The **keystone** of the [agent-nervous-system](https://github.com/thdelmas/agent-nervous-system) suite. The other organs — [perception](https://github.com/thdelmas/open-source-octopus-investigation), [memory](https://github.com/thdelmas/rem-sleep), [defense](https://github.com/thdelmas/immune-check), [grief](https://github.com/thdelmas/sunset) — are *reflexes*: triggered, run, done. On their own they're a body with no pulse. This is the pulse: a **self-firing executive loop** that wakes on its own, pulls the organs into one workspace, decides what needs attention now, and schedules its own next wake.

It's the difference between an organism and a well-organized corpse.

## Two things, paired

- **The loop** — a global-workspace cycle (wake → sense → integrate → decide → act/defer → sleep). The agent's **self-initiation**: it acts with no human prompt in the loop.
- **The frequency** — adaptive arousal. *Alert* (cache-warm, ~60–270s) when something's happening; *drowsy* (~20–30 min) when idle; *deep sleep* (long / event-only) when nothing's expected. The governing law: **never tick faster than the world you're watching changes.**

It's the **wake phase** to rem-sleep's **sleep phase** — the loop is what decides when to sleep. Two arcs of one circadian cycle.

## Functional, not phenomenal

This is a global-workspace integration loop and an arousal clock — **not** a claim about subjective experience. The hard problem is out of scope; continuity, self-initiation, integration, adaptive cadence, and knowing when to stop are in scope. Read "consciousness" as *functional executive*.

## Requirements

A **wake scheduler** — a self-scheduling primitive (a `ScheduleWakeup`-style timed re-invocation), a recurring runner (`/loop`, cron, a job queue), or, best, an **event hook** that re-invokes the agent only when state changes. With none, the loop degrades to a single pass plus a recommended next-wake the human triggers.

## Install

Works with **Claude Code**, **Codex**, and **Cursor**.

```bash
git clone https://github.com/thdelmas/consciousness-loop.git
cd consciousness-loop
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/consciousness-loop
cp SKILL.md ~/.claude/skills/consciousness-loop/
```

Invoke with `/consciousness-loop`, or say *"set the cadence"* / *"how often should I wake?"* / *"keep yourself running."*

### Codex

```bash
mkdir -p ~/.agents/skills/consciousness-loop
cp SKILL.md ~/.agents/skills/consciousness-loop/
```

### Cursor

```bash
mkdir -p ~/.cursor/commands
cp cursor/consciousness-loop.md ~/.cursor/commands/
```

## The loop (one tick)

1. **Wake** — note time since last tick and why (timer vs event).
2. **Sense** — what changed since last tick.
3. **Integrate** — check each organ + the goal/self-model.
4. **Decide** — pick one priority, or conclude nothing needs you.
5. **Act or defer** — one tick, one thing.
6. **Set the next frequency** — choose the interval from arousal.
7. **Sleep** — schedule the next wake (or hand to an event hook). Sleeping *is* the loop working.

See [`SKILL.md`](./SKILL.md) for the arousal bands, the stop conditions, and the runaway guard.

## License

MIT
