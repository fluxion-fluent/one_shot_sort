from typing import Callable, Tuple, TypeAlias, cast
from random import randrange

GameState: TypeAlias = list[int | None]

Strategy: TypeAlias = Callable[[GameState, int], bool]


def manual_strategy(state: GameState, drawn_num: int) -> bool:
    """Strategy that asks the user to place the drawn number in a slot.
    Returns False if a valid choice is impossible, True otherwise."""
    valid_choice = False

    while not valid_choice:
        print(f"Drawn number: {drawn_num}")
        print("Enter the slot number to place the drawn number.")
        choice = input("Or enter -1 if a valid choice is impossible: ")
        slot = int(choice)

        if slot == -1:
            return False
        elif slot < 0 or slot >= len(state):
            print(f"Invalid slot number. Please pick a number between 0 and {len(state) - 1}")
        elif state[slot] is not None:
            print(f"Slot {slot} is already filled. Please pick another slot.")
        else:
            state[slot] = drawn_num
            return True

    return False


def game(
    num_slots: int = 20,
    max_num: int = 999,
    strategy: Strategy = manual_strategy,
    print_state: bool = True,
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
        strategy_succeeded = strategy(state, rand_num)

    return strategy_succeeded and is_winning_state(state), state, rand_nums


def is_winning_state(state: GameState) -> bool:
    if not all(state):
        return False

    not_none_state = cast(list[int], state)

    if sorted(not_none_state) == not_none_state:
        return True

    return False


if __name__ == "__main__":
    game()
