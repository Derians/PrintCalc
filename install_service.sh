#!/bin/bash

# install_service.sh — universal service installation script

PROJECT_DIR=$(cd -- "$(dirname "$0")" && pwd)
UNAME=$(uname -s)

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    local version=$($1 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 7 ]); then
        echo "Python version $version is not supported. Please install Python 3.7 or higher."
        exit 1
    fi
}

if [[ "$UNAME" == "Linux" ]]; then
    echo "Linux environment detected. Installing systemd service..."

    # Check for Python 3
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        if python -c 'import sys; exit(0 if sys.version_info.major == 3 else 1)' >/dev/null 2>&1; then
            PYTHON_CMD="python"
        else
            echo "Python 3 not found. Please install Python 3.7 or higher."
            exit 1
        fi
    else
        echo "Python 3 not found. Please install Python 3.7 or higher."
        exit 1
    fi

    # Check Python version
    check_python_version "$PYTHON_CMD"

    # Check for pip
    if ! command_exists pip3 && ! "$PYTHON_CMD" -m pip --version >/dev/null 2>&1; then
        echo "pip not found. Please install pip for Python 3."
        exit 1
    fi

    SERVICE_NAME="printcalc.service"
    TARGET_PATH="/etc/systemd/system"
    USER_NAME=$(whoami)
    PYTHON_BIN="$PROJECT_DIR/venv/bin/python"

    # Check and create virtual environment
    if [ ! -f "$PYTHON_BIN" ]; then
        echo "Virtual environment not found. Creating..."
        "$PYTHON_CMD" -m venv "$PROJECT_DIR/venv"
        
        echo "Installing dependencies from requirements.txt..."
        "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"
    fi

    # Substitute paths in template
    if [ ! -f "$PROJECT_DIR/$SERVICE_NAME" ]; then
        echo "$SERVICE_NAME not found"
        exit 1
    fi

    TMP_FILE="/tmp/$SERVICE_NAME"
    sed "s|REPLACE_ME_USER|$USER_NAME|g; s|REPLACE_ME_DIR|$PROJECT_DIR|g" "$PROJECT_DIR/$SERVICE_NAME" > "$TMP_FILE"
    sudo cp "$TMP_FILE" "$TARGET_PATH/$SERVICE_NAME"
    sudo chmod 644 "$TARGET_PATH/$SERVICE_NAME"

    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl restart "$SERVICE_NAME"

    echo "Service '$SERVICE_NAME' installed and started."
    sudo systemctl status "$SERVICE_NAME" --no-pager

elif [[ "$UNAME" == MINGW* || "$UNAME" == CYGWIN* || "$UNAME" == MSYS* || "$OS" == "Windows_NT" ]]; then
    echo "Windows detected. Switching to .bat installation..."

    echo "Creating PrintCalcService via sc.exe"
    set SERVICE_NAME=PrintCalcService

    powershell.exe -Command "Start-Process -Verb runAs cmd.exe '/c cd /d %cd% && install_service_windows.bat'"

else
    echo "Unknown OS: $UNAME. Only Linux and Windows are supported."
    exit 1
fi