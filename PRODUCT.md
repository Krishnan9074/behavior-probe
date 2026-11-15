# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
Static HTML/CSS/JS, one file, built by `site/build.py` from the run data and deployed to Vercel (delegated: no framework needed for one page).

## Users
AI researchers and engineers comparing models. They scan a leaderboard, check the method, and judge whether the gaps are real. (Confirmed by the owner.)

## Product Purpose
Behavior-Probe is a benchmark: a model sees a few answers from one simulated student with a hidden subtraction bug and must predict that student's next answers, with or without an optional probe tool. The public page reports results.

## Capabilities and Constraints
- Publish aggregate and per-task scores only. Hidden rules, answer keys, prompts and trajectories stay private.
- Every number on the page comes from the run data; nothing is hand-typed.

## Brand Commitments
- Name: Behavior-Probe.
- Layout follows the public AI-leaderboard convention the owner asked for (vals.ai style), without using another organisation's name, logo or assets.
