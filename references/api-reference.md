# StepFun Search API Reference

## Endpoint

```
POST https://api.stepfun.com/v1/search
```

## Authentication

```
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json; charset=utf-8
```

## Request Schema

```json
{
  "query": "string (required) - Search keywords",
  "n": "integer (optional) - Number of results (1-10, default: 5)",
  "category": "string (optional) - Search category (all|research|news|technical, default: all)"
}
```

### Request Example

```bash
curl -X POST "https://api.stepfun.com/v1/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "query": "Python asyncio tutorial",
    "n": 5,
    "category": "technical"
  }'
```

## Response Schema

```json
{
  "status": 200,
  "message": "Success",
  "results": [
    {
      "title": "string - Result title",
      "url": "string - Source URL",
      "snippet": "string - Preview text (100-200 chars)",
      "source": "string - Domain/source name",
      "date": "string (optional) - Publication date (ISO 8601)",
      "rank": "integer - Result ranking (1-10)"
    }
  ],
  "query": "string - Original query",
  "query_time_ms": "integer - Processing time in milliseconds"
}
```

### Response Example

```json
{
  "status": 200,
  "message": "Success",
  "results": [
    {
      "title": "asyncio — Asynchronous I/O - Python Documentation",
      "url": "https://docs.python.org/3/library/asyncio.html",
      "snippet": "asyncio is a library to write concurrent code using the async/await syntax. It is used as a foundation for multiple Python asynchronous frameworks...",
      "source": "python.org",
      "date": "2024-03-01",
      "rank": 1
    },
    {
      "title": "Python asyncio Tutorial - Real Python",
      "url": "https://realpython.com/async-io-python/",
      "snippet": "A comprehensive guide to Python's asyncio library for asynchronous programming. Learn how to use async/await, coroutines, and event loops...",
      "source": "realpython.com",
      "date": "2024-02-15",
      "rank": 2
    }
  ],
  "query": "Python asyncio tutorial",
  "query_time_ms": 1250
}
```

## Error Responses

### 400 - Bad Request

```json
{
  "status": 400,
  "message": "Invalid query parameter",
  "error": {
    "code": "INVALID_QUERY",
    "detail": "Query must be between 1 and 500 characters"
  }
}
```

### 401 - Unauthorized

```json
{
  "status": 401,
  "message": "Authentication failed",
  "error": {
    "code": "INVALID_API_KEY",
    "detail": "API key is invalid or expired"
  }
}
```

### 429 - Rate Limited

```json
{
  "status": 429,
  "message": "Rate limit exceeded",
  "error": {
    "code": "RATE_LIMITED",
    "detail": "Daily quota exceeded. Limit resets at 2024-03-10T00:00:00Z"
  }
}
```

### 500 - Internal Server Error

```json
{
  "status": 500,
  "message": "Internal server error",
  "error": {
    "code": "INTERNAL_ERROR",
    "detail": "Service temporarily unavailable"
  }
}
```

## Categories

| Category | Use Case | Best For |
|----------|----------|----------|
| `research` | Academic & technical | Papers, reports, whitepapers, documentation |
| `programming` | Code & implementation | Tutorials, code examples, documentation, APIs |
| `business` | Business & market | Business news, company info, market analysis |
| `gov` | Government & policy | Government docs, policies, official information |

## Rate Limiting

- **Quota**: Up to 100 requests/day (free tier)
- **Throttle**: No more than 10 requests/minute
- **Timeout**: 30 seconds per request
- **Cache**: Results cached for 15 minutes

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process results |
| 400 | Bad request | Check query format |
| 401 | Unauthorized | Verify API key |
| 429 | Rate limited | Wait before retrying |
| 500 | Server error | Retry after delay |
| 503 | Service unavailable | Service maintenance |

## Query Tips

### Best Practices

1. **Be specific**: "Python asyncio coroutines" vs "Python"
2. **Use keywords**: "transformer attention mechanism" vs "How do transformers work?"
3. **Combine terms**: "PyTorch CNN image classification"
4. **Choose category**: Use `research` for papers, `news` for current events
5. **Limit results**: Request only what you need (n=3-5 usually sufficient)

### Performance

- Single keyword: ~500ms
- Multi-keyword phrase: ~1-2 seconds
- Cached results: <100ms
- Peak times: May see 2-5 second latency

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| INVALID_QUERY | Query too short/long | Use 1-500 character queries |
| INVALID_API_KEY | Wrong/expired API key | Check config in `openclaw.json` |
| RATE_LIMITED | Daily quota exceeded | Wait for quota reset or upgrade plan |
| TIMEOUT | Search taking too long | Simplify query, use more specific terms |
| NO_RESULTS | No matching content | Try different keywords or change category |

## Integration Notes

- **Environment variable**: `STEPFUN_API_KEY` must be set
- **Config file**: `~/.openclaw/openclaw.json` (skills section)
- **Timeout**: 30 seconds per request (enforced)
- **Retries**: Automatic 3x retry on network errors
- **Caching**: 15-minute TTL for identical queries
