# Smart or Sit 🏈

A fantasy football decision tool that aggregates start/sit recommendations from 5 trusted analysts into one consensus verdict.

## Features

- **Consensus Verdicts** - See START/SIT/FLEX recommendations aggregated from 5 analysts
- **Analyst Breakdown** - View each analyst's pick, projected points, and reasoning
- **Accuracy Tracking** - Historical accuracy scores for each analyst
- **Multiple Scoring Formats** - PPR, Half-PPR, and Standard support
- **Live Updates** - Real-time score updates via SSE during games

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI |
| Database | SQLite3 |
| Frontend | React, Tailwind CSS |
| Live Updates | Server-Sent Events (SSE) |

## Analysts Tracked

1. Matthew Berry (NBC Sports)
2. Mike Clay (ESPN)
3. Jamey Eisenberg (CBS Sports)
4. Andy Holloway (Fantasy Footballers)
5. Alex Korff (Draft Sharks)

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/players/search?q=` | Search players |
| GET | `/api/consensus/{player_id}` | Get consensus verdict |
| GET | `/api/analysts` | List all analysts |
| GET | `/api/games/live` | Get live games |

Full API docs available at `http://localhost:8000/docs` when running.

## Project Structure

```
smart-or-sit/
├── backend/
│   ├── app/
│   │   ├── routers/     # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── main.py      # FastAPI app
│   └── requirements.txt
├── frontend/
│   └── src/
├── data/                # SQLite database
└── docs/                # Documentation
```

## License

MIT
