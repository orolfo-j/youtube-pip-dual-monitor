# YouTube PiP Controller 🎬

Ever wanted to watch YouTube while working but hate manually clicking that tiny PiP button? Same here! That's why I built this little tool that automatically pops your YouTube videos into picture-in-picture mode when you need it.

## What's This All About? 🤔

This is a simple desktop app that sits in your system tray and watches for YouTube videos in Chrome. When it spots one, it'll automatically trigger PiP mode for you (using the Alt+P shortcut). No more hunting for that button!

## Cool Features ✨

- Automatically detects when you're watching YouTube
- One click to enable PiP mode (or let it do it automatically!)
- Hangs out in your system tray, staying out of your way
- Shows you what it's doing with a neat little console
- Pretty modern UI (because why not make it look good?)

## Before You Start 📋

You'll need:

- Windows (sorry Mac/Linux folks!)
- Python 3.6+
- Google Chrome
- A YouTube video to watch (obviously 😉)

## Getting It Running 🚀

1. Grab the code:

```bash
git clone https://github.com/yourusername/youtube-pip-controller.git
cd youtube-pip-controller
```

2. Install the stuff it needs:

```bash
pip install pyautogui PyQt5 pywin32 psutil
```

3. Make sure you've got these files in place:

```
youtube-pip-controller/
├── pip-controller.py
├── icons/
│   └── tray_icon.png
└── fonts/
    └── Poppins-Regular.ttf
```

## How to Use It 🎮

1. Fire it up:

```bash
python pip-controller.py
```

2. That's... pretty much it! But if you want the details:
   - Hit "Start" to let it do its thing
   - Hit "Stop" if you want it to take a break
   - Minimize it to your tray if you want it out of the way
   - Right-click the tray icon for more options

## If Something Goes Wrong 🔧

If PiP isn't working:

- Make sure YouTube is actually playing something in Chrome
- Check if Chrome is the active window
- Try hitting Alt+P yourself to see if it works manually

If the app won't start:

- Double-check you installed all the dependencies
- Make sure you've got the font and icon files in the right spots

## Want to Make It Better? 🛠️

Got ideas? Found a bug? Feel free to:

- Fork it
- Fix it
- Send a pull request

I'm always open to improvements!

## What's Next? 🎯

Some things I'm thinking about adding:

- Support for other browsers
- Custom keyboard shortcuts
- Maybe support for other streaming sites
- Auto-start with Windows
- Whatever else seems cool!

## Need Help? 🤝

Just open an issue on GitHub or shoot me a message. I'll help if I can!

## License 📜

MIT License - do whatever you want with it, just don't blame me if something breaks! 😅

---

Made with ☕ and a desire to watch YouTube while pretending to work
