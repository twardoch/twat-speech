#!/bin/bash
# this_file: scripts/release.sh
# Release script for twat-speech - creates git tags and triggers releases

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

# Function to validate semantic version
validate_semver() {
    local version=$1
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9-]+)?(\+[a-zA-Z0-9-]+)?$ ]]; then
        print_error "Invalid semantic version format: $version"
        print_error "Expected format: X.Y.Z or X.Y.Z-prerelease or X.Y.Z+metadata"
        exit 1
    fi
}

# Function to check if tag already exists
check_tag_exists() {
    local tag=$1
    if git tag -l | grep -q "^$tag$"; then
        print_error "Tag $tag already exists"
        exit 1
    fi
}

# Function to check git status
check_git_status() {
    if [[ -n $(git status --porcelain) ]]; then
        print_error "Working directory is not clean. Please commit or stash changes."
        git status --short
        exit 1
    fi
    
    if [[ $(git rev-parse --abbrev-ref HEAD) != "main" ]]; then
        print_warning "You are not on the main branch. Current branch: $(git rev-parse --abbrev-ref HEAD)"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Function to run pre-release checks
run_pre_release_checks() {
    print_status "Running pre-release checks..."
    
    # Run full test suite
    if [[ -f scripts/build-and-test.sh ]]; then
        ./scripts/build-and-test.sh
    else
        print_warning "build-and-test.sh not found, running basic tests"
        if command -v uv >/dev/null 2>&1; then
            uv run pytest tests/
        else
            hatch run test
        fi
    fi
    
    print_success "Pre-release checks completed"
}

# Function to create and push tag
create_and_push_tag() {
    local version=$1
    local tag="v$version"
    
    print_status "Creating tag $tag..."
    
    # Create annotated tag
    git tag -a "$tag" -m "Release version $version"
    
    # Push tag to remote
    print_status "Pushing tag to remote..."
    git push origin "$tag"
    
    print_success "Tag $tag created and pushed successfully"
}

# Function to show current version
show_current_version() {
    print_status "Detecting current version..."
    
    if command -v uv >/dev/null 2>&1; then
        current_version=$(uv run python -c "import twat_speech; print(twat_speech.__version__)" 2>/dev/null || echo "unknown")
    else
        current_version=$(hatch run python -c "import twat_speech; print(twat_speech.__version__)" 2>/dev/null || echo "unknown")
    fi
    
    print_status "Current version: $current_version"
    
    # Show recent tags
    print_status "Recent tags:"
    git tag -l "v*" | sort -V | tail -5 || echo "No tags found"
}

# Function to increment version
increment_version() {
    local current_version=$1
    local increment_type=$2
    
    if [[ "$current_version" == "unknown" ]]; then
        print_error "Cannot detect current version"
        exit 1
    fi
    
    # Parse version components
    if [[ $current_version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
        local major=${BASH_REMATCH[1]}
        local minor=${BASH_REMATCH[2]}
        local patch=${BASH_REMATCH[3]}
        
        case $increment_type in
            major)
                echo "$((major + 1)).0.0"
                ;;
            minor)
                echo "$major.$((minor + 1)).0"
                ;;
            patch)
                echo "$major.$minor.$((patch + 1))"
                ;;
            *)
                print_error "Invalid increment type: $increment_type"
                exit 1
                ;;
        esac
    else
        print_error "Cannot parse current version: $current_version"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS] [VERSION]"
    echo ""
    echo "Create a new release by tagging the current commit"
    echo ""
    echo "Arguments:"
    echo "  VERSION              Semantic version number (e.g., 1.2.3)"
    echo ""
    echo "Options:"
    echo "  --major              Increment major version"
    echo "  --minor              Increment minor version"
    echo "  --patch              Increment patch version"
    echo "  --current            Show current version and recent tags"
    echo "  --skip-checks        Skip pre-release checks"
    echo "  --dry-run            Show what would be done without executing"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 1.2.3             Release version 1.2.3"
    echo "  $0 --patch           Increment patch version and release"
    echo "  $0 --minor           Increment minor version and release"
    echo "  $0 --major           Increment major version and release"
    echo "  $0 --current         Show current version"
}

# Main execution
main() {
    local version=""
    local increment_type=""
    local skip_checks=false
    local dry_run=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --major)
                increment_type="major"
                shift
                ;;
            --minor)
                increment_type="minor"
                shift
                ;;
            --patch)
                increment_type="patch"
                shift
                ;;
            --current)
                show_current_version
                exit 0
                ;;
            --skip-checks)
                skip_checks=true
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [[ -z "$version" ]]; then
                    version=$1
                else
                    print_error "Multiple versions specified"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Show current version first
    show_current_version
    
    # Handle version increment
    if [[ -n "$increment_type" ]]; then
        if [[ -n "$version" ]]; then
            print_error "Cannot specify both version and increment type"
            exit 1
        fi
        
        current_version=$(uv run python -c "import twat_speech; print(twat_speech.__version__)" 2>/dev/null || echo "unknown")
        version=$(increment_version "$current_version" "$increment_type")
        print_status "Auto-incremented version: $version"
    fi
    
    # Check if version is provided
    if [[ -z "$version" ]]; then
        print_error "Version must be specified"
        show_help
        exit 1
    fi
    
    # Validate version format
    validate_semver "$version"
    
    # Check if tag already exists
    check_tag_exists "v$version"
    
    if [[ "$dry_run" == true ]]; then
        print_status "DRY RUN: Would create and push tag v$version"
        exit 0
    fi
    
    # Check git status
    check_git_status
    
    # Run pre-release checks
    if [[ "$skip_checks" == false ]]; then
        run_pre_release_checks
    fi
    
    # Create and push tag
    create_and_push_tag "$version"
    
    print_success "Release $version completed successfully!"
    print_status "GitHub Actions will now build and publish the release."
    print_status "Monitor the progress at: https://github.com/twardoch/twat-speech/actions"
}

# Execute main function
main "$@"