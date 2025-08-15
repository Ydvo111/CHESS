import pygame
import chess
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (245, 245, 220)
BLACK = (139, 69, 19)
HIGHLIGHT = (186, 202, 68)

# Load piece images
pieces = ['r','n','b','q','k','p']
IMAGES = {}
assets_path = os.path.join(os.path.dirname(__file__), 'assets')

for piece in pieces:
    for color in ['w', 'b']:
        filename = f'{color}{piece}.png'
        filepath = os.path.join(assets_path, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Missing image file: {filepath}")
        IMAGES[color + piece] = pygame.transform.scale(
            pygame.image.load(filepath), (SQUARE_SIZE, SQUARE_SIZE)
        )

# Chess board setup
board = chess.Board()

# Pygame window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Python Chess')

# Draw board and pieces
def draw_board(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            square = chess.square(col, 7-row)  # chess library coordinates
            piece = board.piece_at(square)
            if piece:
                key = ('w' if piece.color else 'b') + piece.symbol().lower()
                if key in IMAGES:
                    win.blit(IMAGES[key], (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Main loop
def main():
    run = True
    selected_square = None
    possible_moves = []
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        draw_board(WIN, board)

        # Highlight possible moves
        for move in possible_moves:
            row = 7 - chess.square_rank(move.to_square)
            col = chess.square_file(move.to_square)
            pygame.draw.rect(WIN, HIGHLIGHT, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                square = chess.square(col, 7-row)

                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == board.turn:
                        selected_square = square
                        possible_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                else:
                    move = chess.Move(selected_square, square)
                    # Handle promotion to queen automatically if pawn reaches last rank
                    if board.piece_at(selected_square).piece_type == chess.PAWN and (chess.square_rank(square) in [0, 7]):
                        move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                    if move in board.legal_moves:
                        board.push(move)

                        # Check for checkmate
                        if board.is_checkmate():
                            winner = "White" if board.turn == chess.BLACK else "Black"
                            font = pygame.font.SysFont(None, 60)
                            text = font.render(f"Checkmate! {winner} wins!", True, (255, 0, 0))
                            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
                            pygame.display.update()

                            # Wait until player closes the window
                            waiting = True
                            while waiting:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        waiting = False
                            run = False

                        selected_square = None
                        possible_moves = []

    pygame.quit()

if __name__ == '__main__':
    main()