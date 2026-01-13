#!/bin/bash
"""
Shell wrapper for Dream.OS comprehensive smoke test suite.
Provides easy execution and colored output for CI/CD pipelines.

Usage:
  ./scripts/health/smoke.sh           # Run all tests
  ./scripts/health/smoke.sh --quiet   # Run with minimal output
  ./scripts/health/smoke.sh --help    # Show help

Exit codes:
  0 = All systems healthy
  1 = One or more systems failed
  2 = Critical system failure (unable to test)

Author: Agent-3 (Infrastructure & DevOps Recovery Specialist)
Date: 2026-01-09
"""

set -e  # Exit on error

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
QUIET=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --quiet|-q)
            QUIET=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Dream.OS Smoke Test Suite"
            echo "========================"
            echo ""
            echo "Usage:"
            echo "  $0                    # Run all tests with colored output"
            echo "  $0 --quiet           # Run with minimal output (CI/CD friendly)"
            echo "  $0 --verbose         # Run with detailed output"
            echo "  $0 --help            # Show this help"
            echo ""
            echo "Exit codes:"
            echo "  0 = All systems healthy"
            echo "  1 = One or more systems failed"
            echo "  2 = Critical system failure"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to print colored output
print_status() {
    local level=$1
    local message=$2

    if [ "$QUIET" = true ]; then
        return
    fi

    case $level in
        "info")
            echo -e "${BLUE}ℹ${NC}  $message"
            ;;
        "success")
            echo -e "${GREEN}✓${NC}  $message"
            ;;
        "warning")
            echo -e "${YELLOW}⚠${NC}  $message"
            ;;
        "error")
            echo -e "${RED}✗${NC}  $message"
            ;;
        *)
            echo "$message"
            ;;
    esac
}

# Function to print section headers
print_header() {
    local title=$1
    if [ "$QUIET" = false ]; then
        echo ""
        echo -e "${BLUE}═══ $title ═══${NC}"
    fi
}

# Pre-flight checks
print_header "Pre-flight Checks"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_status "error" "Python 3 is not available"
    exit 2
fi
print_status "success" "Python 3 found"

# Check if we're in the right directory
if [ ! -f "scripts/health/smoke.py" ]; then
    print_status "error" "smoke.py not found in scripts/health/"
    print_status "info" "Please run this script from the project root directory"
    exit 2
fi
print_status "success" "Smoke test script found"

# Check for .env file
if [ -f ".env" ]; then
    print_status "success" "Environment file (.env) found"
else
    print_status "warning" "No .env file found - using system environment variables"
fi

# Run the smoke tests
print_header "Running Smoke Tests"

if [ "$QUIET" = true ]; then
    # Quiet mode - just run and capture exit code
    if python3 scripts/health/smoke.py > /dev/null 2>&1; then
        echo "✓ All systems healthy"
        exit 0
    else
        exit_code=$?
        echo "✗ Smoke tests failed (exit code: $exit_code)"
        exit $exit_code
    fi
else
    # Normal mode - show output
    cd "$PROJECT_ROOT"
    python3 scripts/health/smoke.py
    exit_code=$?
fi

# Post-run analysis
print_header "Test Results"

case $exit_code in
    0)
        print_status "success" "🎉 ALL SYSTEMS HEALTHY - READY FOR PRODUCTION"
        ;;
    1)
        print_status "error" "💥 SYSTEMS WITH FAILURES - RECOVERY NEEDED"
        ;;
    2)
        print_status "error" "💥 CRITICAL SYSTEM FAILURE - UNABLE TO TEST"
        ;;
    *)
        print_status "error" "Unexpected exit code: $exit_code"
        ;;
esac

exit $exit_code