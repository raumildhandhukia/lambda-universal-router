# Lambda Universal Router Documentation

A flexible and type-safe router for AWS Lambda functions that supports multiple event sources.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Event Sources](#event-sources)
- [API Reference](api.md)
- [Examples](examples.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)

## Installation

```bash
pip install lambda-universal-router
```

## Quick Start

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

## Event Sources

### API Gateway
Handle REST and HTTP API events with path and method-based routing:

```python
@router.apigateway("/users/{id}", method="GET")
def get_user(event: APIGatewayEvent, context):
    user_id = event.path_parameters['id']
    return {
        "statusCode": 200,
        "body": {"id": user_id}
    }
```

[Learn more about API Gateway events](events/api-gateway.md)

### SQS (Simple Queue Service)
Process messages from SQS queues:

```python
@router.sqs()
def handle_messages(event: SQSEvent, context):
    for msg in event.records:
        print(f"Message ID: {msg.message_id}")
        print(f"Body: {msg.body}")
```

[Learn more about SQS events](events/sqs.md)

### S3 (Object Storage)
React to S3 bucket events:

```python
@router.s3()
def handle_s3(event: S3Event, context):
    for record in event.records:
        print(f"Bucket: {record.bucket.name}")
        print(f"File: {record.s3_object.key}")
```

[Learn more about S3 events](events/s3.md)

### DynamoDB Streams
Handle DynamoDB table changes:

```python
@router.dynamodb()
def handle_changes(event: DynamoDBStreamEvent, context):
    for record in event.records:
        print(f"Operation: {record.event_name}")
        print(f"Data: {record.dynamodb}")
```

[Learn more about DynamoDB events](events/dynamodb.md)

### Kinesis Streams
Process records from Kinesis streams:

```python
@router.kinesis()
def handle_stream(event: KinesisStreamEvent, context):
    for record in event.records:
        print(f"Data: {record.data}")
```

[Learn more about Kinesis events](events/kinesis.md)

### SNS (Simple Notification Service)
Handle SNS notifications:

```python
@router.sns()
def handle_notifications(event: SNSEvent, context):
    for msg in event.records:
        print(f"Message: {msg.message}")
```

[Learn more about SNS events](events/sns.md)

### EventBridge (CloudWatch Events)
Handle scheduled and custom events:

```python
@router.eventbridge()
def handle_events(event: EventBridgeEvent, context):
    print(f"Event type: {event.detail_type}")
    print(f"Details: {event.detail.raw_detail}")
```

[Learn more about EventBridge events](events/eventbridge.md)

### Custom Events
Handle unknown or custom event types:

```python
@router.custom()
def handle_unknown(event: CustomEvent, context):
    print(f"Raw event: {event.event_data}")
```

[Learn more about Custom events](events/custom.md)

## Next Steps

- Check out the [API Reference](api.md) for detailed documentation
- See [Examples](examples.md) for more use cases
- Learn how to [Contribute](contributing.md)
- View the [Changelog](changelog.md)
