#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Nyarch Linux

"""Main application entry point for NyarchScript QT"""

import os
import sys
import signal
from importlib import resources

from PySide6.QtGui import QGuiApplication, QIcon, QFont, QFontDatabase
from PySide6.QtCore import QUrl, QCoreApplication
from PySide6.QtQml import QQmlApplicationEngine

from nyarchscriptqt.scripts_model import ScriptsModel, ScriptRunner  # noqa: F401


def run() -> int:
    """Initializes and manages the application execution"""

    QCoreApplication.setApplicationName("NyarchScript QT")
    QCoreApplication.setOrganizationName("Nyarch Linux")
    QCoreApplication.setOrganizationDomain("nyarchlinux.moe")
    QCoreApplication.setApplicationVersion("0.1.0")

    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "org.kde.desktop")

    app = QGuiApplication(sys.argv)
    app.setDesktopFileName("moe.nyarchlinux.scriptsqt")
    app.setWindowIcon(QIcon.fromTheme("moe.nyarchlinux.scriptsqt"))

    system_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
    app.setFont(system_font)

    engine = QQmlApplicationEngine()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    scripts_model = ScriptsModel()
    engine.rootContext().setContextProperty("scriptsModel", scripts_model)

    script_runner = ScriptRunner()
    engine.rootContext().setContextProperty("scriptRunner", script_runner)

    pkg_files = resources.files("nyarchscriptqt")
    icons_path = str(pkg_files.joinpath("icons"))
    engine.rootContext().setContextProperty("iconsPath", f"file://{icons_path}")

    main_qml = pkg_files.joinpath("qml/main.qml")
    engine.load(QUrl.fromLocalFile(str(main_qml)))

    if not engine.rootObjects():
        return 1

    return app.exec()


def main() -> None:
    raise SystemExit(run())
