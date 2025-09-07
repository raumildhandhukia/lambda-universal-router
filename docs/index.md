# Lambda Universal Router

A flexible and type-safe router for AWS Lambda functions that supports multiple event sources.

## Quick Start

```bash
pip install lambda-universal-router
```

## Basic Usage

```python
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent

router = Router()

@router.apigateway("/hello", method="GET")
def hello(event: APIGatewayEvent, context):
    name = event.query_string_parameters.get('name', 'World')
    return {
        "statusCode": 200,
        "body": f"Hello, {name}!"
    }

@router.sqs()
def process_queue(event: SQSEvent, context):
    for msg in event.records:
        print(f"Processing message {msg.message_id}: {msg.body}")

def lambda_handler(event, context):
    return router.dispatch(event, context)
```

## Features

- 🎯 Type-safe event handling with proper Python type hints
- 🔄 Support for multiple AWS event sources
- 🎨 Clean decorator-based routing
- 📦 Easy to extend with new event sources
- 🔒 Structured event objects with proper typing
- 🔍 Custom event handler support for unknown event types

## Event Sources

- [API Gateway](events/api-gateway.md) - Handle REST and HTTP API requests
- [SQS](events/sqs.md) - Process messages from queues
- [S3](events/s3.md) - React to object changes
- [DynamoDB Streams](events/dynamodb.md) - Handle table changes
- [Kinesis](events/kinesis.md) - Process data streams
- [SNS](events/sns.md) - Handle notifications
- [EventBridge](events/eventbridge.md) - Handle scheduled and custom events
- [Custom Events](events/custom.md) - Handle unknown event types

## Documentation

- [API Reference](api.md)
- [Examples](examples.md)
- [Contributing Guide](contributing.md)
- [Changelog](changelog.md)

## Links

- [GitHub Repository](https://github.com/raumildhandhukia/lambda-universal-router)
- [PyPI Package](https://pypi.org/project/lambda-universal-router)
- [Issue Tracker](https://github.com/raumildhandhukia/lambda-universal-router/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.