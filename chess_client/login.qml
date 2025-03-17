import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property var stackView
    
    // Dark theme colors
    property color darkBackground: "#2e2e2e"
    property color darkSurface: "#383838"
    property color darkText: "#ffffff"
    property color darkSecondaryText: "#bbbbbb"
    property color darkAccent: "#5f9ea0"  // Teal-like accent color
    
    color: darkBackground

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        width: parent.width * 0.6
        Layout.maximumWidth: 400

        Text {
            text: "Connexion"
            font.pixelSize: 28
            font.bold: true
            color: darkText
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            id: usernameField
            placeholderText: "Nom d'utilisateur"
            placeholderTextColor: "#888888"
            color: darkText
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            background: Rectangle {
                color: Qt.rgba(0, 0, 0, 0.3)
                border.color: "#555555"
                border.width: 1
                radius: 6
            }
        }

        TextField {
            id: passwordField
            placeholderText: "Mot de passe"
            placeholderTextColor: "#888888"
            color: darkText
            echoMode: TextInput.Password
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            background: Rectangle {
                color: Qt.rgba(0, 0, 0, 0.3)
                border.color: "#555555"
                border.width: 1
                radius: 6
            }
        }

        Button {
            text: "Se connecter"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 20
            background: Rectangle {
                color: darkAccent
                radius: 6
            }
            contentItem: Text {
                text: parent.text
                font.pixelSize: 16
                font.bold: true
                color: darkText
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onClicked: {
                backend.login(usernameField.text, passwordField.text)
            }
        }

        Button {
            text: "Retour"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 10
            background: Rectangle {
                color: darkSurface
                radius: 6
                border.color: darkAccent
                border.width: 1
            }
            contentItem: Text {
                text: parent.text
                font.pixelSize: 16
                color: darkText
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onClicked: {
                stackView.pop()
            }
        }
    }

    // Connexion au signal loginResult pour retourner à l'écran principal en cas de succès
    Connections {
        target: backend
        function onLoginResult(success) {
            if (success) {
                stackView.pop()
            } else {
                // Afficher un message d'erreur
                errorMessage.visible = true
            }
        }
    }

    Text {
        id: errorMessage
        text: "Échec de la connexion. Veuillez réessayer."
        color: "#ff5252"
        font.pixelSize: 14
        visible: false
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 30
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
