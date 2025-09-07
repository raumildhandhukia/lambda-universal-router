# Custom Events

The custom event handler provides a fallback mechanism for handling unknown or custom event types that don't match any of the standard AWS event patterns.

## Event Structure

```python
class CustomEvent:
    event_data: Dict[str, Any]  # Raw event dictionary
```

## Usage Examples

### Basic Custom Handler

```python
from lambda_universal_router import Router
from lambda_universal_router.events import CustomEvent

router = Router()

@router.custom()
def handle_unknown(event: CustomEvent, context):
    print(f"Received unknown event: {event.event_data}")
    
    # Try to identify event type
    if 'Records' in event.event_data:
        return handle_record_based_event(event.event_data)
    elif 'detail-type' in event.event_data:
        return handle_eventbridge_like_event(event.event_data)
    else:
        return handle_generic_event(event.event_data)
```

### Event Type Detection

```python
@router.custom()
def smart_handler(event: CustomEvent, context):
    # Try to determine event type from structure
    if is_api_event(event.event_data):
        return handle_api_event(event.event_data)
    elif is_queue_event(event.event_data):
        return handle_queue_event(event.event_data)
    elif is_stream_event(event.event_data):
        return handle_stream_event(event.event_data)
    else:
        return handle_unknown_event(event.event_data)

def is_api_event(data: Dict[str, Any]) -> bool:
    return 'httpMethod' in data and 'path' in data

def is_queue_event(data: Dict[str, Any]) -> bool:
    return ('Records' in data and len(data['Records']) > 0 and
            'eventSource' in data['Records'][0])

def is_stream_event(data: Dict[str, Any]) -> bool:
    return 'Records' in data and 'kinesis' in data.get('Records', [{}])[0]
```

### Custom Event Processing

```python
@router.custom()
def process_custom_events(event: CustomEvent, context):
    # Handle custom application events
    if 'type' in event.event_data:
        event_type = event.event_data['type']
        
        if event_type == 'user.created':
            return handle_user_created(event.event_data)
        elif event_type == 'order.placed':
            return handle_order_placed(event.event_data)
        elif event_type == 'payment.processed':
            return handle_payment_processed(event.event_data)
    
    return {
        "statusCode": 200,
        "body": "Event processed"
    }
```

### Logging and Monitoring

```python
@router.custom()
def monitored_handler(event: CustomEvent, context):
    # Log unknown event type for analysis
    log_unknown_event_type(event.event_data)
    
    try:
        # Try to process the event
        result = process_unknown_event(event.event_data)
        
        # Track successful processing
        track_success(event.event_data)
        
        return result
    except Exception as e:
        # Track failure
        track_failure(event.event_data, str(e))
        raise
```

## Event Examples

1. **Custom Application Event**
   ```python
   {
       "type": "user.created",
       "timestamp": "2024-03-17T12:00:00Z",
       "data": {
           "user_id": "123",
           "email": "user@example.com",
           "name": "John Doe"
       }
   }
   ```

2. **Third-Party Webhook**
   ```python
   {
       "webhook_id": "abc123",
       "event": "payment.success",
       "payload": {
           "transaction_id": "tx_123",
           "amount": 99.99,
           "currency": "USD"
       }
   }
   ```

## Best Practices

1. **Event Type Detection**
   ```python
   def detect_event_type(event_data: Dict[str, Any]) -> str:
       if 'httpMethod' in event_data:
           return 'api'
       elif 'Records' in event_data:
           if 'eventSource' in event_data['Records'][0]:
               return event_data['Records'][0]['eventSource']
       elif 'detail-type' in event_data:
           return 'eventbridge'
       return 'unknown'
   ```

2. **Error Handling**
   ```python
   @router.custom()
   def safe_handler(event: CustomEvent, context):
       try:
           # Try to process the event
           event_type = detect_event_type(event.event_data)
           handler = get_handler_for_type(event_type)
           return handler(event.event_data)
       except ValueError as e:
           # Invalid event data
           log_validation_error(event.event_data, str(e))
           return {
               "statusCode": 400,
               "body": "Invalid event data"
           }
       except Exception as e:
           # Unexpected error
           log_error(event.event_data, str(e))
           raise
   ```

3. **Logging**
   ```python
   @router.custom()
   def logging_handler(event: CustomEvent, context):
       # Log event metadata
       log_event_metadata(event.event_data)
       
       # Process event
       result = process_event(event.event_data)
       
       # Log result
       log_event_result(event.event_data, result)
       
       return result
   ```

## Configuration Tips

1. **Event Validation**
   - Implement schema validation
   - Check required fields
   - Validate data types

2. **Performance**
   - Cache handler lookups
   - Batch similar events
   - Implement timeouts

3. **Security**
   - Validate event sources
   - Check authentication
   - Sanitize input data

## Common Use Cases

1. **Third-Party Webhooks**
   ```python
   @router.custom()
   def webhook_handler(event: CustomEvent, context):
       # Verify webhook signature
       if not verify_webhook_signature(event.event_data):
           return {"statusCode": 401, "body": "Invalid signature"}
       
       # Process webhook
       webhook_type = event.event_data.get('type')
       handler = get_webhook_handler(webhook_type)
       return handler(event.event_data)
   ```

2. **Custom Application Events**
   ```python
   @router.custom()
   def app_event_handler(event: CustomEvent, context):
       event_type = event.event_data.get('type', '')
       
       # Route to specific handler
       if event_type.startswith('user.'):
           return handle_user_event(event.event_data)
       elif event_type.startswith('order.'):
           return handle_order_event(event.event_data)
       
       return handle_generic_event(event.event_data)
   ```

## See Also

- [AWS Lambda Function Handler](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- [Lambda Function Event Object](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-concepts.html#gettingstarted-concepts-event)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
