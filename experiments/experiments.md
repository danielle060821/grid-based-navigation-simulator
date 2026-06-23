# Experiment Log

## 2026-06-23

### Baseline BC (STAY allowed)

Success Rate: 60%
Average Steps: 8.62

Observation:
- Frequently gets stuck near corners
- Sometimes predicts STAY repeatedly

---

### BC + No STAY

Success Rate: 63%
Average Steps: 9.35

Observation:
- Slight improvement
- STAY replaced by oscillation

Conclusion:
- STAY is not the dominant failure reason



| Method | Success Rate | Timeout | Avg Steps |
|----------|----------|----------|----------|
| A* | 100% | 0 | 11.74 |
| BC (STAY) | 60% | 40 | 8.62 |
| BC (No STAY) | 63% | 37 | 9.35 |