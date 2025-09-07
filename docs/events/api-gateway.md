# API Gateway REST API Events

The API Gateway integration in this library specifically handles RESTful API requests in your Lambda functions. This integration supports the REST API type in API Gateway (not HTTP APIs or WebSocket APIs).

## Supported Features

1. **REST API Only**
   - Full support for REST API event format
   - Path-based routing with parameters
   - Method-based routing (GET, POST, PUT, DELETE, etc.)
   - Request/response mapping
   - Note: HTTP APIs and WebSocket APIs are not supported

2. **Integration Type**
   - Designed for Lambda proxy integration
   - Handles API Gateway's proxy event format
   - Automatically maps request/response structures

## Event Structure

```python
class APIGatewayEvent:
    http_method: str          # HTTP method (GET, POST, etc.)
    path: str                 # Request path
    headers: Dict[str, str]   # Request headers
    query_string_parameters: Dict[str, str]  # Query parameters
    path_parameters: Dict[str, str]          # Path parameters
    body: str                 # Request body
    request_context: APIGatewayRequestContext  # Request context

class APIGatewayRequestContext:
    http_method: str    # HTTP method
    path: str          # Request path
    stage: str         # API stage
    request_id: str    # Unique request ID
```

## Usage

### Basic Routing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent

router = Router()

@router.apigateway("/hello", method="GET")
def hello(event: APIGatewayEvent, context):
    return {
        "statusCode": 200,
        "body": "Hello, World!"
    }
```

### Path Parameters

```python
@router.apigateway("/users/{user_id}", method="GET")
def get_user(event: APIGatewayEvent, context):
    user_id = event.path_parameters['user_id']
    return {
        "statusCode": 200,
        "body": {"id": user_id}
    }
```

### Query Parameters

```python
@router.apigateway("/search", method="GET")
def search(event: APIGatewayEvent, context):
    query = event.query_string_parameters.get('q', '')
    limit = event.query_string_parameters.get('limit', '10')
    return {
        "statusCode": 200,
        "body": {
            "query": query,
            "limit": int(limit)
        }
    }
```

### POST Requests with JSON Body

```python
@router.apigateway("/users", method="POST")
def create_user(event: APIGatewayEvent, context):
    body = json.loads(event.body)
    return {
        "statusCode": 201,
        "body": {
            "message": "User created",
            "user": body
        }
    }
```

### Custom Headers

```python
@router.apigateway("/secure", method="GET")
def secure_endpoint(event: APIGatewayEvent, context):
    auth_header = event.headers.get('Authorization')
    if not auth_header:
        return {
            "statusCode": 401,
            "body": "Unauthorized"
        }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "X-Custom-Header": "value"
        },
        "body": "Secure content"
    }
```

## Best Practices

1. **Type Safety**
   ```python
   def handler(event: APIGatewayEvent, context):
       # Type hints provide IDE support
       event.query_string_parameters  # Auto-complete works
   ```

2. **Error Handling**
   ```python
   @router.apigateway("/users/{id}", method="GET")
   def get_user(event: APIGatewayEvent, context):
       try:
           user_id = event.path_parameters['id']
           # ... fetch user ...
           return {"statusCode": 200, "body": user}
       except KeyError:
           return {"statusCode": 400, "body": "Missing user ID"}
       except Exception as e:
           return {"statusCode": 500, "body": str(e)}
   ```

3. **Response Format**
   ```python
   def format_response(status_code: int, body: Any) -> Dict[str, Any]:
       return {
           "statusCode": status_code,
           "headers": {
               "Content-Type": "application/json"
           },
           "body": json.dumps(body)
       }
   ```

## Common Issues

1. **Missing Body Parsing**
   ```python
   # Wrong
   data = event.body  # body is a string!

   # Right
   data = json.loads(event.body)
   ```

2. **Path Parameter Access**
   ```python
   # Wrong
   user_id = event.path_parameters['id']  # May raise KeyError

   # Right
   user_id = event.path_parameters.get('id')
   if not user_id:
       return {"statusCode": 400, "body": "Missing ID"}
   ```

## Limitations

1. **HTTP API Support**
   - This library does not support API Gateway HTTP APIs
   - HTTP APIs use a different event format
   - If you need HTTP API support, please open an issue

2. **WebSocket Support**
   - WebSocket APIs are not supported
   - WebSocket APIs require different event handling
   - Consider using a separate library for WebSocket support

## See Also

- [API Gateway REST API Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html)
- [REST API vs HTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html)
- [Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html)
