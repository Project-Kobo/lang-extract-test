#!/bin/bash

# LangExtract Test Setup Script
# Automated setup for LangExtract with conda environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
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

# Function to detect conda installation
find_conda() {
    # Check if conda is in PATH
    if command -v conda &> /dev/null; then
        echo "conda"
        return 0
    fi
    
    # Common conda installation paths
    local conda_paths=(
        "/opt/homebrew/bin/conda"
        "/opt/homebrew/Caskroom/miniconda/base/bin/conda"
        "/usr/local/bin/conda"
        "/usr/local/miniconda3/bin/conda"
        "/home/$USER/miniconda3/bin/conda"
        "/home/$USER/anaconda3/bin/conda"
        "/anaconda3/bin/conda"
        "/miniconda3/bin/conda"
    )
    
    for path in "${conda_paths[@]}"; do
        if [ -f "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    
    return 1
}

# Function to check Python version
check_python_version() {
    local python_cmd="$1"
    local version=$($python_cmd --version 2>&1 | awk '{print $2}')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -eq 3 ] && [ "$minor" -ge 11 ]; then
        return 0
    else
        return 1
    fi
}

# Main setup function
main() {
    echo "🚀 LangExtract Test Setup"
    echo "=========================="
    echo
    
    # Step 1: Find conda
    print_status "Looking for conda installation..."
    
    if CONDA_CMD=$(find_conda); then
        print_success "Found conda at: $CONDA_CMD"
    else
        print_error "Conda not found. Please install miniconda or anaconda first."
        echo "📥 Download from: https://docs.conda.io/en/latest/miniconda.html"
        exit 1
    fi
    
    # Step 2: Initialize conda if needed
    if ! command -v conda &> /dev/null; then
        print_status "Initializing conda for current shell..."
        eval "$($CONDA_CMD shell.bash hook)"
    fi
    
    # Step 3: Check if environment already exists
    if $CONDA_CMD env list | grep -q "langextract"; then
        print_warning "Environment 'langextract' already exists"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Removing existing environment..."
            $CONDA_CMD remove -n langextract --all -y
        else
            print_status "Using existing environment..."
        fi
    fi
    
    # Step 4: Create conda environment
    if ! $CONDA_CMD env list | grep -q "langextract"; then
        print_status "Creating conda environment with Python 3.11..."
        $CONDA_CMD create -n langextract python=3.11 -y
    fi
    
    # Step 5: Activate environment and get Python path
    print_status "Activating environment and checking Python version..."
    
    # Get the environment path
    ENV_PATH=$($CONDA_CMD env list | grep langextract | awk '{print $2}')
    PYTHON_CMD="$ENV_PATH/bin/python"
    PIP_CMD="$ENV_PATH/bin/pip"
    
    if [ ! -f "$PYTHON_CMD" ]; then
        print_error "Python not found in langextract environment"
        exit 1
    fi
    
    if check_python_version "$PYTHON_CMD"; then
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
        print_success "Python version OK: $PYTHON_VERSION"
    else
        print_error "Python 3.11+ required"
        exit 1
    fi
    
    # Step 6: Clone LangExtract if not exists
    if [ ! -d "langextract" ]; then
        print_status "Cloning LangExtract repository..."
        git clone https://github.com/google/langextract.git
    else
        print_status "LangExtract repository already exists"
    fi
    
    # Step 7: Install LangExtract
    print_status "Installing LangExtract with development dependencies..."
    cd langextract
    $PIP_CMD install -e ".[dev]"
    cd ..
    
    # Step 8: Verify installation
    print_status "Verifying installation..."
    if $PYTHON_CMD -c "import langextract as lx; print('✅ LangExtract imported successfully')" 2>/dev/null; then
        print_success "LangExtract installation verified"
    else
        print_error "LangExtract installation failed"
        exit 1
    fi
    
    # Step 9: Check for API key
    print_status "Checking API key configuration..."
    if [ -f ".env" ]; then
        if grep -q "LANGEXTRACT_API_KEY=" .env && ! grep -q "your-api-key-here" .env; then
            print_success "API key found in .env file"
        else
            print_warning "API key not properly configured in .env file"
            echo "💡 Edit .env file and add your Gemini API key"
        fi
    else
        print_warning ".env file not found"
        echo "💡 Copy .env.example to .env and add your Gemini API key"
        echo "📝 Get your API key from: https://aistudio.google.com/app/apikey"
    fi
    
    # Step 10: Create outputs directory
    print_status "Creating outputs directory..."
    mkdir -p outputs
    
    echo
    print_success "Setup completed successfully! 🎉"
    echo
    echo "Next steps:"
    echo "1. Activate the environment: conda activate langextract"
    echo "2. Configure your API key in .env file (if not done already)"
    echo "3. Run validation: python validate_setup.py"
    echo "4. Try examples: python examples/basic_example.py"
    echo
    echo "💡 Run 'python validate_setup.py' to test your setup"
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi