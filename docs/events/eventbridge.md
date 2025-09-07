# EventBridge (CloudWatch Events)

Amazon EventBridge (formerly CloudWatch Events) allows you to respond to state changes in your AWS resources and custom events.

## Event Structure

```python
class EventBridgeEvent:
    version: str          # Event version
    id: str              # Unique event ID
    detail_type: str     # Type of event (e.g., "Scheduled Event")
    source: str          # Event source (e.g., "aws.events")
    account: str         # AWS account ID
    time: str           # Event timestamp
    region: str         # AWS region
    resources: List[str] # Affected AWS resources
    detail: Dict[str, Any]  # Event-specific details
```

## Usage Examples

### Scheduled Tasks

```python
from lambda_universal_router import Router
from lambda_universal_router.events import EventBridgeEvent

router = Router()

@router.eventbridge()
def daily_cleanup(event: EventBridgeEvent, context):
    if event.detail_type == "Scheduled Event":
        print(f"Running daily cleanup at {event.time}")
        # Perform cleanup tasks
```

### AWS Service Events

```python
@router.eventbridge()
def handle_ec2_changes(event: EventBridgeEvent, context):
    if event.source == "aws.ec2" and event.detail_type == "EC2 Instance State-change Notification":
        instance_id = event.detail.get('instance-id')
        state = event.detail.get('state')
        print(f"Instance {instance_id} changed to state: {state}")
```

### Custom Events

```python
@router.eventbridge()
def handle_custom_events(event: EventBridgeEvent, context):
    if event.source == "my.application":
        if event.detail_type == "UserSignup":
            handle_new_user(event.detail)
        elif event.detail_type == "OrderPlaced":
            process_order(event.detail)
```

### Cross-Account Events

```python
@router.eventbridge()
def handle_multi_account(event: EventBridgeEvent, context):
    print(f"Event from account: {event.account}")
    print(f"In region: {event.region}")
    print(f"Affected resources: {event.resources}")
```

## Common Event Types

1. **Scheduled Events**
   ```python
   {
       "version": "0",
       "id": "53dc4d37-cffa-4f76-80c9-8b7d4a4d2eaa",
       "detail-type": "Scheduled Event",
       "source": "aws.events",
       "account": "123456789012",
       "time": "2019-10-08T16:53:06Z",
       "region": "us-east-1",
       "resources": ["arn:aws:events:us-east-1:123456789012:rule/MyScheduledRule"],
       "detail": {}
   }
   ```

2. **AWS Service Events**
   ```python
   {
       "version": "0",
       "id": "7bf73129-1428-4cd3-a780-95db273d1602",
       "detail-type": "EC2 Instance State-change Notification",
       "source": "aws.ec2",
       "account": "123456789012",
       "time": "2019-11-11T21:29:54Z",
       "region": "us-east-1",
       "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0"],
       "detail": {
           "instance-id": "i-1234567890abcdef0",
           "state": "running"
       }
   }
   ```

3. **Custom Events**
   ```python
   {
       "version": "0",
       "id": "6a7e8feb-b491-4cf7-a9f1-bf3703467718",
       "detail-type": "OrderPlaced",
       "source": "my.application",
       "account": "123456789012",
       "time": "2019-12-02T17:22:43Z",
       "region": "us-east-1",
       "resources": [],
       "detail": {
           "orderId": "12345",
           "amount": 123.45
       }
   }
   ```

## Best Practices

1. **Event Pattern Matching**
   - Check both `source` and `detail-type`
   - Use type hints for better code completion
   - Handle unknown event types gracefully

2. **Error Handling**
   ```python
   @router.eventbridge()
   def handle_events(event: EventBridgeEvent, context):
       try:
           if event.detail_type == "Scheduled Event":
               process_scheduled_task()
           else:
               log_unknown_event(event)
       except Exception as e:
           handle_error(e, event)
   ```

3. **Logging**
   ```python
   @router.eventbridge()
   def handle_events(event: EventBridgeEvent, context):
       print(f"Processing {event.detail_type} from {event.source}")
       print(f"Event details: {event.detail}")
   ```

## See Also

- [Amazon EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [EventBridge Event Patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
- [AWS Lambda EventBridge Integration](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents.html)
