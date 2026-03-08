// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 Nyarch Linux

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ScrollablePage {
    id: scriptPage

    property var pageSections: []
    property string pageTitle: ""

    title: pageTitle

    ColumnLayout {
        anchors.left: parent.left
        anchors.right: parent.right
        spacing: Kirigami.Units.largeSpacing

        Repeater {
            model: pageSections

            delegate: ColumnLayout {
                id: sectionDelegate

                required property var modelData

                Layout.fillWidth: true
                spacing: Kirigami.Units.smallSpacing

                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.topMargin: Kirigami.Units.gridUnit
                    Layout.leftMargin: Kirigami.Units.gridUnit * 0.5
                    spacing: Kirigami.Units.smallSpacing / 2

                    Kirigami.Heading {
                        text: modelData.title
                        level: 3
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    Controls.Label {
                        visible: modelData.subtitle !== null && modelData.subtitle !== undefined && modelData.subtitle !== ""
                        text: modelData.subtitle ?? ""
                        opacity: 0.65
                        font.pointSize: Kirigami.Theme.smallFont.pointSize
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
                        Layout.bottomMargin: Kirigami.Units.smallSpacing
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Kirigami.ColorUtils.linearInterpolation(
                        Kirigami.Theme.backgroundColor,
                        Kirigami.Theme.textColor,
                        0.12
                    )
                    Layout.leftMargin: Kirigami.Units.gridUnit * 0.5
                    Layout.rightMargin: Kirigami.Units.gridUnit * 0.5
                    Layout.bottomMargin: Kirigami.Units.smallSpacing / 2
                }

                Repeater {
                    model: modelData.scripts

                    delegate: ScriptCard {
                        required property var modelData

                        Layout.fillWidth: true
                        Layout.leftMargin: Kirigami.Units.gridUnit * 0.5
                        Layout.rightMargin: Kirigami.Units.gridUnit * 0.5

                        scriptTitle: modelData.title
                        scriptSubtitle: modelData.subtitle ?? ""
                        scriptCommand: modelData.description ?? modelData.command ?? ""
                        scriptRunCommand: modelData.command ?? ""
                        scriptWebsite: modelData.website ?? ""
                    }
                }
            }
        }

        Item {
            Layout.preferredHeight: Kirigami.Units.gridUnit
        }
    }

    component ScriptCard: Kirigami.AbstractCard {
        id: card

        property string scriptTitle: ""
        property string scriptSubtitle: ""
        property string scriptCommand: ""
        property string scriptRunCommand: ""
        property string scriptWebsite: ""

        property bool expanded: false

        showClickFeedback: false
        hoverEnabled: false

        Behavior on implicitHeight {
            NumberAnimation {
                duration: 180
                easing.type: Easing.OutCubic
            }
        }

        contentItem: ColumnLayout {
            spacing: 0

            RowLayout {
                id: mainRow
                Layout.fillWidth: true
                spacing: Kirigami.Units.largeSpacing

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Kirigami.Units.smallSpacing / 2

                    Controls.Label {
                        text: scriptTitle
                        font.bold: true
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
                    }

                    Controls.Label {
                        visible: scriptSubtitle !== ""
                        text: scriptSubtitle
                        opacity: 0.65
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
                        font.pointSize: Kirigami.Theme.smallFont.pointSize
                    }
                }

                RowLayout {
                    spacing: Kirigami.Units.smallSpacing
                    Layout.alignment: Qt.AlignVCenter

                    Controls.ToolButton {
                        icon.name: card.expanded ? "go-up" : "go-down"
                        display: Controls.AbstractButton.IconOnly

                        Controls.ToolTip.visible: hovered
                        Controls.ToolTip.text: card.expanded ? qsTr("Hide command") : qsTr("Show command")

                        onClicked: card.expanded = !card.expanded
                    }

                    Controls.ToolButton {
                        visible: scriptWebsite !== ""
                        icon.name: "internet-web-browser"
                        display: Controls.AbstractButton.IconOnly

                        Controls.ToolTip.visible: hovered
                        Controls.ToolTip.text: qsTr("Open website")

                        onClicked: Qt.openUrlExternally(scriptWebsite)
                    }

                    Controls.ToolButton {
                        icon.name: "media-playback-start"
                        display: Controls.AbstractButton.IconOnly

                        Controls.ToolTip.visible: hovered
                        Controls.ToolTip.text: qsTr("Run script in terminal")

                        onClicked: scriptRunner.runScript(scriptRunCommand)
                    }
                }
            }

            Item {
                id: commandContainer
                Layout.fillWidth: true
                implicitHeight: card.expanded ? commandBox.implicitHeight + Kirigami.Units.largeSpacing : 0
                clip: true

                Behavior on implicitHeight {
                    NumberAnimation {
                        duration: 180
                        easing.type: Easing.OutCubic
                    }
                }

                Rectangle {
                    id: commandBox
                    anchors {
                        top: parent.top
                        left: parent.left
                        right: parent.right
                        topMargin: Kirigami.Units.largeSpacing
                    }
                    implicitHeight: commandLabel.implicitHeight
                                    + Kirigami.Units.largeSpacing * 2
                    radius: Kirigami.Units.cornerRadius
                    color: Kirigami.ColorUtils.linearInterpolation(
                        Kirigami.Theme.backgroundColor,
                        Kirigami.Theme.textColor,
                        0.06
                    )
                    border.color: Kirigami.ColorUtils.linearInterpolation(
                        Kirigami.Theme.backgroundColor,
                        Kirigami.Theme.textColor,
                        0.15
                    )
                    border.width: 1

                    Controls.Label {
                        id: commandLabel
                        anchors {
                            top: parent.top
                            left: parent.left
                            right: parent.right
                            margins: Kirigami.Units.largeSpacing
                        }
                        text: scriptCommand
                        font.family: "monospace"
                        font.pointSize: Kirigami.Theme.smallFont.pointSize
                        wrapMode: Text.WrapAnywhere
                        textFormat: Text.PlainText
                        opacity: 0.9
                    }
                }
            }
        }
    }
}
