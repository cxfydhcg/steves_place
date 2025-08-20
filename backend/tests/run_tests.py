#!/usr/bin/env python3
"""Simple test runner script for Steve's Place backend application."""

import sys
import subprocess
from pathlib import Path

# Add the backend directory to Python path
BACKEND_DIR = Path(__file__).parent.parent  # Go up one level from tests to backend
sys.path.insert(0, str(BACKEND_DIR))

def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    print("Running all tests with coverage...")
    print("=" * 50)
    
    # Run pytest with coverage
    command = [
        "python", "-m", "pytest",
        ".",  # Run tests in current directory (tests/)
        "--cov=../",  # Coverage for backend directory
        "--cov-report=term-missing",  # Show missing lines
        "-v"  # Verbose output
    ]
    
    try:
        result = subprocess.run(command, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: pytest not found. Please install test requirements.")
        return 1
    except Exception as e:
        print(f"Error running command: {e}")
        return 1


def main():
    """Main function to run all tests with coverage."""
    return run_tests_with_coverage()


if __name__ == '__main__':
    sys.exit(main())