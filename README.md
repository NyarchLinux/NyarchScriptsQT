# NyarchScript QT

A Kirigami/PySide6 GUI application for running system maintenance and installation scripts on Nyarch Linux.

This is the KDE Plasma port of [NyarchScript](https://github.com/nyarchlinux/nyarchscript), built with Kirigami for seamless KDE integration.

## Features

- **Updates** — Pacman operations, mirrorlist management, Nyarch app updates
- **Install** — CLI tools, performance utilities, kernel options, theming, drivers
- **Tweaks** — System maintenance and touchscreen support
- **Information** — System info and diagnostics

Scripts run in a **Kitty** terminal window via `flatpak-spawn --host`.

## Building

```bash
# Run directly (requires PySide6 + Kirigami)
bash install.sh --run

# Install as Flatpak
bash install.sh --install

# Create a .flatpak bundle
bash install.sh --bundle
```

## Requirements

- PySide6
- KDE Kirigami (`org.kde.kirigami` QML module)
- Kitty terminal emulator (on the host)
