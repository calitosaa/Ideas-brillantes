# Skill: Code Review

## Description and Purpose

This skill describes the native code review capability of Ideas-brillantes. The model performs structured code reviews across 9 dimensions, assigning severity levels to findings and providing actionable, constructive feedback. The goal of a code review is not to find fault but to ensure the code is correct, secure, maintainable, and aligned with project standards before it is merged.

---

## When This Skill Applies

- User asks to review a pull request, diff, or code snippet
- User asks "is this code good?" or "what's wrong with this?"
- User shares code before merging or deploying
- Automated review trigger on PR creation (subagent mode)
- User asks to check a specific dimension (e.g., "check this for security issues")

---

## Severity Levels

| Severity | Meaning | Action |
|---|---|---|
| **CRITICAL** | Must be fixed before merge. Causes data loss, security breach, or system failure | Blocks merge |
| **HIGH** | Should be fixed before merge. Significant correctness, security, or performance issue | Strong recommendation to fix |
| **MEDIUM** | Should be addressed soon. Code quality, minor correctness, missing tests | Fix in follow-up PR acceptable |
| **LOW** | Suggestion or style issue. No functional impact | Optional improvement |
| **INFO** | Observation or question. Not necessarily a problem | No action required |

---

## The 9 Review Dimensions

### 1. Architecture

**What to check:**
- Does the code follow the established patterns and structure of the project?
- Is responsibility correctly distributed (single responsibility principle)?
- Are there inappropriate dependencies between modules (e.g., UI code calling DB directly)?
- Is the abstraction level appropriate (not too thin, not over-engineered)?
- Does the change introduce cyclic dependencies?

**Common findings:**

```
[HIGH] Architecture: The UserService is directly instantiating EmailClient instead 
of receiving it via dependency injection. This makes the service impossible to 
unit test in isolation and tightly couples it to the email implementation.

Fix: Accept EmailClient (or an interface/abstract class) as a constructor parameter.
```

```
[MEDIUM] Architecture: This function is 180 lines and handles database query, 
business logic, and response formatting. Consider extracting into three focused 
functions: fetch_user_data(), apply_business_rules(), format_response().
```

---

### 2. Logic

**What to check:**
- Is the algorithm correct? Does it handle all stated requirements?
- Are all edge cases handled (empty input, null, zero, max values, boundary conditions)?
- Are boolean conditions correct (`&&` vs `||`, negation errors)?
- Is error flow correct (does error path actually propagate or swallow the error)?
- Are loops and recursion correct (termination condition, off-by-one)?
- Is state mutation correct (are the right objects being mutated, at the right time)?

**Common findings:**

```
[CRITICAL] Logic: The pagination offset calculation uses `page * limit` but 
should be `(page - 1) * limit` if pages are 1-indexed. With the current code, 
page 1 skips the first `limit` records.
```

```
[HIGH] Logic: The condition `if user and user.active == False` will pass when 
`user` is `None` because `None and ...` evaluates to `None` (falsy). The check 
should be `if user is not None and user.active == False` or 
`if user is not None and not user.active`.
```

```
[MEDIUM] Logic: The function returns early with `None` when the list is empty, 
but the caller at line 47 does `result.items()` without a null check, which 
will raise AttributeError.
```

---

### 3. Security

**What to check (OWASP Top 10 focus):**

| Vulnerability | Check |
|---|---|
| **Injection (SQL, Command, LDAP)** | Are user inputs sanitized before use in queries/commands? |
| **XSS** | Is user-supplied content escaped before rendering in HTML? |
| **Broken Authentication** | Are passwords hashed? Are session tokens properly invalidated? |
| **Sensitive Data Exposure** | Are secrets in env vars, not code? Is PII logged? |
| **Security Misconfiguration** | Debug mode in production? Default credentials? |
| **Insecure Deserialization** | Is untrusted data deserialized (pickle, eval, YAML load)? |
| **CSRF** | Are state-changing requests protected by CSRF tokens? |
| **Authorization** | Are permissions checked on every resource access? |
| **Path Traversal** | Are file paths constructed from user input validated? |
| **Hardcoded Secrets** | API keys, passwords in source code? |

**Critical security findings:**

```
[CRITICAL] Security (SQL Injection): The query at line 23 uses string 
interpolation with user input:
  query = f"SELECT * FROM users WHERE name = '{user_input}'"
This allows SQL injection. Use parameterized queries:
  cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

```
[CRITICAL] Security (Hardcoded Secret): Line 5 contains a hardcoded API key:
  API_KEY = "sk-1234567890abcdef"
