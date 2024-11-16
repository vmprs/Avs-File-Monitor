---

# AVS Monitor Essentials

AVS Monitor Essentials is a lightweight Python application that monitors your Downloads and Temporary folders for file changes. Utilizing the `watchdog` library, it detects newly created, deleted, or renamed files in real-time. The tool flags any suspicious files with extensions indicative of potentially malicious content, such as `.exe`, `.dll`, `.scr`, and `.bat`.

## Features

- **Real-time Monitoring**: Detects file changes (creation, deletion, renaming) in specified directories.
- **Suspicious File Detection**: Alerts users of files with potentially harmful extensions.
- **Automatic Dependency Management**: Installs required Python packages if they are missing.
- **User-friendly GUI**: Simple interface to display file activity and alerts.

## Installation

To run this tool, simply clone the repository and execute the script. The application will automatically install any missing dependencies.

## Usage

1. Run the Python script.
2. Click "Start Monitoring" to begin monitoring the specified directories for file changes.
3. The application will display detected file activity and any suspicious file notifications.

## Note

You can happily look into the source code and modify it to your liking. #FreeEditingPrivileges

---
