# YouTube PiP Controller

A Python desktop application that automatically enables Picture-in-Picture mode for YouTube videos in Google Chrome. This tool provides a modern, user-friendly interface with system tray integration for seamless control of YouTube's PiP feature.

## Features

- Automatic detection of active YouTube videos in Chrome
- One-click Picture-in-Picture activation
- System tray integration for background operation
- Modern, sleek user interface with semi-transparent design
- Real-time status monitoring and logging
- Minimizes to system tray for unobtrusive operation

## Requirements

- Windows operating system
- Python 3.6 or higher
- Google Chrome browser
- YouTube video must be playing in Chrome

### Python Dependencies

```
pyautogui
PyQt5
pywin32
psutil
ctypes
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/youtube-pip-controller.git
cd youtube-pip-controller
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure you have the following directory structure:

```
youtube-pip-controller/
│
├── pip-controller.py
├── icons/
│   └── tray_icon.png
└── fonts/
    └── Poppins-Regular.ttf
```

## Usage

1. Run the application:

```bash
python pip-controller.py
```

2. The application will start with a main window showing:

   - Current monitoring status
   - Start/Stop control buttons
   - Console log for monitoring activities
   - Command input field for future extensions

3. Features:
   - Click "Start" to begin monitoring for active YouTube videos
   - Click "Stop" to pause the monitoring
   - Minimize to tray to keep the application running in the background
   - Right-click the tray icon for additional options:
     - Minimize
     - Show
     - Restore
     - Quit

## How It Works

1. The application monitors active Chrome windows for YouTube video tabs
2. When a YouTube video is detected in the active window, it automatically:
   - Brings the window to focus
   - Simulates the Alt+P keyboard shortcut to activate PiP mode
   - Continues monitoring for new videos

## Customization

You can customize the application by:

- Modifying the UI colors in the `set_background_color()` method
- Changing the font by replacing the Poppins font file
- Adjusting the monitoring interval in the `monitor_youtube()` method
- Modifying the window size in the `__init__` method

## Troubleshooting

1. **PiP Not Activating:**

   - Ensure YouTube is open in Google Chrome
   - Check if the video is playing
   - Verify that Chrome has focus when the shortcut is triggered

2. **Application Not Starting:**
   - Verify all dependencies are installed
   - Check if required font and icon files are present
   - Ensure you have appropriate system permissions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to YouTube for providing the Picture-in-Picture API
- PyQt5 for the modern UI framework
- Google Fonts for the Poppins font family

## Future Enhancements

- Multi-monitor support
- Custom keyboard shortcut configuration
- Browser extension integration
- Support for additional streaming platforms
- Automated startup with Windows
- Configuration file for user preferences

## Support

For support, please open an issue in the GitHub repository or contact the maintainers directly.

Remember to update the documentation as you make changes to the application!
