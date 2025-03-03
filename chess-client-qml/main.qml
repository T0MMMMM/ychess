import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

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
                    text: "Chess Game"
                    font.pixelSize: 24
                    font.bold: true
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Button {
                    text: "Jouer"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    onClicked: {
                        console.log("Bouton Jouer cliqué")
                        backend.jouer()
                    }
                }
                
                Button {
                    text: "Connexion"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    onClicked: {
                        console.log("Bouton Connexion cliqué")
                        stackView.push("login.qml", {"stackView": stackView})
                    }
                }
            }
        }
    }
}
