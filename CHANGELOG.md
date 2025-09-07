# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2024-03-17

### Added
- Comprehensive GitHub Pages documentation
- Direct links to documentation, changelog, and license
- Improved PyPI package metadata

## [0.2.1] - 2024-03-17

### Changed
- Enhanced documentation with comprehensive examples
- Added detailed API documentation
- Added examples for all event types
- Improved type hints documentation

## [0.2.0] - 2024-03-17

### Added
- Custom event handler support as fallback
- DynamoDB Streams event support
- Kinesis Stream event support
- SNS event support
- EventBridge/CloudWatch Events support
- Comprehensive test coverage for all event types
- Better organization of event handlers in separate files

### Changed
- Moved all event types to their own files in the events directory
- Improved error handling and type safety
- Updated documentation with new event types and examples

## [0.1.0] - 2024-03-17

### Added
- Initial release of Lambda Universal Router
- Support for API Gateway events with path and method routing
- Support for SQS events
- Support for S3 events
- Basic event parsing and type safety
- Example code and documentation