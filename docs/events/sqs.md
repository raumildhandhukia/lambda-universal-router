# SQS (Simple Queue Service) Events

Amazon SQS allows you to process messages from both standard and FIFO queues using Lambda functions.

## Event Structure

```python
class SQSEvent:
    records: List[SQSMessage]  # List of SQS messages

class SQSMessage:
    message_id: str           # Unique message ID
    body: str                 # Message body
    attributes: Dict[str, Any]  # Message attributes
```

## Usage Examples

### Basic Message Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import SQSEvent

router = Router()

@router.sqs()
def process_messages(event: SQSEvent, context):
    for message in event.records:
        print(f"Processing message {message.message_id}")
        print(f"Message body: {message.body}")
```

### JSON Message Processing

```python
import json

@router.sqs()
def process_json(event: SQSEvent, context):
    for message in event.records:
        try:
            data = json.loads(message.body)
            process_order(data)
        except json.JSONDecodeError:
            print(f"Invalid JSON in message: {message.message_id}")
```

### Message Attributes

```python
@router.sqs()
def process_with_attributes(event: SQSEvent, context):
    for message in event.records:
        # Check message attributes
        priority = message.attributes.get('Priority', {}).get('StringValue')
        if priority == 'HIGH':
            process_priority_message(message)
        else:
            process_normal_message(message)
```

### Batch Processing with Error Handling

```python
@router.sqs()
def safe_batch_process(event: SQSEvent, context):
    results = {
        "successful": [],
        "failed": []
    }
    
    for message in event.records:
        try:
            process_message(message.body)
            results["successful"].append(message.message_id)
        except Exception as e:
            results["failed"].append({
                "message_id": message.message_id,
                "error": str(e)
            })
    
    return results
```

## Event Examples

1. **Standard Message**
   ```python
   {
       "Records": [
           {
               "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
               "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
               "body": "Hello World",
               "attributes": {
                   "ApproximateReceiveCount": "1",
                   "SentTimestamp": "1545082649183",
                   "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                   "ApproximateFirstReceiveTimestamp": "1545082649185"
               },
               "messageAttributes": {
                   "Priority": {
                       "stringValue": "HIGH",
                       "dataType": "String"
                   }
               },
               "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
               "eventSource": "aws:sqs",
               "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
               "awsRegion": "us-east-1"
           }
       ]
   }
   ```

2. **FIFO Queue Message**
   ```python
   {
       "Records": [
           {
               "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
               "body": "Hello World",
               "attributes": {
                   "MessageGroupId": "group1",
                   "MessageDeduplicationId": "dedupe1",
                   "SequenceNumber": "123456789"
               },
               "eventSource": "aws:sqs"
           }
       ]
   }
   ```

## Best Practices

1. **Error Handling**
   ```python
   @router.sqs()
   def robust_processing(event: SQSEvent, context):
       for message in event.records:
           try:
               process_message(message)
           except ValidationError:
               # Message is invalid, send to DLQ
               send_to_dlq(message)
           except TemporaryError:
               # Temporary failure, message will be retried
               raise
           except Exception as e:
               # Unexpected error
               log_error(message, e)
               raise
   ```

2. **Message Validation**
   ```python
   @router.sqs()
   def validate_messages(event: SQSEvent, context):
       for message in event.records:
           if not is_valid_message(message.body):
               # Invalid message, log and skip
               print(f"Invalid message: {message.message_id}")
               continue
           process_valid_message(message)
   ```

3. **Batch Size Handling**
   ```python
   @router.sqs()
   def batch_process(event: SQSEvent, context):
       if len(event.records) >= 10:
           # Large batch, process in parallel
           process_parallel(event.records)
       else:
           # Small batch, process sequentially
           process_sequential(event.records)
   ```

## Configuration Tips

1. **Queue Settings**
   - Set appropriate visibility timeout
   - Configure DLQ for failed messages
   - Adjust batch size based on processing needs

2. **Lambda Settings**
   - Set memory based on processing needs
   - Configure timeout considering batch size
   - Enable active tracing for debugging

3. **Monitoring**
   ```python
   @router.sqs()
   def monitored_process(event: SQSEvent, context):
       start_time = time.time()
       metrics = {"processed": 0, "errors": 0}
       
       for message in event.records:
           try:
               process_message(message)
               metrics["processed"] += 1
           except Exception:
               metrics["errors"] += 1
       
       metrics["duration"] = time.time() - start_time
       log_metrics(metrics)
   ```

## See Also

- [AWS Lambda SQS Integration](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html)
- [Amazon SQS Documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [SQS FIFO Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html)
