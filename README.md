# Mobile Mystery House API Documentation

Base URL: `/api`

---

## POST /api/log
Logs a user's interaction with a puzzle.

**Body Parameters** (JSON):
- `session_id` (string)
- `puzzle_id` (string)
- `start_time` (ISO datetime string)
- `end_time` (ISO datetime string)
- `device_type` (string, optional)

**Response:**
```json
{
  "status": "logged",
  "attempt_number": 1
}
```

---

## POST /api/feedback
Submits feedback for a session.

**Body Parameters** (JSON):
- `experience` (string)
- `learned` (integer)
- `favorite` (string)
- `moreGames` (string)
- `session_id` (string, optional)

**Response:**
```json
{
  "status": "submitted"
}
```

---

## GET /api/analytics
Returns overall game statistics.

**Response:**
```json
{
  "total_sessions": 56,
  "puzzles": [
    {
      "puzzle_id": "puzzle_1",
      "completions": 42,
      "avg_duration_seconds": 65,
      "max_attempts_by_any_session": 4
    }
  ]
}
```

---

## GET /api/analytics/time-by-attempt
Returns average time per attempt number for each puzzle.

**Response:**
```json
{
  "puzzle_1": [
    { "attempt_number": 1, "avg_duration_seconds": 72 },
    { "attempt_number": 2, "avg_duration_seconds": 60 }
  ]
}
```

---

## GET /api/analytics/dropoff
Shows how many sessions started and completed each puzzle.

**Response:**
```json
{
  "puzzle_1": { "started": 56, "completed": 50 },
  ...
}
```

---

## GET /api/analytics/completion-funnel
Returns progression data through the puzzle sequence.

**Response:**
```json
[
  { "puzzle_id": "puzzle_1", "started": 56, "completed": 50 },
  ...
]
```

---

## GET /api/analytics/first-try-success
Shows how many sessions solved each puzzle on their first attempt.

**Response:**
```json
[
  {
    "puzzle_id": "puzzle_1",
    "total_sessions": 48,
    "first_try_successes": 33,
    "success_rate_percent": 68.8
  }
]
```

---

## GET /api/analytics/improvement-score
Measures average improvement from first to last attempt per puzzle.

**Response:**
```json
[
  {
    "puzzle_id": "puzzle_1",
    "average_first_attempt_seconds": 72,
    "average_last_attempt_seconds": 58,
    "improvement_seconds": 14,
    "improvement_percent": 19.4
  }
]
```

---

## GET /api/analytics/device-comparison
Compares puzzle performance across device types.

**Response:**
```json
[
  {
    "device_type": "iOS",
    "puzzle_id": "puzzle_1",
    "average_duration_seconds": 64,
    "completion_count": 21
  }
]
```

---