#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Nyarch Linux

"""Scripts data model and runner for QML consumption"""

import subprocess
import os 

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QObject, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "moe.nyarchlinux.scriptsqt"
QML_IMPORT_MAJOR_VERSION = 1


SCRIPTS = [
    {
        "title": "Updates",
        "icon": "updates-symbolic",
        "sections": [
            {
                "title": "Pacman",
                "subtitle": "Some useful operations you can do with Arch Linux package manager",
                "scripts": [
                    {
                        "title": "Run full System Update",
                        "subtitle": "Update the system and all of its packages",
                        "command": "sudo pacman -Syu;sudo flatpak update; exec bash",
                        "description": "sudo pacman -Syu",
                    },
                    {
                        "title": "Force refresh packages list",
                        "subtitle": "Mirrors can be out of sync, use this command to resynchronize them",
                        "command": "sudo pacman -Syyu; exec bash",
                        "description": "sudo pacman -Syyu",
                    },
                    {
                        "title": "Refresh Pacman keys",
                        "subtitle": "NOTE: Takes some time. In case there are problems with keys, you can refresh every pacman key",
                        "command": "sudo pacman-key --refresh-keys; exec bash",
                        "description": "sudo pacman-key --refresh-keys",
                    },
                    {
                        "title": "Update mirrorlist",
                        "subtitle": "Will update the mirrorlist for faster downloads using pacman",
                        "command": "sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak;sudo reflector --verbose --latest 10 --protocol https --sort rate --save /etc/pacman.d/mirrorlist; exec bash",
                        "description": "sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak\nsudo reflector --verbose --latest 10 --protocol https --sort rate --save /etc/pacman.d/mirrorlist",
                    },
                    {
                        "title": "Restore old mirrorlist",
                        "subtitle": "Restore old mirrorlist if mirrorlist update failed",
                        "command": "sudo rm -rf /etc/pacman.d/mirrorlist; sudo cp /etc/pacman.d/mirrorlist.bak /etc/pacman.d/mirrorlist; exec bash",
                        "description": "sudo rm -rf /etc/pacman.d/mirrorlist\nsudo cp /etc/pacman.d/mirrorlist.bak /etc/pacman.d/mirrorlist",
                    },
                    {
                        "title": "Remove db lock",
                        "subtitle": "Remove pacman db lock in case of errors",
                        "command": "sudo rm -rf /var/lib/pacman/db.lck; exec bash",
                        "description": "sudo rm -rf /var/lib/pacman/db.lck",
                    },
                ],
            },
            {
                "title": "Nyarch Applications",
                "subtitle": "Nyarch Linux applications are not automatically updated, use this section to update them",
                "scripts": [
                    {
                        "title": "Update Nyarch Updater",
                        "subtitle": "Update Nyarch Updater application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/nyarchupdater/releases/latest/download/nyarchupdater.flatpak; flatpak install nyarchupdater.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/nyarchupdater/releases/latest/download/nyarchupdater.flatpak\nflatpak install nyarchupdater.flatpak",
                    },
                    {
                        "title": "Update Nyarch Assistant",
                        "subtitle": "Update Nyarch Assistant application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/nyarchassistant/releases/latest/download/nyarchassistant.flatpak; flatpak install nyarchassistant.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/nyarchassistant/releases/latest/download/nyarchassistant.flatpak\nflatpak install nyarchassistant.flatpak",
                    },
                    {
                        "title": "Update Nyarch Tour",
                        "subtitle": "Update Nyarch Tour application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/nyarchtour/releases/latest/download/nyarchtour.flatpak; flatpak install nyarchtour.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/nyarchtour/releases/latest/download/nyarchtour.flatpak\nflatpak install nyarchtour.flatpak",
                    },
                    {
                        "title": "Update Nyarch Customize",
                        "subtitle": "Update Nyarch Customize application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/nyarchcustomize/releases/latest/download/nyarchcustomize.flatpak; flatpak install nyarchcustomize.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/nyarchcustomize/releases/latest/download/nyarchcustomize.flatpak\nflatpak install nyarchcustomize.flatpak",
                    },
                    {
                        "title": "Update Nyarch Wizard",
                        "subtitle": "Update Nyarch Wizard application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/nyarchwizard/releases/latest/download/wizard.flatpak; flatpak install wizard.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/nyarchwizard/releases/latest/download/wizard.flatpak\nflatpak install wizard.flatpak",
                    },
                    {
                        "title": "Update Catgirl Downloader",
                        "subtitle": "Update Catgirl Downloader application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/catgirldownloader/releases/latest/download/catgirldownloader.flatpak; flatpak install catgirldownloader.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/catgirldownloader/releases/latest/download/catgirldownloader.flatpak\nflatpak install catgirldownloader.flatpak",
                    },
                    {
                        "title": "Update Waifu Downloader",
                        "subtitle": "Update Waifu Downloader application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/waifudownloader/releases/latest/download/waifudownloader.flatpak; flatpak install waifudownloader.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/waifudownloader/releases/latest/download/waifudownloader.flatpak\nflatpak install waifudownloader.flatpak",
                    },
                    {
                        "title": "Update Nyarch Script",
                        "subtitle": "Update Nyarch Script application by downloading it from the latest release on GitHub",
                        "command": "cd /tmp; wget https://github.com/nyarchlinux/nyarchscript/releases/latest/download/nyarchscript.flatpak; flatpak install nyarchscript.flatpak;exec bash",
                        "description": "cd /tmp\nwget https://github.com/nyarchlinux/nyarchscript/releases/latest/download/nyarchscript.flatpak\nflatpak install nyarchscript.flatpak",
                    },
                    {
                        "title": "Update Material You",
                        "subtitle": "Update Material You extension, the GNOME extension that manages Material You theming",
                        "command": "cd /tmp; git clone https://github.com/FrancescoCaracciolo/material-you-colors.git; cd material-you-colors; make build;make install; npm install --prefix $HOME/.local/share/gnome-shell/extensions/material-you-colors@francescocaracciolo.github.io;cd $HOME/.local/share/gnome-shell/extensions/material-you-colors@francescocaracciolo.github.io; git clone https://github.com/francescocaracciolo/adwaita-material-you; cd adwaita-material-you; bash local-install.sh; exec bash",
                        "description": "cd /tmp\ngit clone https://github.com/FrancescoCaracciolo/material-you-colors.git\ncd material-you-colors\nmake build && make install\nnpm install --prefix $HOME/.local/share/gnome-shell/extensions/material-you-colors@francescocaracciolo.github.io\ncd adwaita-material-you && bash local-install.sh",
                    },
                ],
            },
        ],
    },
    {
        "title": "Install",
        "icon": "palette-symbolic",
        "sections": [
            {
                "title": "Command-line Utilities",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Install fish",
                        "subtitle": "This command installs fish and sets it as default shell",
                        "command": "sudo pacman -Sy fish;chsh -s $(which fish); exec fish",
                        "description": "sudo pacman -Sy fish\nchsh -s $(which fish)",
                    },
                    {
                        "title": "Install Oh My Fish!",
                        "subtitle": "This command installs Oh My Fish to tweak fish easily",
                        "command": "curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish;exec fish",
                        "description": "curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish",
                        "website": "https://github.com/oh-my-fish/oh-my-fish#Getting-Started",
                    },
                ],
            },
            {
                "title": "Performance",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Install preload",
                        "subtitle": "Makes applications run faster by prefetching binaries and shared objects",
                        "command": "yay -Sy preload; sudo systemctl enable --now preload; exec bash",
                        "description": "yay -Sy preload\nsudo systemctl enable --now preload",
                    },
                    {
                        "title": "Install auto-cpufreq",
                        "subtitle": "Automatic CPU speed and power optimizer, useful to enhance laptop battery life",
                        "command": "yay -Sy auto-cpufreq;exec bash",
                        "description": "yay -Sy auto-cpufreq",
                        "website": "https://github.com/AdnanHodzic/auto-cpufreq",
                    },
                    {
                        "title": "Install power-profiles-daemon",
                        "subtitle": "Power Profiles daemon modifies system behaviour based upon user-selected power profiles",
                        "command": "sudo pacman -Sy power-profiles-daemon;exec bash",
                        "description": "sudo pacman -Sy power-profiles-daemon",
                    },
                ],
            },
            {
                "title": "Kernels",
                "subtitle": "After installing, select your preferred kernel in GRUB advanced options",
                "scripts": [
                    {
                        "title": "Install Linux Zen Kernel",
                        "subtitle": "Installs the Linux Zen kernel, optimized for desktop use",
                        "command": "sudo pacman -Sy linux-zen linux-zen-headers;exec bash",
                        "description": "sudo pacman -Sy linux-zen linux-zen-headers",
                    },
                    {
                        "title": "Install Linux LTS Kernel",
                        "subtitle": "Installs the Long Term Support kernel, useful if you have issues with proprietary drivers",
                        "command": "sudo pacman -Sy linux-lts linux-lts-headers;exec bash",
                        "description": "sudo pacman -Sy linux-lts linux-lts-headers",
                    },
                ],
            },
            {
                "title": "Themes",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Firefox GNOME Theme",
                        "subtitle": "Make Firefox more coherent with your GNOME desktop",
                        "command": "cd /tmp; git clone https://github.com/rafaelmardojai/firefox-gnome-theme; cd firefox-gnome-theme; bash scripts/auto-install.sh; exec bash",
                        "description": "cd /tmp\ngit clone https://github.com/rafaelmardojai/firefox-gnome-theme\ncd firefox-gnome-theme && bash scripts/auto-install.sh",
                        "website": "https://github.com/rafaelmardojai/firefox-gnome-theme",
                    },
                    {
                        "title": "Uninstall Firefox GNOME Theme",
                        "subtitle": "Uninstall Firefox GNOME Theme",
                        "command": "xdg-open https://github.com/rafaelmardojai/firefox-gnome-theme#uninstalling",
                        "description": "See: https://github.com/rafaelmardojai/firefox-gnome-theme#uninstalling",
                        "website": "https://github.com/rafaelmardojai/firefox-gnome-theme#uninstalling",
                    },
                    {
                        "title": "Discord Dnome Theme",
                        "subtitle": "Make Discord more coherent with your desktop, also installs Crycord to inject CSS",
                        "command": "yay -S crycord; mkdir -p ~/.config/discord-themes; cd ~/.config/discord-themes; wget https://raw.githubusercontent.com/GeopJr/DNOME/main/DNOME-latest.css; crycord -c ~/.config/discord-themes/DNOME-latest.css;exec bash",
                        "description": "yay -S crycord\nmkdir -p ~/.config/discord-themes\nwget https://raw.githubusercontent.com/GeopJr/DNOME/main/DNOME-latest.css\ncrycord -c ~/.config/discord-themes/DNOME-latest.css",
                        "website": "https://github.com/NyarchLinux/NyarchScript/tree/master/docs/DNOME.md",
                    },
                    {
                        "title": "Uninstall Discord Dnome Theme",
                        "subtitle": "Uninstall Dnome theme from Discord",
                        "command": "crycord -r; exec bash",
                        "description": "crycord -r",
                    },
                    {
                        "title": "Install Pywalfox",
                        "subtitle": "Adapts Firefox theme color to the Nyarch Linux theme",
                        "command": "yay -Sy python-pywalfox; pywalfox install; xdg-open https://addons.mozilla.org/it/firefox/addon/pywalfox/; exec bash",
                        "description": "yay -Sy python-pywalfox\npywalfox install",
                        "website": "https://addons.mozilla.org/it/firefox/addon/pywalfox/",
                    },
                    {
                        "title": "Install Wal VSCode Theme",
                        "subtitle": "Adapts VSCode theme color to the Nyarch Linux theme",
                        "command": "xdg-open https://marketplace.visualstudio.com/items?itemName=dlasagno.wal-theme",
                        "description": "Open VSCode Marketplace: dlasagno.wal-theme",
                        "website": "https://marketplace.visualstudio.com/items?itemName=dlasagno.wal-theme",
                    },
                ],
            },
            {
                "title": "Drivers",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Install NVIDIA Drivers",
                        "subtitle": "Open the installation guide for NVIDIA drivers on Arch Linux",
                        "command": "xdg-open https://github.com/korvahannu/arch-nvidia-drivers-installation-guide",
                        "description": "See guide: https://github.com/korvahannu/arch-nvidia-drivers-installation-guide",
                        "website": "https://github.com/korvahannu/arch-nvidia-drivers-installation-guide",
                    },
                    {
                        "title": "Install Wacom Drivers",
                        "subtitle": "Install Wacom drivers for graphics tablets and stylus devices",
                        "command": "sudo pacman -Sy xf86-input-wacom libwacom;trizen -S input-wacom-dkms wacom-utility;exec bash",
                        "description": "sudo pacman -Sy xf86-input-wacom libwacom\ntrizen -S input-wacom-dkms wacom-utility",
                    },
                    {
                        "title": "Install Wacom Drivers for Surface Devices",
                        "subtitle": "Install a patched version of libwacom for Microsoft Surface devices",
                        "command": "yay -Sy libwacom-surface;exec bash",
                        "description": "yay -Sy libwacom-surface",
                    },
                ],
            },
        ],
    },
    {
        "title": "Tweaks",
        "icon": "tweaks-symbolic",
        "sections": [
            {
                "title": "Maintenance Scripts",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Enable Bluetooth Service",
                        "subtitle": "Enable and start the Bluetooth service",
                        "command": "sudo systemctl enable --now bluetooth.service;exec bash",
                        "description": "sudo systemctl enable --now bluetooth.service",
                    },
                    {
                        "title": "Cleanup Journal Space",
                        "subtitle": "Clean up journalctl logs older than two weeks to free disk space",
                        "command": "sudo journalctl --vacuum-time=2weeks;exec bash",
                        "description": "sudo journalctl --vacuum-time=2weeks",
                    },
                    {
                        "title": "Clean Package Cache",
                        "subtitle": "Remove cached pacman packages to free up disk space",
                        "command": "sudo pacman -Scc;exec bash",
                        "description": "sudo pacman -Scc",
                    },
                    {
                        "title": "Reset All Pacman Keys",
                        "subtitle": "NOTE: May take several minutes. Reset pacman keys to fix key-related update errors",
                        "command": "sudo rm /var/lib/pacman/sync/*; sudo rm -rf /etc/pacman.d/gnupg/*; sudo pacman-key --init; sudo pacman-key --populate; sudo pacman -S --noconfirm archlinux-keyring;exec bash",
                        "description": "sudo rm /var/lib/pacman/sync/*\nsudo rm -rf /etc/pacman.d/gnupg/*\nsudo pacman-key --init\nsudo pacman-key --populate\nsudo pacman -S --noconfirm archlinux-keyring",
                    },
                ],
            },
            {
                "title": "Touchscreen Scripts",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Install Screen Autorotate Extension",
                        "subtitle": "Enable automatic screen rotation regardless of touch mode",
                        "command": "cd /tmp; git clone https://github.com/shyzus/gnome-shell-extension-screen-autorotate.git; mv gnome-shell-extension-screen-autorotate/screen-rotate@shyzus.github.io ~/.local/share/gnome-shell/extensions/;exec bash",
                        "description": "cd /tmp\ngit clone https://github.com/shyzus/gnome-shell-extension-screen-autorotate.git\nmv gnome-shell-extension-screen-autorotate/screen-rotate@shyzus.github.io ~/.local/share/gnome-shell/extensions/",
                    },
                ],
            },
        ],
    },
    {
        "title": "Information",
        "icon": "info-symbolic",
        "sections": [
            {
                "title": "System Information Commands",
                "subtitle": None,
                "scripts": [
                    {
                        "title": "Run nyaofetch",
                        "subtitle": "Show general system information with the Nyarch fetch tool",
                        "command": "nyaofetch;exec bash",
                        "description": "nyaofetch",
                    },
                    {
                        "title": "Run btop",
                        "subtitle": "Show an interactive overview of system resource usage",
                        "command": "btop;exec bash",
                        "description": "btop",
                    },
                    {
                        "title": "Check Temperatures",
                        "subtitle": "Show current CPU and hardware temperatures",
                        "command": "sensors;exec bash",
                        "description": "sensors",
                    },
                    {
                        "title": "Check Session Type",
                        "subtitle": "Show whether the current session is running on Wayland or X11",
                        "command": "echo $XDG_SESSION_TYPE;exec bash",
                        "description": "echo $XDG_SESSION_TYPE",
                    },
                ],
            },
        ],
    },
]