This will be committed to version control. Move to environment variable:
  API_KEY = os.environ["API_KEY"]
Rotate the leaked key immediately.
```

```
[HIGH] Security (Path Traversal): The file path is constructed as:
  path = f"/var/uploads/{user_filename}"
A malicious user could supply `../../etc/passwd` as the filename.
Sanitize with: `os.path.basename(user_filename)` and validate the result.
```

```
[HIGH] Security (XSS): User-supplied content is rendered without escaping:
  <div>{user.bio}</div>
In React this is fine (JSX escapes by default), but if using dangerouslySetInnerHTML 
or server-side templating without autoescaping, this is XSS.
```

---

### 4. Supply Chain

**What to check:**
- Are dependencies pinned to specific versions?
- Are there known vulnerabilities in dependencies? (check CVE databases)
- Are dependencies from trusted sources?
- Is the minimal set of dependencies used (no bloated transitive deps)?
- Are lock files present and committed (`package-lock.json`, `Pipfile.lock`, `Cargo.lock`)?

**Common findings:**

```
[HIGH] Supply Chain: Dependencies are not pinned in requirements.txt:
  requests>=2.0.0
This can silently pull in a new major version with breaking changes or 
security vulnerabilities. Pin to exact versions:
  requests==2.31.0
```

```
[MEDIUM] Supply Chain: `lodash@4.17.20` has known prototype pollution 
vulnerabilities (CVE-2021-23337). Update to 4.17.21 or later.
```

---

### 5. Immutability

**What to check:**
- Are shared data structures mutated unexpectedly?
- Are function parameters mutated (callers may not expect this)?
- Are default mutable arguments used in Python (`def f(x=[])`)?
- Are React state objects mutated directly instead of via setState?
- Are configuration objects frozen/readonly when appropriate?

**Common findings:**

```
[HIGH] Immutability (Python mutable default): 
  def add_item(item, collection=[]):
      collection.append(item)
      return collection
The default list `[]` is created once and shared across all calls. 
Use `None` as default:
  def add_item(item, collection=None):
      if collection is None:
          collection = []
      collection.append(item)
      return collection
```

```
[MEDIUM] Immutability: The function mutates its `options` parameter:
  def process(options):
      options['timeout'] = 30  # mutates caller's dict
Use a copy: `options = {**options, 'timeout': 30}`
```

---

### 6. Error Handling

**What to check:**
- Are errors caught at the right level (not too early, not too late)?
- Are exceptions silently swallowed (`except: pass`)?
- Are error messages informative (include context, not just "error occurred")?
- Are resources properly cleaned up on error (files closed, connections released)?
- Are HTTP errors handled (non-2xx responses checked)?
- Are async rejections handled?

**Common findings:**

```
[HIGH] Error Handling: Bare except clause swallows all exceptions including 
KeyboardInterrupt and SystemExit:
  try:
      process_data()
  except:  # catches EVERYTHING
      pass
Specify the exception type and log it:
  try:
      process_data()
  except ProcessingError as e:
      logger.error("Data processing failed: %s", e)
      raise
```

```
[MEDIUM] Error Handling: The file is opened but not closed if an exception 
occurs during processing:
  f = open(path)
  data = f.read()
  process(data)    # if this raises, f is never closed
  f.close()
Use context manager: `with open(path) as f:`
```

```
[MEDIUM] Error Handling: HTTP response status is not checked:
  response = requests.get(url)
  data = response.json()  # will fail on 4xx/5xx with non-JSON body
Add: `response.raise_for_status()` before accessing body.
```

---

### 7. Performance

**What to check:**
- N+1 query patterns (query inside a loop)
- Unnecessary repeated computation (should be cached or memoized)
- Unnecessary allocations (large objects created in hot paths)
- Blocking operations on async code
- Missing database indexes for queried columns
- Large data loaded entirely into memory when streaming would work

**Common findings:**

```
[HIGH] Performance (N+1 Query): The loop executes one DB query per user:
  for user in users:
      orders = Order.objects.filter(user_id=user.id)  # N queries
This becomes O(N) database round-trips. Use a join or prefetch:
  # Django ORM:
  users = User.objects.prefetch_related('orders').all()
  # SQL:
  SELECT u.*, o.* FROM users u LEFT JOIN orders o ON o.user_id = u.id
