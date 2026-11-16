# L7_49 - Pet Boarding

Lab 7: Fuzz Testing with Hypothesis

**Name:** Rishaan Deen | **SRN:** PES2UG24AM134

## Files

| File | Description |
|------|-------------|
| `pet_boarding.py` | The code under test (hardened after fuzzing) |
| `test_pet_boarding.py` | Hypothesis fuzz and property tests (10 tests) |
| `Lab7_Fuzzing_Report.pdf` | PDF with the screenshots for every step |
| `screenshots/` | The individual screenshots |

## Results

| Stage | Result |
|-------|--------|
| Original script, fuzz tests | 7 failed, 3 passed |
| Fixed script, fuzz tests | **10 passed** |

Invalid input now returns `None` instead of raising. See the PDF for the bugs found and the fix for each.