@QmlElement
class ScriptsModel(QAbstractListModel):
    """Model exposing top-level tab data to QML"""

    TitleRole = Qt.UserRole + 1
    IconRole = Qt.UserRole + 2
    SectionsRole = Qt.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scripts = SCRIPTS

    def rowCount(self, parent=QModelIndex()):
        return len(self._scripts)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._scripts):
            return None

        tab = self._scripts[index.row()]

        if role == self.TitleRole:
            return tab.get("title", "")
        elif role == self.IconRole:
            return tab.get("icon", "")
        elif role == self.SectionsRole:
            return tab.get("sections", [])

        return None

    def roleNames(self):
        return {
            self.TitleRole: b"title",
            self.IconRole: b"icon",
            self.SectionsRole: b"sections",
        }

    @Slot(result=int)
    def tabCount(self):
        return len(self._scripts)

    @Slot(int, result=str)
    def getTabTitle(self, index):
        if 0 <= index < len(self._scripts):
            return self._scripts[index].get("title", "")
        return ""

    @Slot(int, result=str)
    def getTabIcon(self, index):
        if 0 <= index < len(self._scripts):
            return self._scripts[index].get("icon", "")
        return ""

    @Slot(int, result=list)
    def getSections(self, index):
        if 0 <= index < len(self._scripts):
            return self._scripts[index].get("sections", [])
        return []


@QmlElement
class ScriptRunner(QObject):
    """Handles running shell commands in a terminal"""

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def is_flatpak(self) -> bool:
        """
        Check if we are in a flatpak

        Returns:
            bool: True if we are in a flatpak
        """
        if os.getenv("container"):
            return True
        return False

    def get_spawn_command(self) -> list:
        """
        Get the spawn command to run commands on the user system

        Returns:
            list: space diveded command  
        """
        if self.is_flatpak():
            return ["flatpak-spawn", "--host"]
        else:
            return []

    @Slot(str)
    def runScript(self, command):
        """Run command in a new kitty terminal window via flatpak-spawn"""
        subprocess.Popen(
            self.get_spawn_command() + ["konsole", "-e", "bash", "-c", command]
        )
