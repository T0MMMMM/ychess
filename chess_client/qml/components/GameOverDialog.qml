import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: gameOverScreen
    color: "#2d2d2d"  // Dark background
    
    // Properties to be set from the parent
    property var parentStackView: null
    property string result: ""
    property string details: ""
    
    // Title header
    Rectangle {
        id: header
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 60
        color: "#353535"
        
        Text {
            anchors.centerIn: parent
            text: "Game Over"
            font.pixelSize: 24
            font.bold: true
            color: "#ffffff"
        }
    }
    
    // Content area
    Rectangle {
        id: content
        anchors.top: header.bottom
        anchors.bottom: footer.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        color: "transparent"
        
        ColumnLayout {
            anchors.centerIn: parent
            width: Math.min(parent.width - 40, 400)
            spacing: 20
            
            // Result icon (trophy for win, etc.)
            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 100
                Layout.preferredHeight: 100
                radius: 50
                color: getResultColor()
                
                Text {
                    anchors.centerIn: parent
                    text: getResultIcon()
                    font.pixelSize: 50
                    color: "#ffffff"
                }
            }
            
            // Result text
            Text {
                Layout.alignment: Qt.AlignHCenter
                text: result
                font.pixelSize: 32
                font.bold: true
                color: getResultColor()
            }
            
            // Details text
            Text {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                text: details
                font.pixelSize: 18
                color: "#bbbbbb"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
    
    // Footer with buttons
    Rectangle {
        id: footer
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 80
        color: "transparent"
        
        RowLayout {
            anchors.centerIn: parent
            width: Math.min(parent.width - 40, 400)
            spacing: 20
            
            Button {
                Layout.fillWidth: true
                text: "Return to Menu"
                background: Rectangle {
                    color: "#424242"
                    radius: 5
                }
                contentItem: Text {
                    text: parent.text
                    color: "#ffffff"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                onClicked: {
                    // Return to the main menu
                    if (parentStackView) {
                        // Pop back to the home screen
                        parentStackView.pop(null);
                    }
                }
            }
            
            Button {
                Layout.fillWidth: true
                text: "New Game"
                background: Rectangle {
                    color: "#5f9ea0" // Teal accent
                    radius: 5
                }
                contentItem: Text {
                    text: parent.text
                    color: "#ffffff"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                onClicked: {
                    backend.play(); // Start a new game
                    if (parentStackView) {
                        // Pop the current screen, the matchmaking will push a new game screen
                        parentStackView.pop();
                    }
                }
            }
        }
    }
    
    // Helper functions
    function getResultColor() {
        if (result === "Victory!") return "#4caf50"; // Green for victory
        if (result === "Defeat") return "#f44336";   // Red for defeat
        return "#ff9800";                            // Orange for draw
    }
    
    function getResultIcon() {
        if (result === "Victory!") return "🏆"; // Trophy for victory
        if (result === "Defeat") return "❌";    // X for defeat
        return "🤝";                             // Handshake for draw
    }
}
