from itertools import islice
from typing import Callable, Tuple, TypeAlias, cast
from random import randrange

from typing_extensions import reveal_type

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


def scale_and_round(state: GameState, drawn_num: int, max_num: int) -> bool:
    """Strategy that scales the drawn number w.r.t. the number of slots and the maximum.

    "Is probability density uniform? If so, just scale to 1-20 and round to closest empty cell(if possible), I would assume."

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


def recursive_strategy(state: GameState, drawn_num: int, max_num: int) -> bool:
    """Not actually a recursive algorithm just based off a recursive idea.

    The first number that's drawn should be placed in a position proportional to its value so for
    20 slots if you drew 300 then you ought to place it in #7. This makes it so that the number
    of slots for numbers less than 300 is proportional to the probability of picking such a number and
    likewise for numbers > 300

    And then we recurse, if the next number we draw is 500 then the range we're going to place it in is 300 to 1000.
    500 is (500-300)/(1000-300) ~ .28 along the way between 300 and 1000 so 500 should be placed .28 of the way
    between slot 8 and slot 20 something like (.72*8+.28*20) = 11.36 so slot 11

    From https://www.reddit.com/r/compsci/comments/1354n5h/comment/jii2h6u/?utm_source=share&utm_medium=web2x&context=3
    """

    # range of slots to place drawn number in
    lower_slot_bound = -1
    upper_slot_bound = -1
    for slot, num in enumerate(state):
        if upper_slot_bound != -1:
            break

        if num is None:
            continue

        if num < drawn_num:
            lower_slot_bound = slot

        if upper_slot_bound == -1 and num > drawn_num:
            upper_slot_bound = slot

    num_slots = len(state)
    if upper_slot_bound == -1:
        upper_slot_bound = num_slots

    # Make the bounds inclusive
    lower_slot_bound += 1
    upper_slot_bound -= 1

    if upper_slot_bound - lower_slot_bound <= 1:
        return False

    if upper_slot_bound == 0 or lower_slot_bound == num_slots - 1:
        return False

    try:
        lower_num = state[lower_slot_bound - 1]
    except IndexError:
        lower_num = 0

    try:
        upper_num = state[upper_slot_bound + 1]
    except IndexError:
        upper_num = max_num

    if lower_num is None:
        lower_num = 0
    if upper_num is None:
        upper_num = max_num

    relative_distance = (drawn_num - lower_num) / (upper_num - lower_num)

    slot = round(relative_distance * (upper_slot_bound - lower_slot_bound) + lower_slot_bound)

    if state[slot] is not None:
        return False

    state[slot] = drawn_num

    return True


if __name__ == "__main__":
    (
        succeeded,
        final_state,
        drawn_nums,
    ) = game(strategy=recursive_strategy)
    round_num = len(drawn_nums)
    print(f"made it to round  #{round_num}")
