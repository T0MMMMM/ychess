import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property var stackView
    color: "#f5f5f5"

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        width: parent.width * 0.6
        Layout.maximumWidth: 400

        Text {
            text: "Connexion"
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            id: usernameField
            placeholderText: "Nom d'utilisateur"
            Layout.fillWidth: true
            Layout.preferredHeight: 40
        }

        TextField {
            id: passwordField
            placeholderText: "Mot de passe"
            echoMode: TextInput.Password
            Layout.fillWidth: true
            Layout.preferredHeight: 40
        }

        Button {
            text: "Se connecter"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            onClicked: {
                backend.login(usernameField.text, passwordField.text)
            }
        }

        Button {
            text: "Retour"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
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
        color: "red"
        visible: false
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
