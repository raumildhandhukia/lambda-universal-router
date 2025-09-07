# Lambda Universal Router

A flexible and extensible AWS Lambda event router that supports multiple event sources. This library makes it easy to handle different types of AWS Lambda events in a clean and organized way.

## Features

- Support for multiple AWS event sources:
  - API Gateway
  - SQS
  - S3
- Easy to extend with new event sources
- Type-safe event handling with Python type hints
- Clean decorator-based routing
- Structured event objects with proper typing

## Installation

```bash
pip install lambda-universal-router
```

## Usage

Here's a simple example of how to use the router:

```python
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent, S3Event

router = Router()

@router.apigateway("/hello", method="GET")
def api_hello(event: APIGatewayEvent, context):
    return {
        "statusCode": 200,
        "body": "Hello from API Gateway"
    }

@router.sqs()
def process_queue(event: SQSEvent, context):
    for msg in event.records:
        print("SQS Message:", msg.body)

@router.s3()
def process_file(event: S3Event, context):
    for record in event.records:
        print("New S3 object:", record.s3.bucket.name, record.s3.object.key)

def lambda_handler(event, context):
    return router.dispatch(event, context)
```

## Event Types

### API Gateway Event

The `APIGatewayEvent` provides access to:
- HTTP method
- Path
- Headers
- Query string parameters
- Path parameters
- Request body
- Request context

### SQS Event

The `SQSEvent` provides access to:
- List of SQS messages
- Message attributes
- Message body
- Message ID

### S3 Event

The `S3Event` provides access to:
- List of S3 records
- Bucket information (name, ARN)
- Object information (key, size, etag)
- Event name and time

## Extending with New Event Sources

To add support for a new event source:

1. Create a new event class that inherits from `BaseEvent`
2. Create a new handler class that inherits from `EventHandler`
3. Add the handler to the Router's `_event_handlers` dictionary
4. Add a decorator method to the Router class

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
