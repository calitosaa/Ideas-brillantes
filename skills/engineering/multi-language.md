# Multi-Language Programming Skill

## Fuente
VoltAgent/awesome-agent-skills (coding), everything-claude-code, ruflo coder agent, agency-agents (engineering)

---

## 12 Lenguajes Soportados

### Python 3.12+
```python
# Type hints, dataclasses, pattern matching
from dataclasses import dataclass, field
from typing import Any

@dataclass
class User:
    id: int
    name: str
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "tags": self.tags}

# Pattern matching (3.10+)
match status_code:
    case 200: return "OK"
    case 404: return "Not Found"
    case 500 | 503: return "Server Error"
    case _: return f"Unknown: {status_code}"

# Walrus operator
while chunk := file.read(8192):
    process(chunk)

# f-strings con format spec
price = 1234.5
print(f"Price: {price:,.2f}")  # Price: 1,234.50
```

### TypeScript / JavaScript
```typescript
// Generics, utility types, discriminated unions
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUser(id: number): Promise<Result<User>> {
  try {
    const user = await db.users.findById(id);
    if (!user) return { ok: false, error: new Error('Not found') };
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e as Error };
  }
}

// Zod schema validation
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number().positive(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'moderator']),
  createdAt: z.date().default(() => new Date()),
});

type User = z.infer<typeof UserSchema>;
```

### Go
```go
// Error handling, goroutines, channels
package main

import (
    "context"
    "errors"
    "fmt"
    "sync"
)

type UserService struct {
    db Database
    cache Cache
}

// Sentinel errors
var (
    ErrNotFound    = errors.New("user not found")
    ErrUnauthorized = errors.New("unauthorized")
)

func (s *UserService) GetUser(ctx context.Context, id int) (*User, error) {
    // Try cache first
    if user, err := s.cache.Get(ctx, id); err == nil {
        return user, nil
    }

    user, err := s.db.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("getUserByID(%d): %w", id, err)
    }

    s.cache.Set(ctx, id, user)
    return user, nil
}

// Concurrent fan-out
func fetchAll(ctx context.Context, ids []int) ([]*User, error) {
    results := make([]*User, len(ids))
    errs := make([]error, len(ids))
    var wg sync.WaitGroup

    for i, id := range ids {
        wg.Add(1)
        go func(idx, userID int) {
            defer wg.Done()
            results[idx], errs[idx] = fetchUser(ctx, userID)
        }(i, id)
    }

    wg.Wait()
    return results, errors.Join(errs...)
}
```

### Rust
```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    pub id: u64,
    pub name: String,
    pub email: String,
}

#[derive(Debug, Error)]
pub enum UserError {
    #[error("User {id} not found")]
    NotFound { id: u64 },
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("Validation failed: {field} {message}")]
    Validation { field: String, message: String },
}

pub struct UserRepository {
    pool: sqlx::PgPool,
    cache: HashMap<u64, User>,
}

impl UserRepository {
    pub async fn find(&self, id: u64) -> Result<User, UserError> {
        if let Some(user) = self.cache.get(&id) {
            return Ok(user.clone());
        }

        sqlx::query_as!(User, "SELECT id, name, email FROM users WHERE id = $1", id as i64)
            .fetch_optional(&self.pool)
            .await?
            .ok_or(UserError::NotFound { id })
    }
}
```

### Java / Kotlin
```kotlin
// Kotlin — null safety, data classes, coroutines
data class User(
    val id: Long,
    val name: String,
    val email: String,
    val roles: Set<Role> = emptySet()
)

sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Failure(val exception: Throwable) : Result<Nothing>()

    inline fun <R> map(transform: (T) -> R): Result<R> = when (this) {
        is Success -> Success(transform(value))
        is Failure -> this
    }
}

// Coroutines
class UserService(private val repo: UserRepository) {
    suspend fun findUser(id: Long): Result<User> = runCatching {
        repo.findById(id) ?: throw NoSuchElementException("User $id not found")
    }.fold(
        onSuccess = { Result.Success(it) },
        onFailure = { Result.Failure(it) }
    )
}
```

### C# / .NET
```csharp
// Records, nullable reference types, LINQ
public record User(int Id, string Name, string Email, UserRole Role = UserRole.User);

public enum UserRole { User, Moderator, Admin }

public class UserService(IUserRepository repo, ILogger<UserService> logger)
{
    public async Task<User?> GetUserAsync(int id, CancellationToken ct = default)
    {
        var user = await repo.FindByIdAsync(id, ct);
        if (user is null)
        {
            logger.LogWarning("User {Id} not found", id);
            return null;
        }
        return user;
    }

    public async Task<IReadOnlyList<User>> GetAdminsAsync(CancellationToken ct = default)
    {
        var users = await repo.GetAllAsync(ct);
        return users
            .Where(u => u.Role == UserRole.Admin)
            .OrderBy(u => u.Name)
            .ToList()
            .AsReadOnly();
    }
}
```

