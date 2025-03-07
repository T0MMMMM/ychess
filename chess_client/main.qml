import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ChessTypes 1.0

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 800
    height: 600
    title: "Chess Game"
    
    // Occuper tout l'écran
    visibility: "Maximized"
    
    // StackView pour la gestion des écrans
    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: homeScreen
    }
    
    // Composant pour l'écran d'accueil
    Component {
        id: homeScreen
        
        Rectangle {
            color: "#f5f5f5"
            
            ColumnLayout {
                anchors.centerIn: parent
                spacing: 20
                width: parent.width * 0.6
                Layout.maximumWidth: 400
                
                Text {
                    id: userText
                    // Liaison directe qui se met à jour automatiquement
                    text: backend.isLoggedIn ? "Welcome, " + backend.user.username : "Please log in"
                    font.pixelSize: 24
                    font.bold: true
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Text {
                    visible: backend.isLoggedIn
                    // Liaison directe aux propriétés qui se met à jour automatiquement
                    text: "ELO: " + backend.user.elo + 
                          " | Wins: " + backend.user.wins + 
                          " | Losses: " + backend.user.losses
                    font.pixelSize: 16
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Button {
                    text: "Jouer"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    onClicked: {
                        console.log("Bouton Jouer cliqué")
                        backend.play()
                        if (backend.isLoggedIn) {
                            stackView.push("waiting.qml", {"stackView": stackView})
                        }

                    }
                }
                
                Button {
                    text: backend.isLoggedIn ? "Déconnexion" : "Connexion"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    onClicked: {
                        if (backend.isLoggedIn) {
                            backend.logout()
                        } else {
                            stackView.push("login.qml", {"stackView": stackView})
                        }
                    }
                }
            }
        }
    }
}
