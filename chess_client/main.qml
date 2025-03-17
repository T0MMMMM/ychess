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
    
    // Dark theme colors
    property color darkBackground: "#2e2e2e"
    property color darkSurface: "#383838"
    property color darkText: "#ffffff"
    property color darkAccent: "#5f9ea0"  // Teal-like accent color
    
    // Set the application background color
    color: darkBackground
    
    // StackView pour la gestion des écrans
    StackView {
        id: stackView
        objectName: "stackView"  // Added objectName for access from Python
        anchors.fill: parent
        initialItem: homeScreen
    }
    
    // Composant pour l'écran d'accueil
    Component {
        id: homeScreen
        
        Rectangle {
            color: mainWindow.darkBackground
            
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
                    color: mainWindow.darkText
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Text {
                    visible: backend.isLoggedIn
                    // Liaison directe aux propriétés qui se met à jour automatiquement
                    text: "ELO: " + backend.user.elo + 
                          " | Wins: " + backend.user.wins + 
                          " | Losses: " + backend.user.losses
                    font.pixelSize: 16
                    color: mainWindow.darkText
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Button {
                    text: "Jouer"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    background: Rectangle {
                        color: mainWindow.darkAccent
                        radius: 4
                    }
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: mainWindow.darkText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: {
                        console.log("Bouton Jouer cliqué")
                        if (backend.isLoggedIn) {
                            stackView.push("game.qml", {"stackView": stackView})
                        }
                    }
                }
                
                Button {
                    text: backend.isLoggedIn ? "Déconnexion" : "Connexion"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    background: Rectangle {
                        color: mainWindow.darkSurface
                        radius: 4
                        border.color: mainWindow.darkAccent
                        border.width: 1
                    }
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: mainWindow.darkText
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
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
