############################################
#             Behold student!              #
# There is nothing to change here for you  #
# The script is carefully coded by experts #
############################################

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize
import chess
import os
from chess_ai import ai_play

piece_urls = {"r":"br.png", "b":"bb.png", "n":"bn.png", "k":"bk.png", "q":"bq.png", "p":"bp.png",
			  "R":"wr.png", "B":"wb.png", "N":"wn.png", "K":"wk.png", "Q":"wq.png", "P":"wp.png", "1":"blank"}

def get_piece(full_fen, index):
	my_fen = ""
	fen = full_fen.split(" ")[0]

	for char in fen:

		if char.isdigit():
			for i in range(int(char)):
				my_fen += "1"
		else:
			my_fen += char

	row = my_fen.split("/")[index//8]
	return  os.path.join(os.path.join(os.getcwd(), "icons"), piece_urls[row[index%8]])

def from_position_to_chess_move(position):
	move = ""

	if position % 8 == 0:
		move += "a"
	elif position % 8 == 1:
		move += "b"
	elif position % 8 == 2:
		move += "c"
	elif position % 8 == 3:
		move += "d"
	elif position % 8 == 4:
		move += "e"
	elif position % 8 == 5:
		move += "f"
	elif position % 8 == 6:
		move += "g"
	elif position % 8 == 7:
		move += "h"

	move += str(8 - (position // 8))

	return move

def update_board(board, buttons):
	for i in range(8):
		for j in range(8):
			if get_piece(board.fen(), (i * 8) + j) != "blank":
				buttons[i*8+j].setIcon(QIcon(get_piece(board.fen(), (i * 8) + j)))
			else:
				buttons[i*8+j].setIcon(QIcon())

class App(QWidget):

	def __init__(self, board):
		super().__init__()
		self.title = 'CENG461 Chess'
		self.left = 10
		self.top = 10
		self.width = 500
		self.height = 500
		self.board = board
		self.first_position = "none"
		self.second_position = "none"
		self.buttons = []
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		for i in range(8):
			for j in range(8):
				button = QPushButton('', self)
				button.move((j+1)*50, (i+1)*50)
				button.setObjectName('Button ' + str((i*8)+j))

				if get_piece(self.board.fen(), (i*8)+j) != "blank":
					button.setIcon(QIcon(get_piece(self.board.fen(), (i*8)+j)))

				button.setIconSize(QSize(50, 50))
				button.resize(50,50)
				button.clicked.connect(self.on_click)

				if ((i%2)+j)%2 == 0:
					button.setStyleSheet("background-color: #835C3B")
				else:
					button.setStyleSheet("background-color: white")

				self.buttons.append(button)

		self.show()

	@pyqtSlot()
	def on_click(self):
		position = int(self.sender().objectName().split(" ")[1])

		if self.first_position == "none":
			self.first_position = position
			self.buttons[position].setStyleSheet("background-color: blue")

		else:
			self.second_position = position

			if from_position_to_chess_move(self.first_position) != from_position_to_chess_move(self.second_position):

				algebraic_move = from_position_to_chess_move(self.first_position) + \
								 from_position_to_chess_move(self.second_position)

				if self.board.is_legal(chess.Move.from_uci(algebraic_move)):
					self.board.push(chess.Move.from_uci(algebraic_move))
					update_board(self.board, self.buttons)

					ai_move = ai_play(self.board)

					if self.board.is_legal(chess.Move.from_uci(ai_move)):
						self.board.push(chess.Move.from_uci(ai_move))
					else:
						raise ValueError('Your AI Made Illegal Move')

					update_board(self.board, self.buttons)

			if (((self.first_position // 8) % 2) + (self.first_position % 8)) % 2 == 0:
				self.buttons[self.first_position].setStyleSheet("background-color: #835C3B")
			else:
				self.buttons[self.first_position].setStyleSheet("background-color: white")

			self.first_position = "none"
			self.second_position = "none"



