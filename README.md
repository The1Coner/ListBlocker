# ListBlocker
ListBlocker is a lightweight .exe utility that automatically minimizes apps through list input. It is useful for productivity, focus, and avoiding distraction.
# Installation
Install the .exe, and run it.
# Features
- Persistent block list (JSON)
- System tray app
- Live monitoring
- Minimizes processes
- Standalone executable
# Screenshots
![Blocker](screenshot_listblocker_main.png)
![Config](screenshot_listblocker_config.png)
# Why I made it
I built ListBlocker to practice process monitoring, persistent configuration, packaging Python apps into executables, and user interfaces.
# How it works
A background loop runs that, on an interval of every one second, checks running processes. If a process name matches one in the list, its window is minimized. The block list is stored locally and loaded upon starting the app.
