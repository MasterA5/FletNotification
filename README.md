# Flet Notification

A Flet Extension that demonstrates how to manage and send notifications on Android Windows and Linux devices (for now) . This project provides a simple interface for requesting notification permissions and sending them using Android's native APIs, with the intention of adding more platforms to the project in the future.

## [Credits To: @ITAkademi](https://www.youtube.com/@ITAkademi)

## Supported On

| Platform | Status |
|----------|--------|
| Android  | ✅     |
| iOS      | ⏳     Can't test|
| Windows  | ✅     |
| macOS    | ⏳     Can't test|
| Linux    | ✅     |

## Features

- **Permission Management**: Check and request notification permissions
- **Notification Sending**: Send custom notifications with title and text
- **Android Integration**: Uses native Android NotificationManager via JNI
- **User-Friendly Interface**: Simple GUI built with Flet framework

## Requirements

- Python 3.9 or higher
- Flet framework
- Android device or emulator for testing
- Required permissions configured in `pyproject.toml`
- Support for android 16 (API 36)

## Installation

```bash
git clone <repository-url>
cd FletNotification
```

## Usage

### Running the Application

```bash
flet run
```

## Build app
```bash
flet build apk
```

## ⚙️ Pyproject Config
```toml
[tool.flet]

# Permissions For The App
permissions = [
  "notification",
  "access_notification_policy",
  "post_notifications",
  "wake_lock",
  "foreground_service"
]

[tool.flet.android.permissions]
"android.permission.ACCESS_NOTIFICATION" = true
"android.permission.POST_NOTIFICATIONS" = true
"android.permission.WAKE_LOCK" = true
"android.permission.FOREGROUND_SERVICE" = true
"android.permission.INTERNET" = true
"android.permission.RECEIVE_BOOT_COMPLETED" = true
```

### ⚠️ Important
For Android SDK > 35, you must manually add the permission to ```AndroidManifest.xml``` in your build project or you can use my custom build template 

## Example 1
Add Permission Manually in ```AndroidManifest.xml```
```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

## Example 2
Use My Custom Template For Build

# 📄 Toml
```toml
[tool.flet.template]
path = "gh:MasterA5/flet-build-template" # --template
ref = "0.28.3" # --template-ref
```

# 💻 Terminal
```bash
flet build apk --template "gh:MasterA5/flet-build-template" --template-ref "0.28.3"
```

---

### Application Interface

The app provides the following functionality:

1. **Check Notification Permission**: Verifies if the app has notification permissions
2. **Request Notification Permission**: Requests notification permissions from the user
3. **Send Notification**: Sends a test notification (only enabled when permissions are granted)

## Project Structure

```
FletNotification/
├── src/
│   ├── main.py                    # Main application entry point
│   └── flet_post_notification.py  # Notification handling class
├── pyproject.toml                 # Project configuration and dependencies
└── README.md                     # This file
└── .gitignore                    # Git ignore file
```

## Key Components

### FletNotification Class

Located in `src/flet_post_notification.py`, this class handles the native Android notification functionality:

- Creates notification channels
- Builds and displays notifications
- Uses JNI (Java Native Interface) via pyjnius to access Android APIs

### Main Application

Located in `src/main.py`, this provides:

- Permission checking and requesting
- User interface with buttons and status indicators
- Integration with Flet's permission handler

## Dependencies

- `flet==0.28.3`: Main UI framework
- `pyjnius`: Python-Java bridge for Android integration
- `flet-permission-handler`: Flet plugin for handling permissions

## Android Permissions

The app requests the following permissions (configured in `pyproject.toml`):

- `notification`: Basic notification access
- `access_notification_policy`: Access to notification policies
- `post_notifications`: Ability to post notifications
- `wake_lock`: Keep device awake for notifications
- `foreground_service`: Run as foreground service

## Future Improvements

- Add support for scheduled notifications
- Implement notification groups and categories
- Add support for notification actions and buttons
- Improve notification styling and customization
- ✅ Add support for more platform-specific features (iOS, Windows, etc.)

## Notes

- Notification functionality requires proper permissions to be granted by the user
- The app uses native Android APIs for reliable notification delivery

## Contributing

This project is open for contributions. Feel free to submit issues or pull requests.