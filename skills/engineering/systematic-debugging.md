# Skill: Systematic Debugging

## Description and Purpose

This skill describes the native debugging methodology embedded in Ideas-brillantes. Debugging is not trial-and-error patching — it is a structured investigation that always starts with understanding the root cause before writing a single line of fix code. The model has been fine-tuned to resist the urge to apply quick fixes, to follow a four-phase diagnostic process, and to recognize when a problem is symptomatic of a deeper architectural issue.

---

## ROOT CAUSE FIRST

> **Never apply a fix before identifying the root cause.**

Applying fixes without understanding the cause leads to:
- Symptoms disappearing while the bug moves elsewhere
- New bugs introduced by the patch
- Increasing technical debt from accumulated band-aids
- Wasted time when the "fixed" code breaks again

The model always investigates before suggesting solutions.

---

## The Critical Red Flag

> **3 or more failed fixes on the same bug = architecture problem**

When three different attempted fixes all fail to resolve the same issue, stop debugging at the symptom level. The problem is almost certainly structural:
- Wrong abstraction chosen
- Incorrect data flow design
- Fundamental misunderstanding of a library/API
- State management architecture flaw

**At this point:** step back, re-read the relevant code from scratch, draw the data flow, and identify the wrong assumption at the design level.

---

## Four-Phase Debugging Methodology

```
Phase 1: Root Cause Investigation
           ↓
Phase 2: Pattern Analysis
           ↓
Phase 3: Hypothesis Testing
           ↓
Phase 4: Implementation
```

---

### Phase 1: Root Cause Investigation

**Goal:** Gather enough information to understand what the system is actually doing vs. what it should be doing.

**Steps:**

1. **Read the full error message.** Do not skim. Every word matters. Stack traces contain the exact location of the failure.

2. **Identify the failure point:** What line, function, module is failing?

3. **Trace the data path backward:** What data reached the failure point? Trace it back through function calls to its origin.

4. **Examine the state:** What is the value of all relevant variables at the point of failure?

5. **Read the documentation:** If a library/API is involved, read its docs for the failing method. Many bugs are documentation misreads.

**Tools to use:**

```python
# Python: Add strategic print statements
print(f"DEBUG type={type(value)}, value={repr(value)}")

# Python: Use pdb
import pdb; pdb.set_trace()
# Then: n (next), s (step), c (continue), p variable, bt (backtrace)

# Python: Rich traceback
from rich.traceback import install; install(show_locals=True)
```

```javascript
// JavaScript: console.trace for call stack
console.trace('Debug point reached');
console.log(JSON.stringify(obj, null, 2));

// Node.js: Use debugger
debugger;  // with: node --inspect script.js
```

```bash
# Shell: verbose execution
bash -x script.sh
set -x  # in script
```

```go
// Go: fmt.Printf debugging
fmt.Printf("DEBUG: type=%T value=%+v\n", val, val)

// Go: delve debugger
dlv debug main.go
```

```rust
// Rust: dbg! macro
dbg!(&value);

// Rust: RUST_BACKTRACE
RUST_BACKTRACE=1 cargo run
```

**Key questions to answer in Phase 1:**
- What is the exact error message and type?
- What is the exact line of failure?
- What values were in scope at failure?
- Is this deterministic or intermittent?
- When did this start happening? (git bisect if needed)

---

### Phase 2: Pattern Analysis

**Goal:** Determine whether this is an isolated bug or part of a larger pattern.

**Steps:**

1. **Classify the bug type:**
   - Logic error (wrong algorithm or condition)
   - Data error (unexpected input shape, type, or value)
   - Integration error (wrong API usage, mismatched contract)
   - Concurrency error (race condition, deadlock)
   - Configuration error (wrong env var, path, or setting)
   - Dependency error (version conflict, missing library)

2. **Check for related failures:** Are other tests failing? Is this bug similar to a previous one?

3. **Identify the scope:** Is this failure isolated to one function, or does it indicate a broken contract between components?

4. **Search for similar patterns in the codebase:**
   ```bash
   grep -rn "same_function_name\|similar_pattern" src/
   ```

5. **Check git history:**
   ```bash
   git log --oneline -20                    # recent changes
   git log -p --follow src/failing_file.py  # changes to specific file
   git bisect start HEAD <last_good_commit>  # binary search for regression
   ```

**Common patterns by bug type:**

| Pattern | Symptoms | Likely Cause |
|---|---|---|
| `NullPointerException` / `AttributeError: 'NoneType'` | Crash on attribute access | Missing null check, unexpected None return |
| `KeyError` / `undefined` | Missing dict/object key | Wrong key name, different data shape than expected |
| Off-by-one | Wrong count, first/last element missing | Loop bounds, 0 vs 1 indexing |
| Stale closure | JS async function uses wrong outer value | Missing dependency in useEffect, capture by reference |
| Race condition | Intermittent failure under load | Shared mutable state, missing lock |
| Type coercion | Wrong arithmetic, unexpected `"21"` instead of `21` | String/int mixing, JSON parsing |

---

### Phase 3: Hypothesis Testing

**Goal:** Form specific, falsifiable hypotheses and test them systematically. One hypothesis at a time.

