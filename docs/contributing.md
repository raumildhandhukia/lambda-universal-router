---
layout: default
title: Contributing Guide
---

# Contributing Guide

Thank you for considering contributing to Lambda Universal Router! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/lambda-universal-router.git
   cd lambda-universal-router
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Run tests:
   ```bash
   python -m pytest
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your meaningful commit message"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Adding New Event Types

1. Create a new file in `lambda_universal_router/events/`:
   ```python
   from __future__ import annotations
   from typing import Any, Dict
   from dataclasses import dataclass
   from ..base import BaseEvent

   @dataclass
   class NewEventData:
       field1: str
       field2: int

   class NewEvent(BaseEvent):
       def _parse_event(self, event_dict: Dict[str, Any]) -> None:
           self.data = NewEventData(
               field1=event_dict.get('field1', ''),
               field2=event_dict.get('field2', 0)
           )
   ```

2. Create a handler in `lambda_universal_router/handlers.py`:
   ```python
   class NewEventHandler(EventHandler):
       def can_handle(self, event: Dict[str, Any]) -> bool:
           return 'specific_field' in event

       def parse_event(self, event: Dict[str, Any]) -> NewEvent:
           return NewEvent(event)
   ```

3. Add to Router class in `router.py`:
   ```python
   def new_event(self) -> Callable:
       def decorator(func: Callable) -> Callable:
           self._handlers.append(
               HandlerRegistration(
                   func=func,
                   handler=self._event_handlers['new_event']
               )
           )
           return func
       return decorator
   ```

4. Add tests in `tests/test_router.py`

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Keep functions focused and small
- Add tests for new features

## Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=lambda_universal_router

# Run specific test file
python -m pytest tests/test_router.py
```

## Documentation

- Update docstrings for any new code
- Add examples for new features
- Update README.md if needed
- Add changelog entries

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Update CHANGELOG.md
4. Ensure all tests pass
5. Request review from maintainers

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Publish to PyPI

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Documentation improvements