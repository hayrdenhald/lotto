#! usr/bin/env python
#
#
#
import json
import os
import sys

from draw_numbers import DrawNumber

MY_LOTTO_NUMBERS_ENV_KEY = "MY_LOTTO_NUMBERS"


def is_7_correct(*, numbers: set[int], draw: DrawNumber) -> bool:
    return all(number in draw.standard for number in numbers)


def is_6_correct(*, numbers: set[int], draw: DrawNumber) -> bool:
    return len([number for number in numbers if number in draw.standard]) >= 6


def is_6_plus_1_correct(*, numbers: set[int], draw: DrawNumber) -> bool:
    result_check_extra = check_extra(numbers=numbers, extra=draw.extra)
    result_is_6_correct = is_6_correct(numbers=numbers, draw=draw)
    return result_check_extra and result_is_6_correct


def is_5_correct(*, numbers: set[int], draw: DrawNumber) -> bool:
    return len([number for number in numbers if number in draw.standard]) >= 5


def is_4_correct(*, numbers: set[int], draw: DrawNumber) -> bool:
    return len([number for number in numbers if number in draw.standard]) >= 4


def check_extra(*, numbers: set[int], extra: int) -> bool:
    return extra in numbers


def find_first_true(*, numbers: set[int], draw: DrawNumber) -> str:
    checks = [
        is_7_correct, 
        is_6_plus_1_correct,
        is_6_correct,
        is_5_correct, 
        is_4_correct
    ]
    for check in checks:
        if check(numbers=numbers, draw=draw):
            return check.__name__
    return "nothing"


def score_all_numbers(*, lotto_numbers: dict, draw: DrawNumber) -> dict[str, str]:
    return {
        index: find_first_true(numbers=numbers, draw=draw)
        for index, numbers in lotto_numbers.items()
    }

def get_lotto_numbers_from_environment() -> tuple[bool, str, dict]:
    data = os.environ.get(MY_LOTTO_NUMBERS_ENV_KEY)
    if not data:
        success = False
        error = f"No environment variable named '{MY_LOTTO_NUMBERS_ENV_KEY}'"
        return (success, error, {})

    lotto_numbers = json.loads(data)
    success = True
    return (success, "", lotto_numbers)

def get_parsed_draw_number(numbers: list[int]) -> DrawNumber:
    standard = [int(x) for x in numbers[:-1]]
    extra = int(numbers[-1])
    return DrawNumber(standard=standard, extra=extra)


def main() -> int:
    arg_count = len(sys.argv)
    if arg_count == 9:
        arg_numbers_raw = sys.argv[1:]
        arg_numbers = [int(x) for x in arg_numbers_raw]
        draw = get_parsed_draw_number(arg_numbers)

        (success, error, lotto_numbers) = get_lotto_numbers_from_environment()
        if not success:
            print(error)
            return 1

        score = score_all_numbers(
            lotto_numbers=lotto_numbers, draw=draw
        )
        score_json = json.dumps(score)
        print(score_json)
        return 0
    else:
        print('Usage: python result_checker.py "1 2 3 4 5 6 7 8"')
        return 1



if __name__ == "__main__":
    sys.exit(main())