**Steps:**

1. **Form hypothesis:** "I believe the bug is caused by X because of evidence Y."

2. **Design a minimal test:** The smallest possible input or code change that would confirm or deny the hypothesis.

3. **Test the hypothesis:** Run the minimal test. Do not change multiple things at once.

4. **Record the result:** Did the evidence confirm or deny the hypothesis? Update understanding accordingly.

5. **If confirmed:** Move to Phase 4.
   **If denied:** Form a new hypothesis based on new information.

**Example hypothesis process:**
```
Hypothesis 1: "The user_id is None because the database query returns None for new users"
Test: Add print(user_id) immediately after DB query
Result: user_id is "42" (a string, not int 42)
→ Hypothesis disproven. New finding: type mismatch.

Hypothesis 2: "The comparison user_id == 42 fails because user_id is string '42'"
Test: print(type(user_id), user_id == 42, user_id == "42")
Result: <class 'str'> False True
→ Hypothesis CONFIRMED.

Root cause: ORM returns string IDs, but code compares with integer literal.
```

**Writing a minimal reproduction:**
```python
# Minimal repro isolates the bug from all unrelated code
# This is faster than debugging in the full application

def test_hypothesis():
    # Set up ONLY what's needed to reproduce the bug
    user_id = "42"          # simulate what DB returns
    expected_id = 42
    
    # Show the exact failure
    print(user_id == expected_id)  # False — confirmed!
    
    # Show the fix
    print(int(user_id) == expected_id)  # True
```

---

### Phase 4: Implementation

**Goal:** Apply a correct fix, verify it solves the root cause, and ensure no regression.

**Steps:**

1. **Write a failing test first** (TDD discipline applies to bug fixes):
   ```python
   def test_user_id_comparison_with_string_id():
       # This test reproduces the exact bug
       user = User(id="42")
       assert user.matches_id(42) == True  # was returning False
   ```

2. **Apply the minimal correct fix:**
   - Fix the root cause, not the symptom
   - Do not add extra logic "just in case"
   - If multiple approaches exist, choose the one that prevents the class of bug

3. **Run the specific test:** Confirm it now passes.

4. **Run the full test suite:** Confirm no regressions.

5. **Review related code:** Is the same bug pattern present elsewhere?
   ```bash
   grep -rn "== user_id\|!= user_id" src/  # find similar comparisons
   ```

6. **Update or add tests** for edge cases revealed by the bug.

7. **Document the fix** with a clear commit message:
   ```
   fix: normalize user_id to int before comparison
   
   DB returns user IDs as strings, but comparison code expected int.
   Added int() cast at the boundary (service layer) to fix type mismatch.
   ```

---

## When to Escalate vs Continue

### Continue debugging when:
- Less than 3 fix attempts have been made
- The root cause is not yet identified
- More information can be gathered cheaply (add a print statement, read a file)
- The bug is isolated to a specific function or module

### Escalate (step back to architecture) when:
- 3 or more fixes have failed
- The same bug reappears after being "fixed"
- The fix requires changes to 5+ unrelated places
- The bug only reproduces in specific environments and not others
- The error is in a third-party dependency (may need to update, patch, or replace it)

### When to ask the user for more information:
- Cannot reproduce the bug locally
- Need environment details (OS, runtime version, config)
- Need to see the actual data that causes the failure
- The bug is intermittent and requires production logs

---

## Debugging Tools Reference by Language

### Python
| Tool | Use Case |
|---|---|
| `pdb` / `ipdb` | Interactive breakpoint debugger |
| `pytest --pdb` | Drop into debugger on test failure |
| `rich.traceback` | Beautiful tracebacks with local variables |
| `py-spy` | CPU profiler for performance bugs |
| `memory_profiler` | Memory leak detection |
| `logging` module | Structured debug output |

### JavaScript / Node.js
| Tool | Use Case |
|---|---|
| `node --inspect` | Chrome DevTools debugger |
| `console.trace()` | Print call stack |
| `debugger;` statement | Breakpoint in source |
| `Jest --verbose` | Detailed test output |
| `clinic.js` | Node.js performance profiling |

### Go
| Tool | Use Case |
|---|---|
| `dlv` (Delve) | Full debugger with breakpoints |
| `go test -v -run TestName` | Run specific test verbosely |
| `pprof` | CPU and memory profiling |
| `race detector` | `go run -race` for race conditions |

### Linux / Shell
| Tool | Use Case |
|---|---|
| `strace -p PID` | System call tracing |
| `ltrace` | Library call tracing |
| `gdb` | C/C++ debugger |
| `journalctl -f` | Live service logs |
| `tcpdump` / `wireshark` | Network debugging |
| `perf` | Performance analysis |

---

## Debugging Communication Pattern

When presenting debugging findings to the user:

1. **State what was found:** "The error occurs in `auth.py` line 47 because `user_id` is a string but the comparison expects an integer."
2. **Explain the root cause:** "The database ORM returns ID fields as strings, but the comparison code was written assuming integers."
3. **Show the fix:** Concrete code change.
4. **Show the test:** The test that confirms the fix works.
5. **Note related risks:** "I also found two other places with similar comparisons — here are the line numbers."
