import chess
import random

'''
	Your Code Will Come Here
'''

# this function should always be named as ai_play and
# this function's return value is used as AI's move so it will AI's your final decision.
# You can add as many function as you want to above.
# At each turn you will get a board to ai_play and calculate best move and return it.
def ai_play(board):
	plays = []

	for play in board.legal_moves:
		plays.append(str(play))

	return plays[random.randint(0, len(plays)-1)] # here I only return random legal move to show an example



