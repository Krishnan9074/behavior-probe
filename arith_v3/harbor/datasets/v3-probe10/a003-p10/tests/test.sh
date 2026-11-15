#!/bin/bash
# Runs after the agent finishes. Scores /workspace/submission.json against the answer key.
mkdir -p /logs/verifier
python3 /tests/grade.py
