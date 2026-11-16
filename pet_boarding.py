"""Pet boarding helpers, hardened against invalid input (found by fuzzing).

Every function returns None when its input is invalid instead of raising.
"""
import math


def parse_booking(text):
    """Parse 'pet:days' into (Pet, days). Return None if invalid.

    Invalid: not a string, not exactly one ':', empty pet name, days that
    are not a number, are NaN/infinite, or are negative.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    pet = parts[0].strip()
    if not pet:
        return None
    try:
        days = float(parts[1])
    except ValueError:
        return None
    if not math.isfinite(days) or days < 0:
        return None
    return pet.title(), days


def stay_average(days_csv):
    """Average (rounded down) of comma-separated stay lengths. None if invalid.

    Invalid: not a string, any element that is not a whole number
    (including empty elements) or any negative stay length.
    """
    if not isinstance(days_csv, str):
        return None
    try:
        values = [int(r) for r in days_csv.split(',')]
    except ValueError:
        return None
    if any(v < 0 for v in values):
        return None
    return sum(values) // len(values)


def payable_fee(text):
    """Return fee * 1.18 - discount (never below 0) for 'fee|discount'.

    Returns None if invalid: not a string, not exactly one '|', non-numeric,
    NaN/infinite or negative values, or a result that overflows.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        fee = float(parts[0])
        discount = float(parts[1])
    except ValueError:
        return None
    if not (math.isfinite(fee) and math.isfinite(discount)):
        return None
    if fee < 0 or discount < 0:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0.0)


def main():
    """Interactive demo of the three helpers."""
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result if result is not None else "Invalid input")

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
