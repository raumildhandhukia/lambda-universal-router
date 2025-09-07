from __future__ import annotations
import pytest
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent, S3Event

@pytest.fixture
def router():
    return Router()

def test_api_gateway_routing(router):
    @router.apigateway("/test", method="GET")
    def handler(event: APIGatewayEvent, context):
        return {"statusCode": 200, "body": "test"}

    event = {
        "httpMethod": "GET",
        "path": "/test",
        "requestContext": {
            "httpMethod": "GET",
            "path": "/test",
            "stage": "prod",
            "requestId": "test-id"
        },
        "headers": {},
        "queryStringParameters": {},
        "pathParameters": {}
    }

    result = router.dispatch(event, {})
    assert result["statusCode"] == 200
    assert result["body"] == "test"

def test_sqs_routing(router):
    @router.sqs()
    def handler(event: SQSEvent, context):
        return "processed"

    event = {
        "Records": [{
            "messageId": "test",
            "body": "test message",
            "messageAttributes": {},
            "eventSource": "aws:sqs"
        }]
    }

    result = router.dispatch(event, {})
    assert result == "processed"

def test_s3_routing(router):
    @router.s3()
    def handler(event: S3Event, context):
        return "processed"

    event = {
        "Records": [{
            "eventName": "ObjectCreated:Put",
            "eventTime": "2024-03-17T12:00:00.000Z",
            "s3": {
                "bucket": {
                    "name": "test-bucket",
                    "arn": "arn:aws:s3:::test-bucket"
                },
                "object": {
                    "key": "test.txt",
                    "size": 123,
                    "eTag": "abc123"
                }
            },
            "eventSource": "aws:s3"
        }]
    }

    result = router.dispatch(event, {})
    assert result == "processed"

def test_invalid_event_type(router):
    event = {
        "invalid": "event"
    }
    
    with pytest.raises(ValueError, match="No handler found for the given event type"):
        router.dispatch(event, {})