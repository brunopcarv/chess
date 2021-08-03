import random
from typing import Dict, List
import copy

from stockfish import Stockfish
import chess



def evaluation_from_board(board: chess.Board, evaluation_depth: int = 22) -> Dict:
    board_fen = board.fen()
    stockfish = Stockfish("/opt/homebrew/Cellar/stockfish/13/bin/stockfish")
    stockfish.set_depth(evaluation_depth) # set engine depth
    stockfish.set_fen_position(board_fen)
    return stockfish.get_evaluation()


def find_correct_moves(board: chess.Board, evaluation_depth: int = 22, eval_range: int = 300) -> List:
    """Moves whose evaluation is identical to the current one are considered correct.
       Return list of "correct" moves.
    """

    moves_and_evaluations = list()
    for move in board.legal_moves:
        _board = copy.deepcopy(board)
        _board.push(move)
        if not _board.is_game_over():
            moves_and_evaluations.append((move, evaluation_from_board(_board, evaluation_depth=evaluation_depth-1)))
        else:
            pass
    
    current_evaluation = evaluation_from_board(board, evaluation_depth=evaluation_depth)
    if current_evaluation['type']=="cp":
        if current_evaluation['value'] >= 0:
            correct_moves = [(m, e) for (m, e) in moves_and_evaluations if (e['type']=="cp" and e['value'] >= current_evaluation['value'] - eval_range)]
        else:
            correct_moves = [(m, e) for (m, e) in moves_and_evaluations if (e['type']=="cp" and e['value'] <= current_evaluation['value'] + eval_range)]
    else:
        correct_moves = [(m, e) for (m, e) in moves_and_evaluations if (e['type']=="mate" and e['value']==current_evaluation['value']-1)]
    return correct_moves


def generate_random_advantage_position(evaluation_depth: int):
    stockfish = Stockfish("/opt/homebrew/Cellar/stockfish/13/bin/stockfish")
    stockfish.set_depth(evaluation_depth) # set engine depth
    while True:
        board = chess.Board()
        end_game = False
        for i in range(random.randint(10, 200)):
            move = random.choice(list(board.legal_moves))
            board.push(move)
            if board.is_game_over():
                end_game = True
                print("Final position")
                break

        if not end_game:
            board_fen = board.fen()
            stockfish.set_fen_position(board_fen)
            position_evaluation = stockfish.get_evaluation()
            print(f"Position_evaluation: {position_evaluation}, fen = {board_fen}")
            
            if position_evaluation['type']=='cp' and abs(position_evaluation["value"]) < 300 and abs(position_evaluation["value"]) > 1000: # rule out when no big advantage
                print(f"position_evaluation: {position_evaluation}. Passing: rule out when no big advantage")
                pass
            elif position_evaluation['type']=='mate' and position_evaluation['value'] <= 1: # rule out mate in 1
                print(f"position_evaluation: {position_evaluation}. Passing: rule out mate in 1")
                pass
            else:
                if board.turn == chess.WHITE and position_evaluation["value"] <= 0: # not an advantage white
                    print(f"Turn: {board.turn}")
                    print(f"position_evaluation: {position_evaluation}. Passing: not an advantage for white")
                    pass
                elif board.turn == chess.BLACK and position_evaluation["value"] >= 0: # not an advantage black
                    print(f"Turn: {board.turn}")
                    print(f"position_evaluation: {position_evaluation}. Passing: not an advantage for black")
                    pass
                else:
                    yield board, board_fen, position_evaluation


if __name__ == "__main__":
    EVAL_DEPTH = 33
    stockfish = Stockfish("/opt/homebrew/Cellar/stockfish/13/bin/stockfish")
    for board, board_fen, position_evaluation in generate_random_advantage_position(evaluation_depth=EVAL_DEPTH):

        print(f"##### Initial eval = {position_evaluation}, fen = {board_fen}")

        correct_moves = find_correct_moves(board, evaluation_depth=EVAL_DEPTH)
        if len(correct_moves) in (1, 2,):
            stockfish.set_fen_position(board_fen)
            print(stockfish.get_board_visual())
            print(f"Correct moves: {correct_moves}")
