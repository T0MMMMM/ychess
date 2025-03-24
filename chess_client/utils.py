import os
import requests
from pathlib import Path

def download_chess_pieces():
    """Download chess piece images in chess.com style"""
    
    # Create assets directory if it doesn't exist
    assets_dir = Path(__file__).parent / "assets" / "pieces"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Chess.com style piece URLs
    piece_urls = {
        # White pieces
        "w_pawn": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wp.png",
        "w_rook": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wr.png",
        "w_knight": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wn.png",
        "w_bishop": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wb.png",
        "w_queen": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wq.png",
        "w_king": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wk.png",
        
        # Black pieces
        "b_pawn": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bp.png",
        "b_rook": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/br.png",
        "b_knight": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bn.png",
        "b_bishop": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bb.png",
        "b_queen": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bq.png",
        "b_king": "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/bk.png"
    }
    
    # Download each piece
    for piece_name, url in piece_urls.items():
        output_path = assets_dir / f"{piece_name}.png"
        
        # Skip if file already exists
        if output_path.exists():
            print(f"Skipping {piece_name}, file already exists")
            continue
        
        print(f"Downloading {piece_name}...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {piece_name}")
            else:
                print(f"Failed to download {piece_name}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error downloading {piece_name}: {e}")
    
    print("Chess piece download complete!")

def ensure_chess_pieces_exist():
    """Make sure chess piece images are available"""
    assets_dir = Path(__file__).parent / "assets" / "pieces"
    assets_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
    
    # Vérification et création du dossier assets/pieces s'il n'existe pas
    if not assets_dir.exists() or not (assets_dir / "w_king.png").exists():
        print("Chess piece images not found. Downloading...")
        download_chess_pieces()
        
        # Vérification après téléchargement
        if not (assets_dir / "w_king.png").exists():
            print("Error: Failed to download chess pieces")
            sys.exit(1)
    else:
        print("Chess piece images found")
