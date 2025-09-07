# Lambda Universal Router API Documentation

## Router Class

The main class for handling AWS Lambda events.

### Methods

#### `__init__()`
Initialize a new router instance.

#### `apigateway(path: str, method: str = "GET") -> Callable`
Decorator for API Gateway event handlers.
- `path`: URL path to match (supports path parameters)
- `method`: HTTP method to match (GET, POST, etc.)

#### `sqs() -> Callable`
Decorator for SQS event handlers.

#### `s3() -> Callable`
Decorator for S3 event handlers.

#### `dynamodb() -> Callable`
Decorator for DynamoDB Stream event handlers.

#### `kinesis() -> Callable`
Decorator for Kinesis Stream event handlers.

#### `sns() -> Callable`
Decorator for SNS event handlers.

#### `eventbridge() -> Callable`
Decorator for EventBridge/CloudWatch Events handlers.

#### `custom() -> Callable`
Decorator for custom event handlers (fallback for unknown event types).

#### `dispatch(event: Dict[str, Any], context: Any) -> Any`
Dispatch an event to the appropriate handler.
- `event`: AWS Lambda event dictionary
- `context`: AWS Lambda context object
- Returns: Handler's return value
- Raises: ValueError if no handler is found

## Event Classes

### APIGatewayEvent
Represents an API Gateway event.
```python
class APIGatewayEvent:
    http_method: str
    path: str
    headers: Dict[str, str]
    query_string_parameters: Dict[str, str]
    path_parameters: Dict[str, str]
    body: str
    request_context: APIGatewayRequestContext
```

### SQSEvent
Represents an SQS event.
```python
class SQSEvent:
    records: List[SQSMessage]

class SQSMessage:
    message_id: str
    body: str
    attributes: Dict[str, Any]
```

### S3Event
Represents an S3 event.
```python
class S3Event:
    records: List[S3Record]

class S3Record:
    event_name: str
    event_time: str
    bucket: S3Bucket
    s3_object: S3Object

class S3Bucket:
    name: str
    arn: str

class S3Object:
    key: str
    size: int
    etag: str
```

### DynamoDBStreamEvent
Represents a DynamoDB Stream event.
```python
class DynamoDBStreamEvent:
    records: List[DynamoDBStreamRecord]

class DynamoDBStreamRecord:
    event_id: str
    event_name: str
    event_version: str
    event_source: str
    aws_region: str
    dynamodb: Dict[str, Any]
```

### KinesisStreamEvent
Represents a Kinesis Stream event.
```python
class KinesisStreamEvent:
    records: List[KinesisRecord]

class KinesisRecord:
    kinesis_schema_version: str
    partition_key: str
    sequence_number: str
    data: bytes
    approximate_arrival_timestamp: float
```

### SNSEvent
Represents an SNS event.
```python
class SNSEvent:
    records: List[SNSMessage]

class SNSMessage:
    message_id: str
    topic_arn: str
    message: str
    subject: str
    timestamp: str
    message_attributes: Dict[str, Any]
```

### EventBridgeEvent
Represents an EventBridge/CloudWatch Events event.
```python
class EventBridgeEvent:
    version: str
    id: str
    detail_type: str
    source: str
    account: str
    time: str
    region: str
    resources: List[str]
    detail: EventBridgeDetail
```

### CustomEvent
Represents a custom or unknown event type.
```python
class CustomEvent:
    event_data: Dict[str, Any]  # Raw event dictionary
```

## Best Practices

1. **Type Safety**
   - Always use type hints with event classes
   - Let your IDE help you with autocompletion
   - Run a type checker (e.g., mypy) on your code

2. **Error Handling**
   - Handle exceptions in your handlers
   - Use the custom handler for unknown event types
   - Validate event data before processing

3. **Testing**
   - Write unit tests for your handlers
   - Use the provided event classes for type safety
   - Test error cases and edge conditions

4. **Performance**
   - Keep handlers focused and lightweight
   - Use async/await when appropriate
   - Consider cold start times

5. **Security**
   - Validate input data
   - Don't log sensitive information
   - Follow AWS security best practices

## Examples

See the [examples](../examples/) directory for more detailed examples.