```

```
[MEDIUM] Performance: `json.loads(config_file.read())` is called on every 
request handler invocation. The config file does not change at runtime — 
parse it once at startup and reuse the result.
```

```
[MEDIUM] Performance: `Array.find()` is called inside a loop over a large 
array, resulting in O(N²) complexity. Convert the array to a Map for O(1) 
lookup before the loop.
```

---

### 8. Code Quality

**What to check:**
- Naming: are names descriptive and consistent with project conventions?
- Duplication: is the same logic repeated (should be extracted)?
- Complexity: are functions too long or deeply nested?
- Dead code: are there commented-out code blocks, unused variables or imports?
- Magic numbers/strings: are literals given named constants?
- Comments: do comments explain WHY, not WHAT?
- Consistency: does style match the surrounding codebase?

**Common findings:**

```
[LOW] Code Quality: Variable name `d` on line 34 is not descriptive. 
Based on context, `deadline` or `due_date` would clarify intent.
```

```
[LOW] Code Quality: Magic number `86400` appears three times without 
explanation. Extract to a named constant: `SECONDS_PER_DAY = 86400`
```

```
[MEDIUM] Code Quality: This function is 145 lines with nesting depth of 5. 
Consider extracting the inner loop body to a separate function to improve 
readability and testability.
```

```
[INFO] Code Quality: Lines 78-92 are commented out. If this code is no longer 
needed, remove it (git history preserves it). If it may be needed again, 
add a comment explaining why it's disabled.
```

---

### 9. Test Coverage

**What to check:**
- Are the happy paths tested?
- Are edge cases tested (empty input, null, boundary values, error paths)?
- Do tests actually assert the right things (not just "no exception raised")?
- Are tests isolated (no dependency on test execution order)?
- Are there tests for the specific change introduced by this PR?
- Is the test-to-code ratio reasonable?

**Common findings:**

```
[HIGH] Test Coverage: The new `calculate_tax()` function has no tests. 
This is a business-critical calculation — it needs tests for:
- Zero tax rate
- Maximum tax rate
- Input at boundary values
- Negative income (should it raise or return 0?)
```

```
[MEDIUM] Test Coverage: The test only checks the happy path. The function 
has three early-return error conditions that are not tested. Add tests for:
- Empty input list
- Input with invalid data types
- Network timeout scenario (mock the HTTP call)
```

```
[LOW] Test Coverage: `test_process_data` asserts only that no exception is 
raised (`with pytest.raises` is not used). Add an assertion on the return 
value to verify correct output, not just absence of error.
```

---

## Constructive Feedback Guidelines

**Always:**
- State the dimension and severity first: `[HIGH] Security:`
- Explain WHY it's a problem (not just "this is wrong")
- Show the problematic code inline
- Provide a concrete fix or direction
- Distinguish between blocking issues and suggestions

**Never:**
- Use dismissive language ("this is terrible", "obviously wrong")
- Give vague feedback without actionable direction
- Block a PR for style issues when automated formatters should handle them
- Comment on every minor issue — focus on what matters most

**Tone template:**
```
[SEVERITY] Dimension: Brief one-line summary.

The [specific code] at line N [does X], which [causes problem Y]. 
This can lead to [consequence].

Suggested fix:
  [code example]

[Optional: note if related patterns exist elsewhere]
```

---

## Language-Specific Review Notes

### Python
- Check for mutable default arguments
- Verify `__eq__` is paired with `__hash__`
- Look for bare `except:` and `except Exception:` used as control flow
- Check `is` vs `==` for comparisons (use `is` only for identity, not equality)
- Verify f-strings vs `.format()` vs `%` consistency

### JavaScript / TypeScript
- Check for `==` vs `===` (always use `===`)
- Look for unhandled Promise rejections (missing `.catch()` or `try/catch` in async)
- Check for direct DOM manipulation mixing with framework patterns
- Verify TypeScript types are specific (avoid `any`)
- Check `useEffect` dependencies array in React

### Go
- All errors must be handled (no `_` for error return unless intentional and commented)
- Goroutine leaks: verify goroutines have a way to exit
- Race conditions: any shared state must be protected
- Interface compliance: verify interfaces are implemented correctly
- `defer` in loops can be unexpected

### SQL
- Parameterized queries always (never string concatenation with user data)
- Indexes exist for columns in WHERE, JOIN ON, and ORDER BY
- LIMIT on queries that could return large result sets
- Transactions wrap multi-statement operations that must be atomic
