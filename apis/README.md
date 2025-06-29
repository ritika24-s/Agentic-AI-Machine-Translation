## Technical Stack Decisions
Architecture Required -
```
Intelligence Router → Core Translator → Quality Specialist
        ↓                    ↓                  ↓
   (async AI call)    (async service call)  (async optimization)
```

### FastAPI vs Flask for the Use Case

When to prefer Flask 
- Simpler projects - Flask has less "magic"
Team familiarity - if team knows Flask well
Legacy integrations - more mature ecosystem


#### Why FastAPI Wins for this System:

1. Async/Await Native Support
- The multi-agent system needs agents communicating asynchronously
- Translation services (LibreTranslate, Google, Anthropic) are all async calls
- Flask requires extra work (Flask-SocketIO, threading) for real async

2. Built-in Request Validation
- The translation requests have complex validation needs (language codes, text length, batch limits)
- FastAPI uses Pydantic models - perfect for TranslationState dataclasses
- Automatic error responses for invalid input

3. Auto-Generated API Documentation
- FastAPI creates interactive docs at /docs automatically
- Critical for enterprise adoption (scaling goal)
- Shows request/response examples, validates requests in browser

4. Better Performance
- Higher throughput for concurrent translation requests
- Important when processing batches or multiple agents working simultaneously

5. Modern Python Patterns
- Type hints everywhere (better for complex agent system)
- Dependency injection (great for service manager, Redis, etc.)
- Better IDE support and error catching

### Pydantic vs Dataclass 
Use Pydantic for:
- API request/response models (automatic validation, docs generation)
- Configuration models
- External service integration models

Use dataclasses for:
- Internal state management (like TranslationState between agents)
- Simple data containers that don't need validation

how to run the api:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

how to test the api:
```bash
curl -X POST http://localhost:8000/translate -H "Content-Type: application/json" -d '{"text": "Hello, world!"}'
```
