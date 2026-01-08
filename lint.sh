#!/bin/sh

# Default values
ROOT_PATH=""
RUN_AUTOPEP8=false
RUN_SYNTAX_CHECK=false

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS] [ROOT_PATH]"
    echo ""
    echo "Lint Python files using pycodestyle"
    echo ""
    echo "Arguments:"
    echo "  ROOT_PATH         Directory to lint (default: current directory)"
    echo ""
    echo "Options:"
    echo "  -r, --root PATH   Set the root directory to lint"
    echo "  -a, --autopep8    Run autopep8 to automatically fix formatting issues"
    echo "  -s, --syntax      Check Python syntax using compilation (py_compile)"
    echo "  -h, --help        Show this help message and exit"
    echo ""
    echo "Examples:"
    echo "  $0                        # Lint current directory"
    echo "  $0 my_project            # Lint my_project directory"
    echo "  $0 -r my_project         # Lint my_project directory using -r option"
    echo "  $0 -a                    # Lint and auto-fix current directory"
    echo "  $0 -s                    # Lint and check syntax for current directory"
    echo "  $0 -a -s my_project      # Lint, auto-fix, and check syntax for my_project"
    echo "  $0 -r my_project -a -s   # Lint, auto-fix, and check syntax for my_project"
}

# Parse command line arguments
while [ $# -gt 0 ]; do
    case $1 in
        -r|--root)
            if [ -z "$2" ]; then
                echo "Error: --root requires a path argument"
                exit 1
            fi
            ROOT_PATH="$2"
            shift 2
            ;;
        -a|--autopep8)
            RUN_AUTOPEP8=true
            shift
            ;;
        -s|--syntax)
            RUN_SYNTAX_CHECK=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            ROOT_PATH="$1"
            shift
            ;;
    esac
done

if [ -n "$ROOT_PATH" ] && [ ! -d "$ROOT_PATH" ]; then
    echo "Directory $ROOT_PATH does not exist. Exiting."
    exit 1
fi

# Run syntax check if requested
if [ "$RUN_SYNTAX_CHECK" = true ]; then
    echo "Running Python syntax check on $ROOT_PATH..."
    SYNTAX_ERRORS=0
    
    # Find all Python files and check syntax
    find "./$ROOT_PATH" -name "*.py" -type f | while read -r file; do
        python -m py_compile "$file" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "Syntax error in: $file"
            python -m py_compile "$file"
            SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
        fi
    done
    
    if [ $SYNTAX_ERRORS -eq 0 ]; then
        echo "Python syntax check passed."
    else
        echo "Python syntax check found errors."
    fi
fi

# Run autopep8 if requested
if [ "$RUN_AUTOPEP8" = true ]; then
    echo "Running autopep8 on $ROOT_PATH..."
    autopep8 ./$ROOT_PATH --in-place --recursive
    echo "autopep8 completed."
fi

# Lint Python files
PEP8_ERROR_COUNT_CMD="pycodestyle --ignore=W293,W291,W503,W605,E501 ./$ROOT_PATH"
PEP8_ERROR_COUNT=$($PEP8_ERROR_COUNT_CMD | wc -l)

if [ "$PEP8_ERROR_COUNT" -eq 0 ]; then
    echo "PEP8 passed, no linting errors found."
else
    $PEP8_ERROR_COUNT_CMD
    echo "==============================="
    echo "PEP8 failed with $PEP8_ERROR_COUNT errors."
fi