### PHP 8.2+
```php
<?php
// Enums, readonly, first-class callable syntax
enum UserRole: string {
    case Admin = 'admin';
    case User = 'user';
    case Moderator = 'moderator';
}

readonly class User {
    public function __construct(
        public readonly int $id,
        public readonly string $name,
        public readonly string $email,
        public readonly UserRole $role = UserRole::User,
    ) {}

    public function isAdmin(): bool {
        return $this->role === UserRole::Admin;
    }

    public function toArray(): array {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'role' => $this->role->value,
        ];
    }
}

// Named arguments + null safe operator
function createUser(
    string $name,
    string $email,
    UserRole $role = UserRole::User,
    ?int $id = null,
): User {
    return new User(id: $id ?? nextId(), name: $name, email: $email, role: $role);
}
```

### Swift
```swift
// Swift 5.9 — async/await, actor, macros
actor UserCache {
    private var cache: [Int: User] = [:]

    func get(_ id: Int) -> User? { cache[id] }
    func set(_ id: Int, user: User) { cache[id] = user }
}

struct User: Codable, Identifiable {
    let id: Int
    var name: String
    var email: String
    var roles: Set<Role>

    enum Role: String, Codable { case admin, user, moderator }
}

class UserService {
    private let cache = UserCache()
    private let api: APIClient

    func fetchUser(id: Int) async throws -> User {
        if let cached = await cache.get(id) { return cached }

        let user = try await api.get("/users/\(id)", as: User.self)
        await cache.set(id, user: user)
        return user
    }
}
```

### Ruby
```ruby
# Ruby 3.2 — pattern matching, data class
User = Data.define(:id, :name, :email, :role) do
  def admin? = role == :admin
  def to_h = {id:, name:, email:, role:}
end

class UserService
  def initialize(repo)
    @repo = repo
  end

  def find(id)
    case @repo.find(id)
    in { id:, name:, email: } => user then User.new(**user, role: :user)
    in nil then raise NotFoundError, "User #{id} not found"
    end
  rescue => e
    Result.failure(e)
  end
end

# Pattern matching with deconstruct
case response
in { status: 200, body: { user: User => user } } then user
in { status: 404 } then nil
in { status: 500, body: { error: message } } then raise ServerError, message
end
```

### Shell (Bash)
```bash
#!/bin/bash
# Bash best practices
set -euo pipefail
IFS=$'\n\t'

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/tmp/$(basename "$0").log"

# Logging
log()   { echo "[$(date +'%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
error() { log "ERROR: $*" >&2; exit 1; }

# Argument parsing
usage() { echo "Usage: $0 [-v] [-o output_dir] input_file"; exit 1; }

VERBOSE=false
OUTPUT_DIR="."

while getopts "vo:h" opt; do
    case "$opt" in
        v) VERBOSE=true ;;
        o) OUTPUT_DIR="$OPTARG" ;;
        h|*) usage ;;
    esac
done
shift $((OPTIND-1))

[[ $# -ge 1 ]] || usage
INPUT_FILE="$1"
[[ -f "$INPUT_FILE" ]] || error "File not found: $INPUT_FILE"

# Main logic
process() {
    local file="$1"
    local output_dir="$2"

    log "Processing: $file"
    # ... processing logic ...
    log "Done: $output_dir/$(basename "$file")"
}

process "$INPUT_FILE" "$OUTPUT_DIR"
```

### SQL (PostgreSQL avanzado)
```sql
-- CTEs, window functions, JSON
WITH monthly_stats AS (
    SELECT
        date_trunc('month', created_at) AS month,
        COUNT(*) AS total_orders,
        SUM(amount) AS revenue,
        AVG(amount) AS avg_order
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
),
growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
        ROUND(
            100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) /
            NULLIF(LAG(revenue) OVER (ORDER BY month), 0),
            1
        ) AS growth_pct
    FROM monthly_stats
)
SELECT
    to_char(month, 'YYYY-MM') AS period,
    total_orders,
    revenue,
    COALESCE(growth_pct::text, 'N/A') AS growth
FROM growth g
JOIN monthly_stats m USING (month)
ORDER BY month DESC;

-- JSONB operations
SELECT
    id,
    metadata->>'name' AS name,
    (metadata->'address'->>'city') AS city,
    jsonb_array_length(metadata->'tags') AS tag_count
FROM products
WHERE metadata @> '{"active": true}'
  AND metadata ? 'price'
ORDER BY (metadata->>'price')::numeric DESC;
```

---

## Patrones Multi-Lenguaje

### Async/Await (Python, JS/TS, C#, Swift, Kotlin)
```python
# Python
async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
```

### Builder Pattern
```python
# Python
class QueryBuilder:
    def __init__(self): self._query = {}
    def where(self, **kwargs): self._query.update(kwargs); return self
    def limit(self, n): self._query['limit'] = n; return self
    def build(self): return self._query

query = QueryBuilder().where(active=True).limit(10).build()
```

### Repository Pattern (independiente del lenguaje)
```
Interface:
  find_by_id(id) → Entity | None
  find_all(filters) → [Entity]
  save(entity) → Entity
  delete(id) → bool

Implementaciones:
  PostgresRepository
  MongoRepository
  InMemoryRepository (para tests)
```
