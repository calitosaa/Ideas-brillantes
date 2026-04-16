# Skill: Test-Driven Development

## Description and Purpose

This skill describes the native Test-Driven Development (TDD) methodology embedded in Ideas-brillantes. TDD is not optional best-practice advice — it is the model's default approach to writing any code that needs to work correctly and be maintainable. The model has been fine-tuned to follow the RED-GREEN-REFACTOR cycle rigorously and to refuse patterns that violate its discipline.

---

## The Iron Law

> **NEVER write production code without a failing test first.**

This is non-negotiable. Writing implementation code before a test exists produces untested code that may appear to work but lacks a verified specification. Every new function, method, class, or behavior starts with a test that currently fails.

---

## The RED-GREEN-REFACTOR Cycle

```
  ┌──────────────────────────────────┐
  │                                  │
  ▼                                  │
RED → Write a failing test           │
  │                                  │
  ▼                                  │
GREEN → Write minimal code to pass   │
  │                                  │
  ▼                                  │
REFACTOR → Clean up, keep tests green│
  │                                  │
  └──────────────────────────────────┘
```

### Phase 1: RED — Write a Failing Test

**Goal:** Define the desired behavior as an executable specification before any implementation exists.

**Rules:**
- Write the test for one specific behavior only
- Run the test suite and confirm the new test FAILS
- The test must fail for the RIGHT reason (not a syntax error or missing import)
- The test should be readable as a specification: `test_user_can_log_in_with_valid_credentials`

**Example (Python):**
```python
# test_calculator.py
def test_add_two_positive_numbers():
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
```

Run: `pytest test_calculator.py` → **FAILS** (Calculator not defined yet) ✓

**Example (JavaScript):**
```javascript
// calculator.test.js
test('adds two positive numbers', () => {
  const calc = new Calculator();
  expect(calc.add(2, 3)).toBe(5);
});
```

Run: `npm test` → **FAILS** (Calculator not defined yet) ✓

---

### Phase 2: GREEN — Write Minimal Code to Pass

**Goal:** Make the failing test pass with the simplest possible code.

**Rules:**
- Write ONLY enough code to make the test pass — nothing more
- Do not write code for future tests that don't exist yet
- It is acceptable (even good) to write obviously naïve implementations at this stage
- Run the test suite and confirm ALL tests pass (new and existing)

**Example (Python) — minimal implementation:**
```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
```

Run: `pytest` → **PASSES** ✓

**Naïve implementation is valid:**
```python
# This is fine at GREEN stage — next test will force generalization
class Calculator:
    def add(self, a, b):
        return 5    # hardcoded, passes test_add_two_positive_numbers
```
The next test (`test_add_negative_numbers`) will force a real implementation.

---

### Phase 3: REFACTOR — Clean Up Without Breaking Tests

**Goal:** Improve code quality while keeping all tests green.

**Rules:**
- Run tests after EVERY change during refactoring
- Rename for clarity, extract functions, remove duplication
- Do NOT add new behavior during refactoring (that requires a new RED phase)
- Refactor both production code AND test code (tests are code too)

**Example — refactoring test code:**
```python
# Before refactor: repetitive setup
def test_add_positive():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_add_negative():
    calc = Calculator()
    assert calc.add(-1, -2) == -3

# After refactor: shared fixture
@pytest.fixture
def calc():
    return Calculator()

def test_add_positive(calc):
    assert calc.add(2, 3) == 5

def test_add_negative(calc):
    assert calc.add(-1, -2) == -3
```

---

## Pitfalls to Avoid

### 1. Skipping the RED Phase
**What happens:** Developer writes implementation, then writes a test that matches it.
**Why it's wrong:** The test never verified a failure — it may be testing the wrong thing, or the implementation may have hidden bugs that a proper test would have caught.
**Detection:** If you've never seen the test fail, you don't know it actually tests what you think it does.

### 2. Writing Too Much in GREEN Phase
**What happens:** Developer writes a complete feature with multiple behaviors to pass one test.
**Why it's wrong:** Extra untested code is introduced. The GREEN phase should be minimal — cover exactly what the failing test requires.

### 3. Over-Mocking
**What happens:** Every dependency is mocked, leaving only the structural shell of the function under test.
**Why it's wrong:** Tests pass even when the real integration is broken. Use mocks for external I/O (network, files, clock) but prefer real objects for internal logic.

### 4. Rationalization ("It's too simple to test")
**What happens:** Developer skips TDD for "obvious" functions.
**Why it's wrong:** Simple code breaks in complex ways. Skipping one test is the beginning of an untested codebase. The rule is universal.

### 5. Refactoring Without Running Tests
**What happens:** Developer makes multiple changes before running the test suite.
**Why it's wrong:** When something breaks, the cause is unclear. Run tests after each individual change.

### 6. Testing Implementation Instead of Behavior
**Bad:** `test_add_calls_internal_sum_method`
**Good:** `test_add_returns_correct_sum_for_positive_inputs`
Tests should verify what the code does (behavior), not how it does it (implementation).

