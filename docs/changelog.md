# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Class-based structure for geometry operations
- Class-based structure for H3 operations
- Improved file I/O with multiple format support
- Comprehensive documentation
- Type hints throughout the codebase
- Custom exceptions for better error handling
- CLI improvements with better argument handling
- Direct WKT string input support
- Automated testing with pytest
- CI/CD pipeline
- Pre-commit hooks for code quality

### Changed
- Simplified CLI interface - no need to specify 'process' command for basic operations
- Made process command the default operation
- Refactored geometry operations into GeometryProcessor class
- Refactored H3 operations into H3Processor class
- Improved error messages and logging
- Updated CLI interface for better usability
- Consolidated file handling utilities

### Fixed
- Improved error handling in file operations
- Better CRS handling and validation
- Fixed geometry validation issues
- Improved H3 resolution validation

## [0.1.0] - 2025-04-03

### Added
- Initial release
- Basic geometry operations
- Basic H3 operations
- File I/O support
- Command-line interface
- Basic documentation
