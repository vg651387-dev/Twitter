# Public API Index

No public APIs were discovered in the repository yet. This index will populate as code is added or when `scripts/generate-docs.sh` can detect a supported project type.

## How to add a new API doc
Create a new file under this folder (or a subfolder) per API surface.

Recommended sections per API:
- **Summary**: What the API does and when to use it
- **Signature**: Function/method/class signature or HTTP endpoint
- **Parameters**: Name, type, required?, default, description
- **Returns**: Type and meaning
- **Errors**: Possible exceptions/status codes and causes
- **Examples**: 1-2 minimal usage snippets
- **Notes**: Edge cases, perf, security considerations

### Example (library function)
```ts
// Example only — replace with your real function
/**
 * getUserTimeline fetches the timeline for a given user.
 * @param userId string - unique user identifier
 * @param limit number = 20 - max items to fetch
 * @returns Tweet[]
 */
async function getUserTimeline(userId: string, limit: number = 20): Promise<Tweet[]> {}

// Usage
const tweets = await getUserTimeline("123", 10)
```

### Example (HTTP endpoint)
```http
GET /api/timeline?userId=123&limit=20

200 OK
Content-Type: application/json
[
  { "id": "t1", "text": "hello" }
]
```

### Example (Python function)
```python
def get_user_timeline(user_id: str, limit: int = 20) -> list[dict]:
    """Example only — replace with your real function.
    Args:
        user_id: unique user identifier
        limit: max items to fetch (default 20)
    Returns:
        List of tweet dicts
    """
    ...

# Usage
tweets = get_user_timeline("123", 10)
```