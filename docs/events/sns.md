# SNS (Simple Notification Service) Events

Amazon SNS allows you to process notifications from topics using Lambda functions.

## Event Structure

```python
class SNSEvent:
    records: List[SNSMessage]  # List of SNS messages

class SNSMessage:
    message_id: str           # Unique message ID
    topic_arn: str           # SNS topic ARN
    message: str             # Message content
    subject: str             # Message subject
    timestamp: str           # Message timestamp
    message_attributes: Dict[str, Any]  # Message attributes
```

## Usage Examples

### Basic Message Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import SNSEvent

router = Router()

@router.sns()
def process_notifications(event: SNSEvent, context):
    for message in event.records:
        print(f"Message ID: {message.message_id}")
        print(f"Subject: {message.subject}")
        print(f"Message: {message.message}")
        print(f"From topic: {message.topic_arn}")
```

### JSON Message Processing

```python
import json

@router.sns()
def process_json(event: SNSEvent, context):
    for message in event.records:
        try:
            data = json.loads(message.message)
            if data['type'] == 'alert':
                handle_alert(data)
            elif data['type'] == 'notification':
                handle_notification(data)
        except json.JSONDecodeError:
            print(f"Invalid JSON in message: {message.message_id}")
```

### Topic-Based Processing

```python
@router.sns()
def handle_by_topic(event: SNSEvent, context):
    for message in event.records:
        if 'alerts' in message.topic_arn:
            process_alert(message)
        elif 'notifications' in message.topic_arn:
            process_notification(message)
        elif 'metrics' in message.topic_arn:
            process_metrics(message)
```

### Message Attributes

```python
@router.sns()
def process_with_attributes(event: SNSEvent, context):
    for message in event.records:
        # Check message attributes
        message_type = message.message_attributes.get('MessageType', {}).get('Value')
        if message_type == 'CRITICAL':
            handle_critical(message)
        else:
            handle_normal(message)
```

## Event Examples

1. **Basic SNS Event**
   ```python
   {
       "Records": [
           {
               "EventSource": "aws:sns",
               "EventVersion": "1.0",
               "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
               "Sns": {
                   "Type": "Notification",
                   "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                   "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                   "Subject": "Example notification",
                   "Message": "Hello from SNS!",
                   "Timestamp": "2024-03-17T12:00:00.000Z",
                   "MessageAttributes": {
                       "MessageType": {
                           "Type": "String",
                           "Value": "CRITICAL"
                       }
                   }
               }
           }
       ]
   }
   ```

2. **JSON Message**
   ```python
   {
       "Records": [
           {
               "Sns": {
                   "Message": "{\"type\":\"alert\",\"severity\":\"high\",\"message\":\"System alert\"}",
                   "MessageAttributes": {
                       "AlertType": {
                           "Type": "String",
                           "Value": "SystemAlert"
                       }
                   }
               }
           }
       ]
   }
   ```

## Best Practices

1. **Error Handling**
   ```python
   @router.sns()
   def safe_process(event: SNSEvent, context):
       for message in event.records:
           try:
               process_message(message)
           except ValidationError:
               # Message validation failed
               log_validation_error(message)
           except ProcessingError as e:
               # Processing error
               handle_processing_error(message, e)
           except Exception as e:
               # Unexpected error
               log_error(message, e)
               raise
   ```

2. **Message Validation**
   ```python
   @router.sns()
   def validate_messages(event: SNSEvent, context):
       for message in event.records:
           try:
               data = json.loads(message.message)
               if not is_valid_schema(data):
                   log_invalid_schema(message)
                   continue
               process_valid_message(data)
           except json.JSONDecodeError:
               log_invalid_json(message)
   ```

3. **Monitoring**
   ```python
   @router.sns()
   def monitored_process(event: SNSEvent, context):
       metrics = {
           "processed": 0,
           "errors": 0,
           "by_type": {}
       }
       
       for message in event.records:
           try:
               msg_type = get_message_type(message)
               metrics["by_type"][msg_type] = metrics["by_type"].get(msg_type, 0) + 1
               process_message(message)
               metrics["processed"] += 1
           except Exception:
               metrics["errors"] += 1
       
       log_metrics(metrics)
   ```

## Configuration Tips

1. **SNS Topic Settings**
   - Configure appropriate access policies
   - Set up topic subscriptions
   - Enable message attributes if needed

2. **Lambda Settings**
   - Set appropriate memory and timeout
   - Configure error handling
   - Enable X-Ray tracing if needed

3. **Security**
   - Use encryption for sensitive data
   - Validate message sources
   - Implement proper access controls

## See Also

- [Using AWS Lambda with Amazon SNS](https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html)
- [Amazon SNS Message Attributes](https://docs.aws.amazon.com/sns/latest/dg/sns-message-attributes.html)
- [SNS Message Filtering](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html)
