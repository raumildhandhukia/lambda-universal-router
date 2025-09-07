from __future__ import annotations
from typing import Any, Dict
from dataclasses import dataclass
from ..base import BaseEvent

@dataclass
class APIGatewayIdentity:
    """Represents the identity information in the request context.
    
    Attributes:
        cognito_identity_pool_id: The Amazon Cognito identity pool ID
        account_id: The AWS account ID associated with the request
        cognito_identity_id: The Amazon Cognito identity ID
        caller: The caller
        api_key: The API key associated with the request
        source_ip: The source IP address
        cognito_authentication_type: The Amazon Cognito authentication type
        cognito_authentication_provider: The Amazon Cognito authentication provider
        user_arn: The user ARN
        user_agent: The user agent
        user: The user
        access_key: The access key
    """
    cognito_identity_pool_id: str = ''
    account_id: str = ''
    cognito_identity_id: str = ''
    caller: str = ''
    api_key: str = ''
    source_ip: str = ''
    cognito_authentication_type: str = ''
    cognito_authentication_provider: str = ''
    user_arn: str = ''
    user_agent: str = ''
    user: str = ''
    access_key: str = ''

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> APIGatewayIdentity:
        return cls(
            cognito_identity_pool_id=data.get('cognitoIdentityPoolId', ''),
            account_id=data.get('accountId', ''),
            cognito_identity_id=data.get('cognitoIdentityId', ''),
            caller=data.get('caller', ''),
            api_key=data.get('apiKey', ''),
            source_ip=data.get('sourceIp', ''),
            cognito_authentication_type=data.get('cognitoAuthenticationType', ''),
            cognito_authentication_provider=data.get('cognitoAuthenticationProvider', ''),
            user_arn=data.get('userArn', ''),
            user_agent=data.get('userAgent', ''),
            user=data.get('user', ''),
            access_key=data.get('accessKey', '')
        )

@dataclass
class APIGatewayRequestContext:
    """Represents the request context from API Gateway.
    
    Attributes:
        account_id: The AWS account ID associated with the request
        resource_id: The identifier API Gateway assigns to your resource
        operation_name: The operation name
        stage: The deployment stage
        domain_name: The domain name
        domain_prefix: The domain prefix
        request_id: The request ID
        protocol: The protocol
        identity: The identity information
        resource_path: The resource path
        http_method: The HTTP method
        request_time: The request time
        request_time_epoch: The request time in epoch format
        path: The request path
    """
    account_id: str
    resource_id: str
    operation_name: str
    stage: str
    domain_name: str
    domain_prefix: str
    request_id: str
    protocol: str
    identity: APIGatewayIdentity
    resource_path: str
    http_method: str
    request_time: str
    request_time_epoch: int
    path: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> APIGatewayRequestContext:
        return cls(
            account_id=data.get('accountId', ''),
            resource_id=data.get('resourceId', ''),
            operation_name=data.get('operationName', ''),
            stage=data.get('stage', ''),
            domain_name=data.get('domainName', ''),
            domain_prefix=data.get('domainPrefix', ''),
            request_id=data.get('requestId', ''),
            protocol=data.get('protocol', ''),
            identity=APIGatewayIdentity.from_dict(data.get('identity', {})),
            resource_path=data.get('resourcePath', ''),
            http_method=data.get('httpMethod', ''),
            request_time=data.get('requestTime', ''),
            request_time_epoch=data.get('requestTimeEpoch', 0),
            path=data.get('path', '')
        )

class APIGatewayEvent(BaseEvent):
    """Represents an API Gateway REST API event.
    
    This class handles events from API Gateway REST APIs only.
    It does not support HTTP APIs or WebSocket APIs, which use different event formats.
    The event format follows the Lambda proxy integration structure for REST APIs.
    
    This event is triggered when an HTTP request is made to an API Gateway REST endpoint.
    It contains all the information about the HTTP request including method, path,
    headers, query parameters, body, and request context.
    
    Attributes:
        version: The payload version
        resource: The resource path defined in API Gateway
        path: The request path
        http_method: The HTTP method used
        headers: The request headers
        multi_value_headers: The multi-value request headers
        query_string_parameters: The request query string parameters
        multi_value_query_string_parameters: The multi-value query string parameters
        path_parameters: The request path parameters
        stage_variables: The stage variables defined in API Gateway
        request_context: The request context including identity information
        body: The request body
        is_base64_encoded: Whether the body is Base64-encoded
    """
    
    def _parse_event(self, event_dict: Dict[str, Any]) -> None:
        """Parse the raw event dictionary into structured API Gateway event data.
        
        Args:
            event_dict: The raw event dictionary from Lambda
        """
        self.version = event_dict.get('version', '')
        self.resource = event_dict.get('resource', '')
        self.path = event_dict.get('path', '')
        self.http_method = event_dict.get('httpMethod', '')
        self.headers = event_dict.get('headers', {})
        self.multi_value_headers = event_dict.get('multiValueHeaders', {})
        self.query_string_parameters = event_dict.get('queryStringParameters', {})
        self.multi_value_query_string_parameters = event_dict.get('multiValueQueryStringParameters', {})
        self.path_parameters = event_dict.get('pathParameters', {})
        self.stage_variables = event_dict.get('stageVariables', {})
        self.request_context = APIGatewayRequestContext.from_dict(
            event_dict.get('requestContext', {})
        )
        self.body = event_dict.get('body', '')
        self.is_base64_encoded = event_dict.get('isBase64Encoded', False)
