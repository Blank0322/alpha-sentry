# Execution Sentry Playbook

This playbook defines how Alpha-Sentry moves from **signal** to **actionable execution prep**.

## 1) Intake

- source link / source channel
- timestamp
- raw message

## 2) Triage

- actionable? (yes/no)
- kind (listing / launch / campaign / other)
- reason (short)

## 3) Action Plan

If actionable, generate an execution plan with:
- urgency (`low/medium/high`)
- ETA (minutes)
- checklist

## 4) Human gate (mandatory)

Execution Sentry is **decision-support**, not auto-execution.
Before any trade/task:
1. confirm source authenticity
2. confirm risk limits
3. explicit human approval

## 5) Post-action logging

- action taken
- outcome
- what changed
- what to automate next
