apis/
├── main.py                 # Application entry point
├── core/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   └── database.py        # Database connections
├── models/
│   ├── __init__.py
│   ├── requests.py        # Pydantic request models
│   ├── responses.py       # Pydantic response models
│   └── database.py        # Database models
├── services/
│   ├── __init__.py
│   ├── translation.py     # Agent orchestration service
│   ├── websocket.py       # Real-time updates
│   └── file_processing.py # Document handling
├── routes/
│   ├── __init__.py
│   ├── translation.py     # Translation endpoints
│   ├── documents.py       # File upload endpoints
│   ├── analytics.py       # Metrics endpoints
│   └── websocket.py       # WebSocket endpoints
└── utils/
    ├── __init__.py
    ├── dependencies.py    # Dependency injection
    └── exceptions.py      # Custom exceptions

Why This Structure?

Separation of Concerns: Models, services, and routes are separate
Scalability: Easy to add new agents or features
Testing: Each component can be tested independently
Configuration: Environment-based settings for different deployments

