# Changelog

## [0.1.1] - 2025-04-10

### Added
- New inspect mode when only INPUT is provided
  - `--head N` to show first N rows in WKT format
  - `--tail N` to show last N rows in WKT format
  - `--crs` to show CRS information
- Operation order preservation: operations are now applied in the exact order they appear in command line
- Logging system improvements:
  - Switched to loguru for better logging control
  - Added `--log-level` flag with DEBUG, INFO, WARNING, ERROR options
  - Simplified INFO output format
  - Detailed DEBUG output with timestamps and file info

### Changed
- Restructured project:
  - Renamed `file_io` folder to `io`
  - Created `operators` folder for geometry and H3 operations
- Version now reads directly from pyproject.toml
- Improved geometry display in head/tail output

### Fixed
- Fixed warning about geometry column modification in head/tail commands
- Reduced log verbosity for file operations

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-04-10

### Note

Version bump only. No functional changes from 0.1.0.

## [0.1.0] - 2025-04-07

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
- Initial release
- Basic geometry operations
- Basic H3 operations
- File I/O support
- Command-line interface
- Basic documentation

### Changed
- Switched from `setup.py` to Poetry with `pyproject.toml` for dependency and packaging management
- Simplified CLI interface - no need to specify 'process' command for basic operations
- Made `process` command the default operation
- Refactored geometry operations into `GeometryProcessor` class
- Refactored H3 operations into `H3Processor` class
- Improved error messages and logging
- Updated CLI interface for better usability
- Consolidated file handling utilities

### Fixed
- Improved error handling in file operations
- Better CRS handling and validation
- Fixed geometry validation issues
- Improved H3 resolution validation
