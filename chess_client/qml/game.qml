import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ChessTypes 1.0

Rectangle {
    id: gameScreen
    objectName: "gameScreen"
    
    // Propriétés de base avec valeurs par défaut
    property int labelSize: 24
    property var matchData: ({})
    property string selectedSquare: ""
    property var possibleMoves: []
    property bool boardFlipped: false
    property bool gameStarted: false
    property bool isMyTurn: false
    property string playerColor: "white"

    // Property to receive stackView from parent
    property var stackView
    
    // Properties to store game over information
    property string dialogResult: ""
    property string dialogDetails: ""

    // Un seul Timer pour l'initialisation
    Timer {
        id: gameStateTimer
        interval: 100
        running: true
        repeat: false
        onTriggered: {
            if (backend && backend.chessGame) {
                // Inverser l'échiquier pour les noirs
                boardFlipped = backend.chessGame.player_color === "black"
                // Safely check if match_id exists and is not null
                gameStarted = backend.chessGame.match_id !== null && backend.chessGame.match_id !== "None"
                isMyTurn = backend.chessGame.is_my_turn
                playerColor = backend.chessGame.player_color
                chessboard.repeater.model = 64
            }
        }
    }

    // Une seule connexion au backend
    Connections {
        target: backend.chessGame
        
        function onBoardChanged() {
            selectedSquare = ""
            possibleMoves = []
            isMyTurn = backend.chessGame.is_my_turn
            playerColor = backend.chessGame.player_color
            
            // Update boardFlipped whenever the board state changes
            boardFlipped = playerColor === "black"
            chessboard.repeater.model = 64
        }
        
        function onGameOver(winner, reason) {
            console.log("Game over:", winner, reason)
            let result = ""
            let resultDetails = ""
            
            // Set result text based on winner
            if (winner === "draw") {
                result = "Game Drawn"
                resultDetails = "The game ended in a draw by " + reason + "."
            } else {
                const playerWon = winner === playerColor
                result = playerWon ? "Victory!" : "Defeat"
                resultDetails = playerWon ? "You won by checkmate!" : "Your opponent won by checkmate."
            }
            
            // Au lieu de charger la boîte de dialogue via un Loader,
            // faire un push directement sur la stackView
            stackView.push("components/GameOverDialog.qml", {
                "parentStackView": stackView,
                "result": result,
                "details": resultDetails
            });
        }
    }

    Component.onCompleted: {
        // Ensure board is flipped right from the start if playing as black
        boardFlipped = backend.chessGame.player_color === "black"
    }

    // Dark theme colors
    property color darkBackground: "#1e1e1e"  // Darker background for modern look
    property color darkSurface: "#2d2d2d"
    property color darkCard: "#353535"
    property color darkText: "#ffffff"
    property color darkSecondaryText: "#bbbbbb"
    property color darkAccent: "#5f9ea0"  // Teal-like accent color
    
    // Chess.com board colors
    property color lightSquare: "#f0d9b5"  // Light squares (cream/tan)
    property color darkSquare: "#b58863"   // Dark squares (brown)
    property color highlightSquare: "#abebc680" // "#bbcc44"  // Square highlight color
    property color possibleMoveIndicator: "#82e0ab80" // "#66bbcc44"
    
    color: darkBackground

    // Function to convert square name to coordinates
    function squareToCoordinates(square) {
        if (!square || square.length !== 2) return null;
        
        const col = square.charCodeAt(0) - 97; // 'a' is 97 in ASCII
        const row = 8 - parseInt(square.charAt(1));
        
        // Apply flipping for black player
        if (boardFlipped) {
            const flippedResult = { row: 7 - row, col: 7 - col };
            return flippedResult;
        }
        
        return { row: row, col: col };
    }
    
    // Function to convert coordinates to square name
    function coordinatesToSquare(row, col) {
        // Calculate actual algebraic notation
        // When the board is flipped, we need to convert coordinates differently
        let file, rank;
        
        if (boardFlipped) {
            // We're already flipping row and col in the Rectangle properties
            // so here we just do a regular conversion
            file = String.fromCharCode(97 + col);
            rank = 8 - row;
        } else {
            // Regular board
            file = String.fromCharCode(97 + col);
            rank = 8 - row;
        }
        
        const result = `${file}${rank}`;
        return result;
    }
    
    // Helper function to get piece image source based on piece name
    function getPieceImage(piece) {
        if (!piece) return "";
        return "../assets/pieces/" + piece + ".png";
    }
    
    // Check if a position is in the possible moves list
    function isValidMove(row, col) {
        const square = coordinatesToSquare(row, col);
        return possibleMoves.includes(square);
    }
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15
        
        // Left side - Chess Board
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.6
            Layout.minimumWidth: 400
            color: darkCard
            radius: 10
            border.color: "#444444"
            border.width: 1
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 12
                
                // Header with game status
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: {
                            if (!gameStarted) return "Waiting for opponent..."
                            return isMyTurn ? "Your turn" : "Opponent's turn"
                        }
                        font.pixelSize: 20
                        font.bold: true
                        color: darkText
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Rectangle {
                        width: 10
                        height: 10
                        radius: 5
                        color: "#4caf50"
                    }
                    
                    Text {
                        text: "Live"
                        font.pixelSize: 14
                        color: darkSecondaryText
                        leftPadding: 5
                    }
                }
                
                // Chess Board Container with labels
                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    
                    // Container for board + labels
                    Item {
                        id: boardContainer
                        anchors.centerIn: parent
                        
                        // Calculate sizes based on available space
                        property int availableSize: Math.min(parent.width, parent.height) 
                        property int boardSize: availableSize - (labelSize * 2)
                        
                        width: boardSize + (labelSize * 2)
                        height: boardSize + (labelSize * 2)
                        
                        // Row labels (numbers 8-1) 
                        Column {
                            x: 0
                            y: labelSize
                            width: boardContainer.labelSize
                            height: boardContainer.boardSize
                            
                            Repeater {
                                model: 8
                                
                                Rectangle {
                                    width: boardContainer.labelSize
                                    height: boardContainer.boardSize / 8
                                    color: "transparent"
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: boardFlipped ? (index + 1) : (8 - index)
                                        color: darkText
                                        font.pixelSize: boardContainer.labelSize * 0.6
                                    }
                                }
                            }
                        }
                        
                        // Chess Board 
                        Grid {
                            id: chessboard
                            rows: 8
                            columns: 8
                            anchors {
                                left: parent.left
                                leftMargin: labelSize
                                top: parent.top
                                topMargin: labelSize
                            }
                            
                            property int cellSize: boardContainer.boardSize / 8
                            width: cellSize * 8
                            height: cellSize * 8
                            
                            property alias repeater: boardRepeater

                            Repeater {
                                id: boardRepeater
                                model: 64
                                
                                Rectangle {
                                    // Inverser le calcul des coordonnées pour le joueur noir
                                    property int row: boardFlipped ? (7 - Math.floor(index / 8)) : Math.floor(index / 8)
                                    property int col: boardFlipped ? (7 - (index % 8)) : (index % 8)
                                    property string square: coordinatesToSquare(row, col)
                                    property bool isSelected: square === selectedSquare
                                    property bool isPossibleMove: isValidMove(row, col)
                                    
                                    width: chessboard.cellSize
                                    height: chessboard.cellSize
                                    
                                    // Square coloring based on selection state
                                    color: isSelected ? highlightSquare : 
                                           isPossibleMove ? possibleMoveIndicator :
                                           (row + col) % 2 === 0 ? lightSquare : darkSquare
                                    
                                    Image {
                                        id: pieceImage
                                        anchors.fill: parent
                                        anchors.margins: parent.width * 0.05
                                        source: {
                                            if (!backend || !backend.chessGame || !backend.chessGame.piece_positions) {
                                                return ""
                                            }
                                            const positions = backend.chessGame.piece_positions;
                                            
                                            // Get the actual algebraic notation for this square
                                            const actualSquareName = square;
                                            const piece = positions.find(p => p.square === actualSquareName);
                                            
                                            if (piece) {
                                                return getPieceImage(piece.piece);
                                            }
                                            return "";
                                        }
                                        fillMode: Image.PreserveAspectFit
                                        visible: source !== ""
                                    }
                                    
                                    // Add debug text overlay to show square names for debugging
                                    Text {
                                        anchors.centerIn: parent
                                        text: square
                                        color: "red"
                                        font.pixelSize: 10
                                        visible: false // Set to true to debug square names
                                    }
                                    
                                    // Mouse area for piece selection and movement
                                    MouseArea {
                                        anchors.fill: parent
                                        enabled: gameStarted && isMyTurn
                                        onClicked: {
                                            // First check if the backend and chessGame are available
                                            if (!backend || !backend.chessGame) {
                                                console.error("Backend or chessGame not available")
                                                return;
                                            }
                                            
                                            // Ensure is_valid_move_source exists
                                            if (typeof backend.chessGame.is_valid_move_source !== "function") {
                                                console.error("is_valid_move_source is not a function")
                                                return;
                                            }
                                            
                                            if (selectedSquare && isPossibleMove) {
                                                backend.makeMove(selectedSquare, square);
                                                selectedSquare = "";
                                                possibleMoves = [];
                                            } 
                                            else if (backend.chessGame.is_valid_move_source(square)) {
                                                selectedSquare = square;
                                                possibleMoves = backend.chessGame.get_legal_destinations(square);
                                            } 
                                            else {
                                                selectedSquare = "";
                                                possibleMoves = [];
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Column labels (letters a-h)
                        Row {
                            // Fix the x and y properties by using literals instead of possibly undefined values
                            x: labelSize
                            y: labelSize + boardContainer.boardSize
                            width: boardContainer.boardSize
                            height: labelSize
                            
                            Repeater {
                                model: 8
                                
                                Text {
                                    width: boardContainer.boardSize / 8
                                    height: boardContainer.labelSize
                                    // Inverser les lettres pour le joueur noir
                                    text: String.fromCharCode(boardFlipped ? 104 - index : 97 + index)
                                    color: darkText
                                    font.pixelSize: boardContainer.labelSize * 0.6
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }
                    }
                }
                
                // Game controls
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    
                    Button {
                        text: "Return to Menu"
                        background: Rectangle {
                            color: darkSurface
                            radius: 6
                            border.color: darkAccent
                            border.width: 1
                        }
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            color: darkText
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            backend.cancelMatchmaking();
                            let sv = findStackView();
                            if (sv) {
                                sv.pop();
                            }
                        }
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Button {
                        text: "New Game"
                        background: Rectangle {
                            color: darkAccent
                            radius: 6
                        }
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            color: darkText
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            backend.play();
                            selectedSquare = "";
                            possibleMoves = [];
                        }
                    }
                    
                    Button {
                        text: "Draw"
                        background: Rectangle {
                            color: "#616161"
                            radius: 6
                        }
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            color: darkText
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: console.log("Draw requested")
                    }
                    
                    Button {
                        text: "Resign"
                        background: Rectangle {
                            color: "#7d0000"
                            radius: 6
                        }
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            color: darkText
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            console.log("Resign clicked")
                        }
                    }
                }
            }
        }
        
        // Right side - Game Info Panel
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: darkCard
            radius: 10
            border.color: "#444444"
            border.width: 1
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 12
                
                // Tabs for chat and game info
                TabBar {
                    id: tabBar
                    Layout.fillWidth: true
                    background: Rectangle {
                        color: darkSurface
                        radius: 5
                    }
                    
                    TabButton {
                        text: "Chat"
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 16
                            color: tabBar.currentIndex === 0 ? darkAccent : darkSecondaryText
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        background: Rectangle {
                            color: "transparent"
                            border.color: tabBar.currentIndex === 0 ? darkAccent : "transparent"
                            border.width: tabBar.currentIndex === 0 ? 2 : 0
                            radius: 5
                        }
                    }
                    
                    TabButton {
                        text: "Game Info"
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 16
                            color: tabBar.currentIndex === 1 ? darkAccent : darkSecondaryText
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        background: Rectangle {
                            color: "transparent"
                            border.color: tabBar.currentIndex === 1 ? darkAccent : "transparent"
                            border.width: tabBar.currentIndex === 1 ? 2 : 0
                            radius: 5
                        }
                    }
                }
                
                // Content area
                StackLayout {
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    currentIndex: tabBar.currentIndex
                    
                    // Chat tab
                    Item {
                        Rectangle {
                            anchors.fill: parent
                            color: Qt.rgba(0, 0, 0, 0.2)
                            radius: 8
                            
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 10
                                spacing: 10
                                
                                // Chat messages display area
                                ListView {
                                    id: chatView
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true
                                    clip: true
                                    model: ListModel {
                                        ListElement { sender: "System"; message: "Welcome to the game chat!"; timestamp: "12:00" }
                                        ListElement { sender: "System"; message: "You can chat with your opponent here."; timestamp: "12:01" }
                                    }
                                    
                                    delegate: Rectangle {
                                        width: chatView.width
                                        height: messageLayout.height + 12
                                        color: "transparent"
                                        
                                        ColumnLayout {
                                            id: messageLayout
                                            width: parent.width - 16
                                            x: 8
                                            y: 6
                                            spacing: 4
                                            
                                            RowLayout {
                                                Layout.fillWidth: true
                                                
                                                Text {
                                                    text: sender
                                                    font.bold: true
                                                    font.pixelSize: 14
                                                    color: darkText
                                                }
                                                
                                                Item { Layout.fillWidth: true }
                                                
                                                Text {
                                                    text: timestamp
                                                    font.pixelSize: 12
                                                    color: darkSecondaryText
                                                }
                                            }
                                            
                                            Text {
                                                text: message
                                                Layout.fillWidth: true
                                                wrapMode: Text.WordWrap
                                                font.pixelSize: 14
                                                color: darkText
                                            }
                                            
                                            Rectangle {
                                                Layout.fillWidth: true
                                                height: 1
                                                color: "#444444"
                                                visible: index < chatView.count - 1
                                                opacity: 0.5
                                            }
                                        }
                                    }
                                    
                                    ScrollBar.vertical: ScrollBar {
                                        active: true
                                    }
                                }
                                
                                // Chat input area
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 40
                                    color: Qt.rgba(0, 0, 0, 0.3)
                                    radius: 20  // Rounded input field
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.leftMargin: 15
                                        anchors.rightMargin: 5
                                        spacing: 10
                                        
                                        TextField {
                                            id: chatInput
                                            Layout.fillWidth: true
                                            placeholderText: "Type your message..."
                                            placeholderTextColor: "#888888"
                                            color: darkText
                                            background: Item {}  // Remove default background
                                            verticalAlignment: TextInput.AlignVCenter
                                            
                                            onAccepted: {
                                                if (text.trim() !== "") {
                                                    chatView.model.append({
                                                        "sender": backend.user.username || "You",
                                                        "message": text.trim(), 
                                                        "timestamp": new Date().toLocaleTimeString(Qt.locale(), "hh:mm")
                                                    });
                                                    text = "";
                                                }
                                            }
                                        }
                                        
                                        RoundButton {
                                            text: ">"  // Right angle bracket as send icon
                                            font.pixelSize: 18
                                            font.bold: true
                                            Layout.preferredHeight: 30
                                            Layout.preferredWidth: 30
                                            background: Rectangle {
                                                radius: 15
                                                color: darkAccent
                                            }
                                            contentItem: Text {
                                                text: parent.text
                                                font: parent.font
                                                color: darkText
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            onClicked: chatInput.accepted()
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    // Game info tab - now using WebSocket Chess Game
                    Item {
                        Rectangle {
                            anchors.fill: parent
                            color: Qt.rgba(0, 0, 0, 0.2)
                            radius: 8
                            
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 15
                                spacing: 15
                                
                                // Player info boxes
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 80
                                    color: darkSurface
                                    radius: 8
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 10
                                        spacing: 10
                                        
                                        Rectangle {
                                            width: 60
                                            height: 60
                                            radius: 30
                                            color: darkAccent
                                            
                                            Text {
                                                anchors.centerIn: parent
                                                text: backend.chessGame.player_color === "white" ? "W" : "B"
                                                color: darkText
                                                font.pixelSize: 24
                                                font.bold: true
                                            }
                                        }
                                        
                                        ColumnLayout {
                                            Layout.fillWidth: true
                                            spacing: 2
                                            
                                            Text {
                                                text: backend.user.username || "Player 1"
                                                font.pixelSize: 16
                                                font.bold: true
                                                color: darkText
                                            }
                                            
                                            Text {
                                                text: "ELO: " + (backend.user.elo || "1500")
                                                font.pixelSize: 14
                                                color: darkSecondaryText
                                            }
                                        }
                                        
                                        Text {
                                            text: "10:00"
                                            font.pixelSize: 20
                                            font.family: "monospace"
                                            color: darkText
                                        }
                                    }
                                }
                                
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 80
                                    color: darkSurface
                                    radius: 8
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 10
                                        spacing: 10
                                        
                                        Rectangle {
                                            width: 60
                                            height: 60
                                            radius: 30
                                            color: "#555555"
                                            
                                            Text {
                                                anchors.centerIn: parent
                                                text: backend.chessGame.player_color === "white" ? "B" : "W"
                                                color: darkText
                                                font.pixelSize: 24
                                                font.bold: true
                                            }
                                        }
                                        
                                        ColumnLayout {
                                            Layout.fillWidth: true
                                            spacing: 2
                                            
                                            Text {
                                                text: "Opponent"
                                                font.pixelSize: 16
                                                font.bold: true
                                                color: darkText
                                            }
                                            
                                            Text {
                                                text: "ELO: 1520"
                                                font.pixelSize: 14
                                                color: darkSecondaryText
                                            }
                                        }
                                        
                                        Text {
                                            text: "10:00"
                                            font.pixelSize: 20
                                            font.family: "monospace"
                                            color: darkText
                                        }
                                    }
                                }
                                
                                // Captured pieces for both players
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 40
                                    color: darkSurface
                                    radius: 8
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 8
                                        spacing: 5
                                        
                                        Text {
                                            text: boardFlipped ? "White captured: " : "Black captured: "
                                            color: darkSecondaryText
                                            font.pixelSize: 14
                                        }
                                        
                                        Row {
                                            spacing: 4
                                            Layout.fillWidth: true
                                            
                                            // This will be populated when you implement getCapturedPieces
                                        }
                                    }
                                }
                                
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 40
                                    color: darkSurface
                                    radius: 8
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 8
                                        spacing: 5
                                        
                                        Text {
                                            text: boardFlipped ? "Black captured: " : "White captured: "
                                            color: darkSecondaryText
                                            font.pixelSize: 14
                                        }
                                        
                                        Row {
                                            spacing: 4
                                            Layout.fillWidth: true
                                            
                                            // This will be populated when you implement getCapturedPieces
                                        }
                                    }
                                }
                                
                                // Game moves
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    color: darkSurface
                                    radius: 8
                                    
                                    ColumnLayout {
                                        anchors.fill: parent
                                        anchors.margins: 10
                                        spacing: 5
                                        
                                        Text {
                                            text: "Moves"
                                            font.pixelSize: 16
                                            font.bold: true
                                            color: darkText
                                        }
                                        
                                        ListView {
                                            Layout.fillWidth: true
                                            Layout.fillHeight: true
                                            clip: true
                                            model: {
                                                // When you implement the history feature
                                                return [];
                                            }
                                            
                                            delegate: RowLayout {
                                                width: parent.width
                                                height: 30
                                                
                                                Text {
                                                    text: modelData.moveNumber + "."
                                                    width: 30
                                                    color: darkSecondaryText
                                                    font.pixelSize: 14
                                                }
                                                
                                                Text {
                                                    text: modelData.white
                                                    Layout.preferredWidth: parent.width / 2 - 30
                                                    color: darkText
                                                    font.pixelSize: 14
                                                    font.bold: true
                                                }
                                                
                                                Text {
                                                    text: modelData.black
                                                    Layout.fillWidth: true
                                                    color: darkText
                                                    font.pixelSize: 14
                                                    font.bold: true
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}