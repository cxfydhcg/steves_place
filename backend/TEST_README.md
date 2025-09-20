# Steve's Place Backend Testing Guide

This document provides comprehensive information about the testing framework for Steve's Place backend application.

## Overview

The testing framework is built using pytest and includes comprehensive test coverage for:
- **Models**: All data models and their functionality
- **Routes**: API endpoints and their behavior
- **Integration**: End-to-end testing scenarios
- **Mocking**: Isolated unit tests with mock dependencies

## Test Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared test fixtures
│   ├── run_tests.py             # Simple test runner script
│   ├── models/
│   │   ├── __init__.py
│   │   ├── test_category.py     # Category enum tests
│   │   ├── test_order.py        # Order model tests
│   │   ├── test_hotdog.py       # Hotdog model tests
│   │   ├── test_sandwich.py     # Sandwich model tests
│   │   ├── test_eggsandwich.py  # EggSandwich model tests
│   │   ├── test_drink.py        # Drink model tests
│   │   ├── test_combo.py        # Combo model tests
│   │   ├── test_salad.py        # Salad model tests
│   │   ├── test_side.py         # Side model tests
│   │   └── test_storeclosedatetable.py # Store close date tests
│   └── routes/
│       ├── __init__.py
│       ├── test_checkout_api.py    # Checkout API tests
│       ├── test_close_store_api.py # Store closing API tests
│       └── test_get_info_api.py    # Info retrieval API tests
├── test_requirements.txt        # Testing dependencies
└── TEST_README.md              # This file
```

## Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
python -m pip install -r test_requirements.txt
```

### 2. Run All Tests with Coverage

```bash
# Using the test runner script (from tests directory)
cd tests
python run_tests.py

# Using pytest directly
pytest . --cov=../ --cov-report=term-missing --cov-report=html:../htmlcov -v
```

## Test Runner

The `run_tests.py` script is a simple test runner that:
- Runs all tests in the test suite
- Generates coverage reports (terminal and HTML)
- Shows missing lines in coverage
- Provides verbose output
## Coverage Reports

After running tests, coverage reports are generated in two formats:
- **Terminal**: Shows coverage percentage and missing lines
- **HTML**: Detailed report in `../htmlcov/index.html`

## Running Specific Tests

For more granular test execution, use pytest directly:

```bash
# Run a specific test file
pytest models/test_category.py -v

# Run a specific test function
pytest models/test_category.py::TestCategory::test_category_values -v

# Run tests matching a pattern
pytest -k "test_hotdog" -v

# Run only model tests
pytest models/ -v

# Run only route tests
pytest routes/ -v
```

## Test Configuration

### conftest.py
Provides shared test fixtures:
- `app`: Flask application instance for testing
- `client`: Test client for API requests
- Database setup and teardown
- Mock data fixtures

## Writing Tests

### Test Structure

Each test file should follow this structure:

```python
import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestYourModel:
    """Test cases for YourModel."""
    
    @pytest.fixture
    def mock_data(self):
        """Provide mock data for testing."""
        return {'key': 'value'}
    
    def test_functionality(self, mock_data):
        """Test specific functionality."""
        # Test implementation
        assert True
```

### Mocking

Use mocks for external dependencies:

```python
from unittest.mock import Mock, patch

@patch('module.external_service')
def test_with_mock(mock_service):
    mock_service.return_value = {'status': 'success'}
    # Test implementation
```

## Docker Integration

The Docker container automatically runs tests with coverage on startup:

```bash
# Build and run the container
docker-compose up --build
```

The container will:
1. Install all dependencies
2. Run the complete test suite with coverage
3. Start the Flask application (if tests pass)

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the backend directory is in your Python path
2. **Database Errors**: Tests use SQLite in-memory database by default
3. **Missing Dependencies**: Install with `pip install -r test_requirements.txt`
4. **Permission Errors**: Ensure write permissions for test artifacts

### Debug Mode

For debugging tests:

```bash
# Run with verbose output and stop on first failure
pytest -v -x

# Run with Python debugger
pytest --pdb

# Run specific test with maximum verbosity
pytest -vvv models/test_category.py::TestCategory::test_category_values
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Services**: Don't rely on external APIs in tests
3. **Use Fixtures**: Share common test data using pytest fixtures
4. **Descriptive Names**: Use clear, descriptive test function names
5. **Test Edge Cases**: Include tests for error conditions and edge cases
6. **Keep Tests Fast**: Use mocks to avoid slow operations
7. **Regular Testing**: Run tests frequently during development

## Coverage Goals

- **Overall Coverage**: Aim for 80%+ code coverage
- **Critical Paths**: 100% coverage for payment and order processing
- **Models**: 90%+ coverage for all data models
- **APIs**: 85%+ coverage for all API endpoints

---

**Note**: This simplified testing framework focuses on running all tests with comprehensive coverage reporting.