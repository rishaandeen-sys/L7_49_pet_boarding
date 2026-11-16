import math

from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee


# ---------------------------------------------------------------- no-crash
# Property: no function may raise, whatever text (or None) it is given.
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:
        assert False, f"stay_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"


# ----------------------------------------------------- output-shape properties
# Property: invalid input gives None, valid input gives a sensible value.
@given(st.text() | st.none())
def test_parse_booking_result_is_sane(s):
    result = parse_booking(s)
    if result is not None:
        pet, days = result
        assert isinstance(pet, str) and pet != ""
        assert math.isfinite(days) and days >= 0


@given(st.text() | st.none())
def test_stay_average_result_is_sane(s):
    result = stay_average(s)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.text() | st.none())
def test_payable_fee_result_is_sane(s):
    result = payable_fee(s)
    assert result is None or (math.isfinite(result) and result >= 0)


# --------------------------------------------------------- valid-input checks
@given(st.text(alphabet=st.characters(whitelist_categories=("L",)), min_size=1),
       st.integers(min_value=0, max_value=10_000))
def test_parse_booking_valid_roundtrip(pet, days):
    result = parse_booking(f"{pet}:{days}")
    assert result == (pet.strip().title(), float(days))


@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1))
def test_stay_average_valid_values(values):
    csv = ",".join(str(v) for v in values)
    assert stay_average(csv) == sum(values) // len(values)


@given(st.integers(min_value=0, max_value=1_000_000),
       st.integers(min_value=0, max_value=1_000_000))
def test_payable_fee_valid_values(fee, discount):
    expected = max(fee * 1.18 - discount, 0)
    assert math.isclose(payable_fee(f"{fee}|{discount}"), expected)


# ------------------------------------------------------ known edge cases found
def test_known_bad_inputs_return_none():
    assert parse_booking("dog5") is None          # no colon
    assert parse_booking("dog:5:6") is None       # too many colons
    assert parse_booking(":5") is None            # empty pet name
    assert parse_booking("dog:nan") is None       # NaN days
    assert parse_booking("dog:-3") is None        # negative days
    assert stay_average("2,,7") is None           # empty element
    assert stay_average("") is None               # empty string
    assert payable_fee("1500") is None            # missing discount
    assert payable_fee("nan|0") is None           # NaN fee
    assert payable_fee("inf|0") is None           # infinite fee
