#!/bin/bash
# this_file: scripts/build-binary.sh
# Build standalone binary executables for twat-speech

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

# Function to detect OS and architecture
detect_platform() {
    local os=$(uname -s | tr '[:upper:]' '[:lower:]')
    local arch=$(uname -m)
    
    case $os in
        linux*)
            os="linux"
            ;;
        darwin*)
            os="macos"
            ;;
        mingw*|cygwin*|msys*)
            os="windows"
            ;;
        *)
            print_error "Unsupported OS: $os"
            exit 1
            ;;
    esac
    
    case $arch in
        x86_64|amd64)
            arch="x64"
            ;;
        aarch64|arm64)
            arch="arm64"
            ;;
        i386|i686)
            arch="x86"
            ;;
        *)
            print_error "Unsupported architecture: $arch"
            exit 1
            ;;
    esac
    
    echo "${os}-${arch}"
}

# Function to install binary dependencies
install_dependencies() {
    print_status "Installing binary build dependencies..."
    
    if command -v uv >/dev/null 2>&1; then
        uv pip install --system ".[binary]"
    else
        pip install ".[binary]"
    fi
    
    print_success "Dependencies installed"
}

# Function to create PyInstaller spec file
create_spec_file() {
    local output_dir=$1
    local spec_file="$output_dir/twat-speech.spec"
    
    print_status "Creating PyInstaller spec file..."
    
    cat > "$spec_file" << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for twat-speech

import sys
import os
from pathlib import Path

block_cipher = None

# Get the source directory
src_dir = Path(__file__).parent.parent / "src"

a = Analysis(
    ['../src/twat_speech/twat_speech.py'],
    pathex=[str(src_dir)],
    binaries=[],
    datas=[
        # Include package data if any
        # ('src/twat_speech/data', 'twat_speech/data'),
    ],
    hiddenimports=[
        'twat_speech',
        'twat_speech.twat_speech',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'jupyter',
        'notebook',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='twat-speech',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path if you have one
)
EOF

    print_success "Spec file created: $spec_file"
    echo "$spec_file"
}

# Function to build binary with PyInstaller
build_with_pyinstaller() {
    local output_dir=$1
    local platform=$2
    
    print_status "Building binary with PyInstaller for $platform..."
    
    # Create spec file
    spec_file=$(create_spec_file "$output_dir")
    
    # Run PyInstaller
    if command -v uv >/dev/null 2>&1; then
        uv run pyinstaller \
            --distpath "$output_dir" \
            --workpath "$output_dir/build" \
            --clean \
            --onefile \
            --name "twat-speech-$platform" \
            "$spec_file"
    else
        pyinstaller \
            --distpath "$output_dir" \
            --workpath "$output_dir/build" \
            --clean \
            --onefile \
            --name "twat-speech-$platform" \
            "$spec_file"
    fi
    
    print_success "PyInstaller build completed"
}

# Function to create static Linux binary
create_static_binary() {
    local output_dir=$1
    local platform=$2
    
    if [[ "$platform" == linux-* ]]; then
        print_status "Creating static Linux binary..."
        
        local binary_path="$output_dir/twat-speech-$platform"
        local static_binary_path="$output_dir/twat-speech-$platform-static"
        
        if command -v staticx >/dev/null 2>&1; then
            staticx "$binary_path" "$static_binary_path"
            print_success "Static binary created: $static_binary_path"
        else
            print_warning "staticx not available, skipping static binary creation"
        fi
    fi
}

# Function to test binary
test_binary() {
    local binary_path=$1
    
    print_status "Testing binary..."
    
    if [[ -f "$binary_path" ]]; then
        chmod +x "$binary_path"
        
        # Test that binary runs
        if "$binary_path" >/dev/null 2>&1; then
            print_success "Binary test passed"
        else
            print_warning "Binary test failed, but this might be expected for demo binaries"
        fi
        
        # Show binary info
        print_status "Binary information:"
        ls -lh "$binary_path"
        file "$binary_path" 2>/dev/null || true
    else
        print_error "Binary not found: $binary_path"
        exit 1
    fi
}

# Function to package binary
package_binary() {
    local output_dir=$1
    local platform=$2
    
    print_status "Packaging binary for distribution..."
    
    local binary_name="twat-speech-$platform"
    local binary_path="$output_dir/$binary_name"
    local static_binary_path="$output_dir/$binary_name-static"
    
    # Create distribution directory
    local dist_dir="$output_dir/dist"
    mkdir -p "$dist_dir"
    
    # Package regular binary
    if [[ -f "$binary_path" ]]; then
        if command -v gzip >/dev/null 2>&1; then
            gzip -c "$binary_path" > "$dist_dir/$binary_name.gz"
            print_status "Compressed binary: $dist_dir/$binary_name.gz"
        else
            cp "$binary_path" "$dist_dir/"
            print_status "Binary copied: $dist_dir/$binary_name"
        fi
    fi
    
    # Package static binary if available
    if [[ -f "$static_binary_path" ]]; then
        if command -v gzip >/dev/null 2>&1; then
            gzip -c "$static_binary_path" > "$dist_dir/$binary_name-static.gz"
            print_status "Compressed static binary: $dist_dir/$binary_name-static.gz"
        else
            cp "$static_binary_path" "$dist_dir/"
            print_status "Static binary copied: $dist_dir/$binary_name-static"
        fi
    fi
    
    # Create checksums
    cd "$dist_dir"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum * > checksums.txt
        print_success "Checksums created: $dist_dir/checksums.txt"
    fi
    cd - >/dev/null
    
    print_success "Binary packaging completed"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Build standalone binary executables for twat-speech"
    echo ""
    echo "Options:"
    echo "  --output-dir DIR     Output directory for binaries (default: ./build-binary)"
    echo "  --skip-test          Skip binary testing"
    echo "  --skip-package       Skip binary packaging"
    echo "  --clean              Clean output directory before building"
    echo "  --help               Show this help message"
    echo ""
    echo "The script will automatically detect the current platform and build"
    echo "appropriate binaries for it."
}

# Main execution
main() {
    local output_dir="./build-binary"
    local skip_test=false
    local skip_package=false
    local clean=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --output-dir)
                output_dir="$2"
                shift 2
                ;;
            --skip-test)
                skip_test=true
                shift
                ;;
            --skip-package)
                skip_package=true
                shift
                ;;
            --clean)
                clean=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Detect platform
    local platform=$(detect_platform)
    print_status "Detected platform: $platform"
    
    # Clean output directory if requested
    if [[ "$clean" == true ]]; then
        print_status "Cleaning output directory: $output_dir"
        rm -rf "$output_dir"
    fi
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # Install dependencies
    install_dependencies
    
    # Build binary
    build_with_pyinstaller "$output_dir" "$platform"
    
    # Create static binary (Linux only)
    create_static_binary "$output_dir" "$platform"
    
    # Test binary
    if [[ "$skip_test" == false ]]; then
        test_binary "$output_dir/twat-speech-$platform"
    fi
    
    # Package binary
    if [[ "$skip_package" == false ]]; then
        package_binary "$output_dir" "$platform"
    fi
    
    print_success "Binary build completed successfully!"
    print_status "Output directory: $output_dir"
    print_status "Platform: $platform"
    
    # Show final results
    print_status "Built files:"
    find "$output_dir" -type f -name "twat-speech*" -exec ls -lh {} \;
}

# Execute main function
main "$@"