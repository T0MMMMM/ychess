import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ChessTypes 1.0

Rectangle {
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
    property color highlightSquare: "#bbcc44"  // Square highlight color
    property color possibleMoveIndicator: "#66bbcc44"
    
    // Track selections
    property int selectedRow: -1
    property int selectedCol: -1
    property var possibleMoves: []
    
    color: darkBackground
    property var stackView
    
    // Helper function to get piece image source based on piece symbol
    function getPieceImage(symbol) {
        if (!symbol) return "";
        
        const color = symbol === symbol.toLowerCase() ? "b" : "w";
        let pieceName;
        
        switch(symbol.toLowerCase()) {
            case "p": pieceName = "pawn"; break;
            case "r": pieceName = "rook"; break;
            case "n": pieceName = "knight"; break;
            case "b": pieceName = "bishop"; break;
            case "q": pieceName = "queen"; break;
            case "k": pieceName = "king"; break;
            default: return "";
        }
        
        return "assets/pieces/" + color + "_" + pieceName + ".png";
    }
    
    // Check if a position is in the possible moves list
    function isValidMove(row, col) {
        for (let i = 0; i < possibleMoves.length; i++) {
            if (possibleMoves[i][0] === row && possibleMoves[i][1] === col) {
                return true;
            }
        }
        return false;
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
                        text: "Game in Progress - " + backend.chessGame.currentPlayer + "'s move"
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
                        property int labelSize: 24
                        
                        width: boardSize + (labelSize * 2)
                        height: boardSize + (labelSize * 2)
                        
                        // Row labels (numbers 8-1) - Fix the centering
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
                                        anchors.centerIn: parent  // This centers both horizontally and vertically
                                        text: 8 - index
                                        color: darkText
                                        font.pixelSize: boardContainer.labelSize * 0.6
                                    }
                                }
                            }
                        }
                        
                        // Chess Board using Python model
                        Grid {
                            id: chessboard
                            rows: 8
                            columns: 8
                            x: boardContainer.labelSize
                            y: boardContainer.labelSize
                            
                            property int cellSize: boardContainer.boardSize / 8
                            width: cellSize * 8
                            height: cellSize * 8
                            
                            Repeater {
                                model: 64
                                
                                Rectangle {
                                    property int row: Math.floor(index / 8)
                                    property int col: index % 8
                                    property bool isSelected: row === selectedRow && col === selectedCol
                                    property bool isPossibleMove: isValidMove(row, col)
                                    
                                    width: chessboard.cellSize
                                    height: chessboard.cellSize
                                    
                                    // Square coloring based on selection state
                                    color: isSelected ? highlightSquare : 
                                          isPossibleMove ? possibleMoveIndicator :
                                          (row + col) % 2 === 0 ? lightSquare : darkSquare
                                    
                                    // Piece image from Python model
                                    Image {
                                        id: pieceImage
                                        anchors.fill: parent
                                        anchors.margins: parent.width * 0.05
                                        source: {
                                            // Get piece symbol from Python model
                                            const board = backend.chessGame.board;
                                            const symbol = board[row][col];
                                            return getPieceImage(symbol);
                                        }
                                        fillMode: Image.PreserveAspectFit
                                        visible: source !== ""
                                    }
                                    
                                    // Possible move indicator
                                    Rectangle {
                                        visible: isPossibleMove && !pieceImage.visible
                                        anchors.centerIn: parent
                                        width: parent.width * 0.3
                                        height: width
                                        radius: width / 2
                                        color: possibleMoveIndicator
                                        opacity: 0.8
                                    }
                                    
                                    // Mouse area for piece selection and movement
                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                            // If we have a selected piece and this is a valid move
                                            if (selectedRow !== -1 && selectedCol !== -1 && isPossibleMove) {
                                                // Move the piece using Python model
                                                backend.chessGame.movePiece(row, col);
                                                selectedRow = -1;
                                                selectedCol = -1;
                                                possibleMoves = [];
                                            } 
                                            // If we're selecting a piece
                                            else {
                                                const board = backend.chessGame.board;
                                                if (board[row][col]) {
                                                    // Check if selection is valid (user can only select their pieces)
                                                    if (backend.chessGame.selectPiece(row, col)) {
                                                        selectedRow = row;
                                                        selectedCol = col;
                                                        // Get possible moves from Python
                                                        possibleMoves = backend.chessGame.getPossibleMoves(row, col);
                                                    }
                                                } else {
                                                    // Clicking on empty square outside of possible moves
                                                    selectedRow = -1;
                                                    selectedCol = -1;
                                                    possibleMoves = [];
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Column labels (letters a-h)
                        Row {
                            x: boardContainer.labelSize
                            y: boardContainer.labelSize + boardContainer.boardSize
                            width: boardContainer.boardSize
                            height: boardContainer.labelSize
                            
                            Repeater {
                                model: 8
                                
                                Text {
                                    width: boardContainer.boardSize / 8
                                    height: boardContainer.labelSize
                                    text: String.fromCharCode(97 + index)
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
                        onClicked: stackView.pop()
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
                            backend.chessGame.resetGame();
                            selectedRow = -1;
                            selectedCol = -1;
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
                        onClicked: console.log("Resign clicked")
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
                                            text: "⟩"  // Right angle bracket as send icon
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
                    
                    // Game info tab - now using the Python model
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
                                                text: "W"
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
                                                text: "B"
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
                                
                                // White captured pieces
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
                                            text: "Black captured: "
                                            color: darkSecondaryText
                                            font.pixelSize: 14
                                        }
                                        
                                        Row {
                                            spacing: 4
                                            Layout.fillWidth: true
                                            
                                            Repeater {
                                                model: backend.chessGame.getCapturedPieces("white")  // Use the helper method
                                                
                                                Text {
                                                    text: {
                                                        // Map piece notations to Unicode symbols
                                                        const symbols = {
                                                            "P": "♟", "p": "♟",
                                                            "R": "♜", "r": "♜",
                                                            "N": "♞", "n": "♞",
                                                            "B": "♝", "b": "♝",
                                                            "Q": "♛", "q": "♛",
                                                            "K": "♚", "k": "♚"
                                                        };
                                                        return symbols[modelData] || modelData;
                                                    }
                                                    color: "#bbbbbb"  // Gray for black pieces captured by white
                                                    font.pixelSize: 20
                                                }
                                            }
                                        }
                                    }
                                }
                                
                                // Black captured pieces
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
                                            text: "White captured: "
                                            color: darkSecondaryText
                                            font.pixelSize: 14
                                        }
                                        
                                        Row {
                                            spacing: 4
                                            Layout.fillWidth: true
                                            
                                            Repeater {
                                                model: backend.chessGame.getCapturedPieces("black")  // Use the helper method
                                                
                                                Text {
                                                    text: {
                                                        // Map piece notations to Unicode symbols
                                                        const symbols = {
                                                            "P": "♙", "p": "♙",
                                                            "R": "♖", "r": "♖",
                                                            "N": "♘", "n": "♘",
                                                            "B": "♗", "b": "♗",
                                                            "Q": "♕", "q": "♕",
                                                            "K": "♔", "k": "♔"
                                                        };
                                                        return symbols[modelData] || modelData;
                                                    }
                                                    color: darkText
                                                    font.pixelSize: 20
                                                }
                                            }
                                        }
                                    }
                                }
                                
                                // Game moves from Python model
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
                                                // Group moves into pairs for display
                                                const moves = backend.chessGame.moves;
                                                const result = [];
                                                for (let i = 0; i < moves.length; i += 2) {
                                                    result.push({
                                                        moveNumber: Math.floor(i/2) + 1,
                                                        white: moves[i] || "",
                                                        black: i+1 < moves.length ? moves[i+1] : ""
                                                    });
                                                }
                                                return result;
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
    
    // Update when the model changes
    Connections {
        target: backend.chessGame
        function onBoardChanged() {
            // Reset selection when board changes
            selectedRow = -1;
            selectedCol = -1;
            possibleMoves = [];
        }
    }
}
