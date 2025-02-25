import chess
import chess.svg


KNIGHT_SQUARES = [
    -10, -8, -6, -6, -6, -6, -8, -10,
    -8, -4, 0, 0, 0, 0, -4, -8,
    -6, 0, 2, 3, 3, 2, 0, -6,
    -6, 1, 3, 4, 4, 3, 1, -6,
    -6, 0, 3, 4, 4, 3, 0, -6,
    -6, 1, 2, 3, 3, 2, 1, -6,
    -8, -4, 0, 1, 1, 0, -4, -8,
    -10, -8, -6, -6, -6, -6, -8, -10
]

BISHOP_SQUARES = [
    -6, -4, -4, -4, -4, -4, -4, -6,
    -4, 0, 0, 0, 0, 0, 0, -4,
    -4, 0, 2, 4, 4, 2, 0, -4,
    -4, 1, 2, 4, 4, 2, 1, -4,
    -4, 0, 4, 4, 4, 4, 0, -4,
    -4, 4, 4, 4, 4, 4, 4, -4,
    -4, 2, 0, 0, 0, 0, 2, -4,
    -6, -4, -4, -4, -4, -4, -4, -6
]

ROOK_SQUARES = [
    0, 0, 0, 1, 1, 0, 0, 0,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0, 0, 0, 0, 0, -1,
    1, 2, 2, 2, 2, 2, 2, 1,
    0, 0, 0, 0, 0, 0, 0, 0
]

QUEEN_SQUARES = [
    -4, -2, -2, -1, -1, -2, -2, -4,
    -2, 0, 0, 0, 0, 0, 0, -2,
    -2, 0, 1, 1, 1, 1, 0, -2,
    -1, 0, 1, 1, 1, 1, 0, -1,
    0, 0, 1, 1, 1, 1, 0, -1,
    -2, 1, 1, 1, 1, 1, 0, -2,
    -2, 0, 1, 0, 0, 0, 0, -2,
    -4, -2, -2, -1, -1, -2, -2, -4
]

def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    if piece.piece_type == chess.KNIGHT:
        return 3
    if piece.piece_type == chess.BISHOP:
        return 3
    if piece.piece_type == chess.ROOK:
        return 5
    if piece.piece_type == chess.QUEEN:
        return 9
    if piece.piece_type == chess.KING:
        return 0
    return 0

def rank_targets(board):
    move = board.peek()
    targeted = board.attacks(move.to_square)
    print(f'Move: {move}; Targeted squares:\n{targeted}')
    targets = [sq for sq in targeted if board.piece_at(sq) and board.piece_at(sq).color != board.turn]
    ranked_targets = targets.sort(key=lambda sq: piece_value(board.piece_at(sq)), reverse=True)
    print(f'Targets: {targets}')
    print(f'Ranked targets: {ranked_targets}')
    return ranked_targets

def score_by_material_and_position(board):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            allegiance = 1 if piece.color == chess.WHITE else -1
            score += (piece_value(piece) * allegiance)
            if piece.piece_type == chess.KNIGHT:
                score += (KNIGHT_SQUARES[square] * allegiance * .2)
            if piece.piece_type == chess.BISHOP:
                score += (BISHOP_SQUARES[square] * allegiance * .2)
            if piece.piece_type == chess.ROOK:
                score += (ROOK_SQUARES[square] * allegiance * .2)
            if piece.piece_type == chess.QUEEN:
                score += (QUEEN_SQUARES[square] * allegiance * .2)
    if board.is_checkmate():
        score += (9999 * -allegiance)

    if board.is_check():
        score += (1 * -allegiance)
    
    return score
    

def minimax(board, depth=4, alpha=-9999, beta=9999):
    if depth == 0 or board.is_game_over():
        best_move = [score_by_material_and_position(board), board.move_stack[-depth]]
        
        return best_move
    best_move = [alpha, None] if board.turn == chess.WHITE else [beta, None]
    if len(board.move_stack) > 0:
        best_move[1] = board.peek()
    if board.turn == chess.WHITE:
        for move in board.legal_moves:
            board.push(move)
            try_move = minimax(board, depth - 1, alpha, beta)
            if try_move[0] > best_move[0]:
                best_move = try_move
            alpha = max(alpha, best_move[0])
            board.pop()
            if beta <= alpha:
                return best_move
        return best_move
    else:
        for move in board.legal_moves:
            board.push(move)
            try_move = minimax(board, depth - 1, alpha, beta)
            if try_move[0] < best_move[0]:
                best_move = try_move
            beta = min(beta, best_move[0])
            board.pop()
            if beta <= alpha:
                return best_move
        return best_move

board = chess.Board()

while not board.is_game_over():
    print(board)
    print("Material score: ", score_by_material_and_position(board))
    num_moves = len(board.move_stack)
    while len(board.move_stack) == num_moves:
        if board.turn == chess.WHITE:
            move = minimax(board.copy(stack=False))
            print(f'Best move: {move[1]}')
            board.push(move[1])
        else:
            move = input("Enter move: ")
            try:
                board.push_uci(move)
            except chess.IllegalMoveError or ValueError:
                print(f'{move} is not a legal uci move on the board.')
            except:
                print(f'An error occurred while processing {move}.')
        svg_content = chess.svg.board(board)
        with open("/home/jocko/podman/www/chess_board.svg", "w") as file:
            file.write(svg_content)

print("Game over")
print("Final board:")
print(board)
print("Material score: ", score_by_material_and_position(board))
