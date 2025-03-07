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


        Button {
            text: "Annuler"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            onClicked: {
                backend.cancelMatchmaking()
                stackView.pop() // Fermer la page d'attente
            }
        }
    }

}