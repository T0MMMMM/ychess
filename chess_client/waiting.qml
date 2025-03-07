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
            text: "Recherche d'un match en cours..."
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        ProgressBar {
            id: progressBar
            running: true
            indeterminate: true
            Layout.fillWidth: true
            Layout.preferredHeight: 20
        }

        Button {
            text: "Annuler"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            onClicked: {
                // Logique pour annuler la recherche
                stackView.pop() // Fermer la page d'attente
            }
        }
    }

    // Pour simuler un délai de recherche (remplacer par la logique réelle)
    Timer {
        id: matchTimer
        interval: 5000 // Délai de 5 secondes avant de trouver un match
        running: false
        repeat: false
        onTriggered: {
            stackView.push("Match trouvé!") // Remplacez cela par l'écran suivant ou la logique
        }
    }

    Component.onCompleted: {
        matchTimer.start() // Démarrer le timer au démarrage de la page
    }
}