#!/bin/bash
# this_file: scripts/build-and-test.sh
# Build, test, and release script for twat-speech

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    if ! command_exists hatch; then
        print_warning "Hatch not found. Installing..."
        pip install hatch
    fi
    
    if ! command_exists uv; then
        print_warning "uv not found. Installing for faster builds..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    print_success "Prerequisites check completed"
}

# Clean previous builds
clean_build() {
    print_status "Cleaning previous builds..."
    rm -rf dist/ build/ *.egg-info/
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    print_success "Clean completed"
}

# Run linting and formatting
run_linting() {
    print_status "Running linting and formatting..."
    
    # Run ruff formatting
    if command_exists uv; then
        uv run ruff format src tests
        uv run ruff check --fix src tests
    else
        hatch run lint:fmt
    fi
    
    print_success "Linting completed"
}

# Run type checking
run_type_checking() {
    print_status "Running type checking..."
    
    if command_exists uv; then
        uv run mypy src tests
    else
        hatch run lint:typing
    fi
    
    print_success "Type checking completed"
}

# Run tests with coverage
run_tests() {
    print_status "Running tests with coverage..."
    
    if command_exists uv; then
        uv run pytest --cov-report=term-missing --cov-report=html --cov-config=pyproject.toml --cov=src/twat_speech --cov=tests tests/
    else
        hatch run test-cov
    fi
    
    print_success "Tests completed"
}

# Build the package
build_package() {
    print_status "Building package..."
    
    if command_exists uv; then
        uv run python -m build --outdir dist
    else
        hatch build
    fi
    
    print_success "Package built successfully"
    print_status "Built files:"
    ls -la dist/
}

# Verify the built package
verify_package() {
    print_status "Verifying package..."
    
    # Check if wheel and source distribution exist
    if [ ! -f dist/*.whl ] || [ ! -f dist/*.tar.gz ]; then
        print_error "Missing distribution files"
        exit 1
    fi
    
    # Test installation in a temporary environment
    if command_exists uv; then
        print_status "Testing package installation..."
        uv run pip install dist/*.whl --force-reinstall
        uv run python -c "import twat_speech; print(f'Package version: {twat_speech.__version__}')"
        uv run twat-speech --help 2>/dev/null || uv run python -m twat_speech.twat_speech
    fi
    
    print_success "Package verification completed"
}

# Main execution
main() {
    print_status "Starting build-and-test workflow..."
    
    # Parse command line arguments
    SKIP_TESTS=false
    SKIP_LINT=false
    SKIP_BUILD=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --skip-lint)
                SKIP_LINT=true
                shift
                ;;
            --skip-build)
                SKIP_BUILD=true
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --skip-tests    Skip running tests"
                echo "  --skip-lint     Skip linting and formatting"
                echo "  --skip-build    Skip building the package"
                echo "  --help          Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Execute workflow steps
    check_prerequisites
    clean_build
    
    if [ "$SKIP_LINT" = false ]; then
        run_linting
        run_type_checking
    fi
    
    if [ "$SKIP_TESTS" = false ]; then
        run_tests
    fi
    
    if [ "$SKIP_BUILD" = false ]; then
        build_package
        verify_package
    fi
    
    print_success "Build-and-test workflow completed successfully!"
    print_status "You can now publish the package with: hatch publish"
}

# Execute main function
main "$@"