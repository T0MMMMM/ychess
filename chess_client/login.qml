import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property var stackView
    
    implicitWidth: stackView ? stackView.width : 800
    implicitHeight: stackView ? stackView.height : 600
    color: "#f0f0f0"
    
    // Connexion du signal loginResult à une fonction JavaScript
    Connections {
        target: backend
        function onLoginResult(success) {
            console.log("Résultat de connexion reçu: " + success)
            if (success) {
                stackView.pop()
                console.log("Connexion réussie")
                errorMessage.visible = false
                // Ici vous pouvez rediriger vers une autre page après connexion
            } else {
                console.log("Échec de la connexion")
                errorMessage.visible = true
            }
        }
    }
    
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
        
        // Message d'erreur
        Text {
            id: errorMessage
            text: "Échec de la connexion. Veuillez vérifier vos identifiants."
            color: "red"
            visible: false
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
        
        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            
            Button {
                text: "Se connecter"
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                onClicked: {
                    console.log("Tentative de connexion")
                    // Cacher le message d'erreur lors d'une nouvelle tentative
                    errorMessage.visible = false
                    backend.login(usernameField.text, passwordField.text)
                }
            }
            
            Button {
                text: "Retour"
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                onClicked: {
                    console.log("Retour à l'accueil")
                    stackView.pop()
                }
            }
        }
    }
}
