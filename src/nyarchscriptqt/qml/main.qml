// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 Nyarch Linux

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: root

    title: qsTr("NyarchScript")

    minimumWidth: Kirigami.Units.gridUnit * 38
    minimumHeight: Kirigami.Units.gridUnit * 36
    width: Kirigami.Units.gridUnit * 44
    height: Kirigami.Units.gridUnit * 42

    property int currentPageIndex: 0

    globalDrawer: Kirigami.GlobalDrawer {
        title: qsTr("NyarchScript")
        titleIcon: "moe.nyarchlinux.scriptsqt"
        modal: false
        collapsible: true

        actions: [
            Kirigami.Action {
                text: scriptsModel.getTabTitle(0)
                icon.source: iconsPath + "/" + scriptsModel.getTabIcon(0) + ".svg"
                checked: root.currentPageIndex === 0
                onTriggered: root.switchToPage(0)
            },
            Kirigami.Action {
                text: scriptsModel.getTabTitle(1)
                icon.source: iconsPath + "/" + scriptsModel.getTabIcon(1) + ".svg"
                checked: root.currentPageIndex === 1
                onTriggered: root.switchToPage(1)
            },
            Kirigami.Action {
                text: scriptsModel.getTabTitle(2)
                icon.source: iconsPath + "/" + scriptsModel.getTabIcon(2) + ".svg"
                checked: root.currentPageIndex === 2
                onTriggered: root.switchToPage(2)
            },
            Kirigami.Action {
                text: scriptsModel.getTabTitle(3)
                icon.source: iconsPath + "/" + scriptsModel.getTabIcon(3) + ".svg"
                checked: root.currentPageIndex === 3
                onTriggered: root.switchToPage(3)
            },
            Kirigami.Action {
                separator: true
            },
            Kirigami.Action {
                text: qsTr("About NyarchScript")
                icon.name: "help-about"
                onTriggered: aboutDialog.open()
            },
            Kirigami.Action {
                text: qsTr("Quit")
                icon.name: "application-exit"
                onTriggered: Qt.quit()
            }
        ]
    }

    Component {
        id: scriptPageComponent
        ScriptPage {}
    }

    function switchToPage(index) {
        currentPageIndex = index
        pageStack.clear()
        pageStack.push(scriptPageComponent, {
            pageSections: scriptsModel.getSections(index),
            pageTitle: scriptsModel.getTabTitle(index)
        })
    }

    Component.onCompleted: switchToPage(0)

    Kirigami.Dialog {
        id: aboutDialog
        title: qsTr("About NyarchScript QT")
        standardButtons: Kirigami.Dialog.Close
        preferredWidth: Kirigami.Units.gridUnit * 22

        ColumnLayout {
            spacing: Kirigami.Units.largeSpacing

            Kirigami.Icon {
                source: "moe.nyarchlinux.scriptsqt"
                Layout.preferredWidth: Kirigami.Units.iconSizes.enormous
                Layout.preferredHeight: Kirigami.Units.iconSizes.enormous
                Layout.alignment: Qt.AlignHCenter
            }

            Kirigami.Heading {
                text: qsTr("NyarchScript QT")
                level: 1
                Layout.alignment: Qt.AlignHCenter
            }

            Controls.Label {
                text: qsTr("Version 0.1.0")
                Layout.alignment: Qt.AlignHCenter
                opacity: 0.7
            }

            Controls.Label {
                text: qsTr("A Kirigami GUI for running system maintenance and installation scripts on Nyarch Linux.")
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
            }

            Controls.Label {
                text: qsTr("Built with Kirigami for KDE Plasma")
                Layout.alignment: Qt.AlignHCenter
                opacity: 0.7
            }

            Controls.Label {
                text: "\u00A9 2024 Nyarch Linux"
                Layout.alignment: Qt.AlignHCenter
                opacity: 0.5
            }
        }
    }

    Shortcut {
        sequence: StandardKey.Quit
        onActivated: Qt.quit()
    }
}