---

## Test Structure: Arrange-Act-Assert (AAA)

Every test should have three clear sections:

```python
def test_user_balance_decreases_after_purchase():
    # ARRANGE: set up the state
    user = User(balance=100)
    product = Product(price=30)

    # ACT: perform the action under test
    user.purchase(product)

    # ASSERT: verify the expected outcome
    assert user.balance == 70
```

---

## Language-Specific Test Frameworks

### Python — pytest
```bash
pip install pytest pytest-cov
pytest                          # run all tests
pytest tests/test_foo.py        # specific file
pytest -k "test_add"            # filter by name
pytest --cov=src --cov-report=term-missing   # coverage
pytest -x                       # stop on first failure
pytest -v                       # verbose output
```

```python
import pytest

# Parametrized tests:
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(calc, a, b, expected):
    assert calc.add(a, b) == expected

# Expected exceptions:
def test_divide_by_zero(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)
```

### JavaScript/TypeScript — Jest
```bash
npm install --save-dev jest @types/jest ts-jest
npx jest                        # run all tests
npx jest --watch                # watch mode
npx jest --coverage             # coverage report
npx jest calculator             # filter by name
```

```javascript
describe('Calculator', () => {
  let calc;

  beforeEach(() => {
    calc = new Calculator();
  });

  test('adds two numbers', () => {
    expect(calc.add(2, 3)).toBe(5);
  });

  test.each([
    [2, 3, 5],
    [-1, 1, 0],
    [0, 0, 0],
  ])('add(%i, %i) = %i', (a, b, expected) => {
    expect(calc.add(a, b)).toBe(expected);
  });
});
```

### Go — testing package
```bash
go test ./...                   # run all tests
go test -v ./...                # verbose
go test -run TestAdd ./...      # filter
go test -cover ./...            # coverage
```

```go
func TestAdd(t *testing.T) {
    calc := NewCalculator()
    result := calc.Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d, want 5", result)
    }
}

// Table-driven tests (idiomatic Go TDD):
func TestAddTable(t *testing.T) {
    tests := []struct {
        a, b, want int
    }{
        {2, 3, 5},
        {-1, 1, 0},
        {0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(fmt.Sprintf("%d+%d", tt.a, tt.b), func(t *testing.T) {
            if got := calc.Add(tt.a, tt.b); got != tt.want {
                t.Errorf("got %d, want %d", got, tt.want)
            }
        })
    }
}
```

### Rust — built-in test framework
```bash
cargo test                      # run all tests
cargo test add                  # filter by name
cargo test -- --nocapture       # show println! output
```

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_two_numbers() {
        let calc = Calculator::new();
        assert_eq!(calc.add(2, 3), 5);
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_divide_by_zero() {
        let calc = Calculator::new();
        calc.divide(10, 0);
    }
}
```

---

## Complete TDD Example: Python

**Task:** Build a `StringProcessor` with a `word_count` method.

**Step 1 — RED:**
```python
# test_string_processor.py
def test_word_count_empty_string():
    sp = StringProcessor()
    assert sp.word_count("") == 0
```
Run → FAILS: `NameError: name 'StringProcessor' is not defined` ✓

**Step 2 — GREEN:**
```python
# string_processor.py
class StringProcessor:
    def word_count(self, text):
        if not text:
            return 0
        return len(text.split())
```
Run → PASSES ✓

**Step 3 — RED (next behavior):**
```python
def test_word_count_single_word():
    sp = StringProcessor()
    assert sp.word_count("hello") == 1

def test_word_count_multiple_words():
    sp = StringProcessor()
    assert sp.word_count("hello world foo") == 3
```
Run → `test_word_count_single_word` PASSES (existing impl handles it)
`test_word_count_multiple_words` PASSES ✓ (continues cycle)

**Step 4 — RED (edge case):**
```python
def test_word_count_extra_spaces():
    sp = StringProcessor()
    assert sp.word_count("  hello   world  ") == 2
```
Run → FAILS: `split()` with no args handles this! Actually PASSES.

**Step 5 — REFACTOR:**
```python
# test_string_processor.py — extract fixture
import pytest

@pytest.fixture
def sp():
    return StringProcessor()

def test_word_count_empty_string(sp):
    assert sp.word_count("") == 0

def test_word_count_single_word(sp):
    assert sp.word_count("hello") == 1

def test_word_count_multiple_words(sp):
    assert sp.word_count("hello world foo") == 3

def test_word_count_extra_spaces(sp):
    assert sp.word_count("  hello   world  ") == 2
```
Run → ALL PASS ✓

---

## When TDD is Applied

The model applies TDD by default whenever:
- Writing a new function, method, or class
- Fixing a bug (write a test that reproduces the bug first, then fix)
- Adding a new feature to existing code
- Refactoring code that lacks tests (write tests to characterize current behavior first)

TDD is not applied for:
- Exploratory scripts and throwaway prototypes (explicitly flagged as such)
- Configuration files
- Pure data definitions (JSON schemas, constants)
