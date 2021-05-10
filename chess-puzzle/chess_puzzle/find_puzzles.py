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


def evaluation_delta(initial_position: str, evaluation_depth: int = 22, steps_to_compare: int = 4):
    stockfish.set_depth(evaluation_depth) # set engine depth
    board = chess.Board(fen=initial_position)
    stockfish.set_fen_position(board.fen())
    initial_evaluation = stockfish.get_evaluation()

    moves = list()
    for i in range(steps_to_compare):
        best_move = stockfish.get_best_move()
        moves.append(best_move)
        # best_move = stockfish.get_best_move_time(time_to_think)
        board.push(chess.Move.from_uci(best_move))
        stockfish.set_fen_position(board.fen())
        if board.is_game_over():
            break

    final_position = board.fen()
    final_evaluation = stockfish.get_evaluation()
    return (initial_position, initial_evaluation), (final_position, final_evaluation), moves


def generate_random_position():
    while True:
        board = chess.Board()
        end_game = False
        for i in range(random.randint(10, 200)):
            move = random.choice(list(board.legal_moves))
            board.push(move)
            if board.is_game_over():
                end_game = True
                break
        if not end_game:
            yield board.fen()


if __name__ == "__main__":
    import sys

    store_high_deltas = list()

    for initial_position in generate_random_position():
        initial, final, moves = evaluation_delta(initial_position, int(sys.argv[1]), int(sys.argv[2]))
        initial_position, initial_evaluation = initial
        final_position, final_evaluation = final

        if initial_evaluation['type']=="cp" and final_evaluation['type']=="cp":
            print(f"Absolute delta: {abs(final_evaluation['value']-initial_evaluation['value'])}")
            if abs(final_evaluation['value']-initial_evaluation['value']) > 400 and (final_evaluation['value'] * initial_evaluation['value']) < 0:
                store_high_deltas.append((initial, final))
                print(f"#### INITIAL POSITION: eval = {initial_evaluation['value']}, fen = {initial_position}")
                stockfish.set_fen_position(initial_position)
                print(stockfish.get_board_visual())
                print(f"#### FINAL POSITION: eval = {final_evaluation['value']}, fen = {final_position}")
                stockfish.set_fen_position(final_position)
                print(stockfish.get_board_visual())
                print(f"#### Moves list: {moves}")

        elif initial_evaluation['type']=="cp" and final_evaluation['type']=="mate":
            pass
        else:
            pass




