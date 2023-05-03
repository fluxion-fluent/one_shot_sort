from one_shot_sort import Results, game, scale_and_round, recursive_strategy

strategies = (recursive_strategy, scale_and_round)


def benchmark(num_slots: int = 20, max_num=999, num_samples=1000000):
    strat_to_results: dict[str, list[Results]] = {
        strat.__name__: [game(num_slots, max_num, strat) for _ in range(num_samples)] for strat in strategies
    }

    print(f"Number of samples: {num_samples}")
    print()
    for strat, results in strat_to_results.items():
        num_successes = sum(res.success for res in results)
        print(f"{strat} results:")
        print(f"Number of successes: {num_successes}")
        print(f"Rate of success: {num_successes/num_samples}")
        print(f"Average round reached: {sum(len(res.drawn_nums) for res in results) / num_samples}")
        print()


if __name__ == "__main__":
    benchmark()
