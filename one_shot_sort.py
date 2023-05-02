from itertools import islice
from typing import Callable, Tuple, TypeAlias, cast
from random import randrange

GameState: TypeAlias = list[int | None]

Strategy: TypeAlias = Callable[[GameState, int, int], bool]


def manual_strategy(state: GameState, drawn_num: int, max_num: int) -> bool:
    """Strategy that asks the user to place the drawn number in a slot.
    Returns False if a valid choice is impossible, True otherwise."""
    print(f"Max number: {max_num}")
    round_num = 0
    while True:
        round_num += 1
        print(f"Round {round_num}")
        print(f"Drawn number: {drawn_num}")
        print("Enter the slot number to place the drawn number into.")

        try:
            slot = int(input("Or enter -1 if a valid choice is impossible: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if slot == -1:
            return False
        elif slot < 0 or slot >= len(state):
            print(f"Invalid slot number. Please pick a number between 0 and {len(state) - 1}")
        elif state[slot] is not None:
            print(f"Slot {slot} is already filled. Please pick another slot.")
        else:
            state[slot] = drawn_num
            return True


def game(
    num_slots: int = 20,
    max_num: int = 999,
    strategy: Strategy = manual_strategy,
    print_state: bool = False,
    num_generator: Callable[[int], int] = randrange,
) -> Tuple[bool, GameState, list[int]]:
    state: GameState = [None] * num_slots
    rand_nums = []
    strategy_succeeded = True
    while not is_winning_state(state) and strategy_succeeded:
        if print_state:
            for i, num in enumerate(state):
                print(i, num or "")

        rand_num = num_generator(max_num + 1)
        while rand_num in rand_nums:
            rand_num = num_generator(max_num + 1)

        rand_nums.append(rand_num)
        strategy_succeeded = strategy(state, rand_num, max_num)

    return strategy_succeeded and is_winning_state(state), state, rand_nums


def is_winning_state(state: GameState) -> bool:
    if not all(state):
        return False

    not_none_state = cast(list[int], state)

    if sorted(not_none_state) == not_none_state:
        return True

    return False


def scale_and_round(state: GameState, drawn_num: int, max_num: int = 1000) -> bool:
    """Strategy that scales the drawn number w.r.t. the number of slots and the maximum.

    From https://www.reddit.com/r/compsci/comments/1354n5h/comment/jii1xtu/?utm_source=share&utm_medium=web2x&context=3
    """
    num_slots = len(state)
    chosen_slot = round(drawn_num * (num_slots / max_num))

    for slot, num in islice(enumerate(state), chosen_slot, num_slots):
        if num is None:
            state[slot] = drawn_num
            return True
        elif drawn_num < num:
            return False

    return False


if __name__ == "__main__":
    (
        succeeded,
        final_state,
        drawn_nums,
    ) = game(strategy=scale_and_round)
    round_num = len([num for num in final_state if num is not None])
    print(f"made it ito {round_num} rounds")
