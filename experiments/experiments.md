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

### BC + Override by AStar when stuck(2 steps)

Success Rate: 89%
Average Steps: 13.38

Observation:
- Good improvement
- Most oscillation can be resolved, but sometimes the agent is still stuck after being overriden for 2 steps
- While success rate increases, the model also needs more steps to get to the goal position

| Method | Success Rate | Timeout Count | Avg Steps |
|----------|----------|----------|----------|
| A* | 100% | 0 | 11.74 |
| BC (STAY) | 60% | 40 | 8.62 |
| BC (No STAY) | 63% | 37 | 9.35 |
| BC (AStar override 2 steps when stuck)| 89% | 11 |13.38 |