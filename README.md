# Lambda Universal Router

[![PyPI version](https://badge.fury.io/py/lambda-universal-router.svg)](https://badge.fury.io/py/lambda-universal-router)
[![Python Support](https://img.shields.io/pypi/pyversions/lambda-universal-router.svg)](https://pypi.org/project/lambda-universal-router/)
[![License](https://img.shields.io/github/license/raumildhandhukia/lambda-universal-router.svg)](https://github.com/raumildhandhukia/lambda-universal-router/blob/main/LICENSE)

A flexible and type-safe router for AWS Lambda functions that supports multiple event sources. This library makes it easy to handle different types of AWS Lambda events in a clean and organized way.

## Features

- 🎯 Type-safe event handling with proper Python type hints
- 🔄 Support for multiple AWS event sources
- 🎨 Clean decorator-based routing
- 📦 Easy to extend with new event sources
- 🔒 Structured event objects with proper typing
- 🔍 Custom event handler support for unknown event types

## Installation

```bash
pip install lambda-universal-router
```

## Quick Start

```python
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent, CustomEvent

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

@router.custom()
def handle_unknown(event: CustomEvent, context):
    print(f"Handling unknown event type: {event.event_data}")

def lambda_handler(event, context):
    return router.dispatch(event, context)
```

## Supported Event Sources

### 1. API Gateway (REST/HTTP APIs)
```python
from lambda_universal_router.events import APIGatewayEvent

@router.apigateway("/users/{id}", method="GET")
def get_user(event: APIGatewayEvent, context):
    user_id = event.path_parameters['id']
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {"id": user_id, "name": "John Doe"}
    }
```
Available properties:
- `http_method`: HTTP method (GET, POST, etc.)
- `path`: Request path
- `headers`: Request headers
- `query_string_parameters`: Query string parameters
- `path_parameters`: Path parameters
- `body`: Request body
- `request_context`: API Gateway request context

### 2. SQS (Simple Queue Service)
```python
from lambda_universal_router.events import SQSEvent

@router.sqs()
def process_messages(event: SQSEvent, context):
    for msg in event.records:
        print(f"Message ID: {msg.message_id}")
        print(f"Body: {msg.body}")
        print(f"Attributes: {msg.attributes}")
```
Available properties:
- `records`: List of SQS messages
- Each record has:
  - `message_id`: Unique message ID
  - `body`: Message body
  - `attributes`: Message attributes

### 3. S3 (Object Storage)
```python
from lambda_universal_router.events import S3Event

@router.s3()
def handle_s3_events(event: S3Event, context):
    for record in event.records:
        print(f"Bucket: {record.bucket.name}")
        print(f"Key: {record.s3_object.key}")
        print(f"Event: {record.event_name}")
```
Available properties:
- `records`: List of S3 events
- Each record has:
  - `event_name`: Type of event (e.g., ObjectCreated:Put)
  - `bucket`: Bucket information (name, arn)
  - `s3_object`: Object information (key, size, etag)

### 4. DynamoDB Streams
```python
from lambda_universal_router.events import DynamoDBStreamEvent

@router.dynamodb()
def handle_dynamodb_changes(event: DynamoDBStreamEvent, context):
    for record in event.records:
        print(f"Event Type: {record.event_name}")  # INSERT, MODIFY, REMOVE
        print(f"DynamoDB: {record.dynamodb}")  # Contains Keys, NewImage, OldImage
```
Available properties:
- `records`: List of DynamoDB Stream records
- Each record has:
  - `event_id`: Unique event ID
  - `event_name`: Type of change (INSERT/MODIFY/REMOVE)
  - `dynamodb`: Changed data (keys, new/old images)

### 5. Kinesis Streams
```python
from lambda_universal_router.events import KinesisStreamEvent

@router.kinesis()
def process_stream(event: KinesisStreamEvent, context):
    for record in event.records:
        print(f"Partition Key: {record.partition_key}")
        print(f"Data: {record.data}")  # Base64-decoded data
```
Available properties:
- `records`: List of Kinesis records
- Each record has:
  - `kinesis_schema_version`: Schema version
  - `partition_key`: Partition key
  - `sequence_number`: Sequence number
  - `data`: Base64-decoded data
  - `approximate_arrival_timestamp`: Timestamp

### 6. SNS (Simple Notification Service)
```python
from lambda_universal_router.events import SNSEvent

@router.sns()
def handle_notifications(event: SNSEvent, context):
    for msg in event.records:
        print(f"Message: {msg.message}")
        print(f"Topic: {msg.topic_arn}")
```
Available properties:
- `records`: List of SNS messages
- Each message has:
  - `message_id`: Unique message ID
  - `topic_arn`: SNS topic ARN
  - `message`: Message content
  - `subject`: Message subject
  - `timestamp`: Message timestamp
  - `message_attributes`: Message attributes

### 7. EventBridge (CloudWatch Events)
```python
from lambda_universal_router.events import EventBridgeEvent

@router.eventbridge()
def handle_scheduled_event(event: EventBridgeEvent, context):
    print(f"Source: {event.source}")
    print(f"Detail Type: {event.detail_type}")
    print(f"Detail: {event.detail.raw_detail}")
```
Available properties:
- `version`: Event version
- `id`: Event ID
- `detail_type`: Type of event
- `source`: Event source
- `account`: AWS account ID
- `time`: Event time
- `region`: AWS region
- `resources`: List of affected resources
- `detail`: Event details

### 8. Custom Events
```python
from lambda_universal_router.events import CustomEvent

@router.custom()
def handle_unknown_events(event: CustomEvent, context):
    # Fallback handler for unknown event types
    print(f"Raw event data: {event.event_data}")
    return "Processed unknown event type"
```
Available properties:
- `event_data`: Raw event dictionary

## Error Handling

The router will raise a `ValueError` if:
- No handler is found for an event type
- Multiple custom handlers are registered (only one is allowed)

## Type Safety

All event types are properly typed with Python type hints, providing:
- IDE autocompletion
- Type checking support
- Runtime type safety

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.