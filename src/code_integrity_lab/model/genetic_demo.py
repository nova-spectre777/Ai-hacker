"""Genetic algorithm demo optimizing a toy threshold; not a security detector."""
from __future__ import annotations

import random
from typing import Any


def evolve_threshold(generations: int = 30) -> dict[str, Any]:
    """Optimize a one-dimensional threshold on synthetic labels using a simple genetic search."""
    if not isinstance(generations, int) or not 1 <= generations <= 200:
        raise ValueError("generations must be an integer between 1 and 200")

    rng = random.Random(13)
    data = [(index / 100, int(index / 100 >= 0.65)) for index in range(101)]
    population = [rng.random() for _ in range(24)]

    def fitness(threshold: float) -> float:
        correct = sum(int((value >= threshold) == bool(label)) for value, label in data)
        return correct / len(data)

    history: list[float] = []
    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        history.append(round(fitness(population[0]), 4))
        next_population = population[:4]
        while len(next_population) < 24:
            parent = rng.choice(population[:10])
            mutated = min(1.0, max(0.0, parent + rng.gauss(0, 0.08)))
            next_population.append(mutated)
        population = next_population

    best = max(population, key=fitness)
    return {
        "best_threshold": round(best, 4),
        "fitness": round(fitness(best), 4),
        "generations": generations,
        "history": history,
        "warning": "Toy optimization only; not a vulnerability detector.",
    }
