import random

from stockfish import Stockfish
import chess

stockfish = Stockfish("/opt/homebrew/Cellar/stockfish/13/bin/stockfish")

# print(stockfish.get_board_visual())
# print(stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"))
# print(stockfish.get_board_visual())
# print(stockfish.get_best_move())
# print(stockfish.get_evaluation())
# print(stockfish.set_depth(15))
# print(stockfish.get_evaluation())


def evaluation_delta(initial_position: str, depth: int):
    stockfish.set_depth(depth) # set engine depth
    board = chess.Board(fen=initial_position)
    stockfish.set_fen_position(board.fen())
    initial_evaluation = stockfish.get_evaluation()['value']
    for i in range(depth + 1):
        best_move = stockfish.get_best_move()
        board.push(chess.Move.from_uci(best_move))
        stockfish.set_fen_position(board.fen())
    
    final_position = board.fen()
    final_evaluation = stockfish.get_evaluation()['value']
    return (initial_position, initial_evaluation), (final_position, final_evaluation)


def generate_random_position():
    while True:
        board = chess.Board()
        end_game = False
        for i in range(random.randint(10, 100)):
            move = random.choice(list(board.legal_moves))
            board.push(move)
            if board.is_game_over():
                end_game = True
                break
        if not end_game:
            yield board.fen()


if __name__ == "__main__":
    # Set initial position
    # print(stockfish.get_parameters())
    # STARTING_FEN = chess.STARTING_FEN # "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
    # board = chess.Board(fen=STARTING_FEN)
    # depth = 15
    # stockfish.set_depth(depth)

    store_high_deltas = list()

    for initial_position in generate_random_position():
        initial, final = evaluation_delta(initial_position, 7)
        initial_position, initial_evaluation = initial
        final_position, final_evaluation = final

        print(f"Absolute delta: {abs(final_evaluation-initial_evaluation)}")
        if abs(final_evaluation-initial_evaluation) > 600 and (final_evaluation * initial_evaluation) < 0:
            store_high_deltas.append((initial, final))
            print(f"#### INITIAL POSITION: eval = {initial_evaluation}, fen = {initial_position}")
            stockfish.set_fen_position(initial_position)
            print(stockfish.get_board_visual())
            print(f"#### FINAL POSITION: eval = {final_evaluation}, fen = {final_position}")
            stockfish.set_fen_position(final_position)
            print(stockfish.get_board_visual())




