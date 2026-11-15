"""Benchmark service entry point."""

from benchmark_service import BenchmarkServiceApp

from behavior_probe_benchmark_service.benchmark_service import BehaviorProbeBenchmark

app = BenchmarkServiceApp(BehaviorProbeBenchmark)