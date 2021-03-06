# -*- coding: utf-8 -*-
"""EARIN_Exercise3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/196Vg2s5sAMsO2N4gEaiDZePeOJBLXnlC
"""

import numpy as np

def getInput():
  newInput = [-1, -1]
  run = 1
  while run == 1:
    print("Enter row where to place your symbol:")
    newInput[0] = int(input())
    print("Enter column where to place your symbol:")
    newInput[1] = int(input())
    if -1 < newInput[0] < 3 and -1 <newInput[1] < 3 and board[newInput[0]][newInput[1]] == '_':
      run = 0
    else:
      run = 1
      print("Invalid Inputs, reenter")

  return newInput

def adaptBoard(board, newInput, symbol):
  board[newInput[0]][newInput[1]] = symbol
  return board

def showBoard(board):
  print(board[0])
  print(board[1])
  print(board[2])

def newBoard():
  board = [
    [ '_', '_', '_' ],
    [ '_', '_', '_' ],
    [ '_', '_', '_' ]
  ]

  print(board[0])
  print(board[1])
  print(board[2])

  return board

# Python3 program to find the next optimal move for a player
#player, opponent = 'o', 'x'

# This function returns true if there are moves
# remaining on the board. It returns false if
# there are no moves left to play.
def isMovesLeft(board) :

	for i in range(3) :
		for j in range(3) :
			if (board[i][j] == '_') :
				return True
	return False

# This is the evaluation function as discussed
# in the previous article ( http://goo.gl/sJgv68 )
def evaluate(b) :

	# Checking for Rows for X or O victory.
	for row in range(3) :	
		if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :	
			if (b[row][0] == player) :
				return 10
			elif (b[row][0] == computer) :
				return -10

	# Checking for Columns for X or O victory.
	for col in range(3) :
	
		if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) :
		
			if (b[0][col] == player) :
				return 10
			elif (b[0][col] == computer) :
				return -10

	# Checking for Diagonals for X or O victory.
	if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
	
		if (b[0][0] == player) :
			return 10
		elif (b[0][0] == computer) :
			return -10

	if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
	
		if (b[0][2] == player) :
			return 10
		elif (b[0][2] == computer) :
			return -10

	# Else if none of them have won then return 0
	return 0

# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board
def minimax(board, depth, isMax) :
	score = evaluate(board)

	# If Maximizer has won the game return his/her
	# evaluated score
	if (score == 10) :
		return score #- depth

	# If Minimizer has won the game return his/her
	# evaluated score
	if (score == -10) :
		return score #+depth

	# If there are no more moves and no winner then
	# it is a tie
	if (isMovesLeft(board) == False): # or depth == 0:
		return 0

	# If this maximizer's move
	if (isMax) :	
		best = -1000

		# Traverse all cells
		for i in range(3) :		
			for j in range(3) :
			
				# Check if cell is empty
				if (board[i][j]=='_') :
				
					# Make the move
					board[i][j] = player

					# Call minimax recursively and choose
					# the maximum value
					best = max(best, minimax(board, depth - 1, 0) )

					# Undo the move
					board[i][j] = '_'
		return best

	# If this minimizer's move
	else:
		best = 1000

		# Traverse all cells
		for i in range(3) :		
			for j in range(3) :
			
				# Check if cell is empty
				if (board[i][j] == '_') :
				
					# Make the move
					board[i][j] = computer

					# Call minimax recursively and choose
					# the minimum value
					best = min(best, minimax(board, depth - 1, 1))

					# Undo the move
					board[i][j] = '_'
		return best

# This will return the best possible move for the player
def findBestMove(board, depth, isMax) :
	bestVal = 10000
	bestMove = (-1, -1)

	# Traverse all cells, evaluate minimax function for
	# all empty cells. And return the cell with optimal
	# value.
	for i in range(3) :	
		for j in range(3) :
		
			# Check if cell is empty
			if (board[i][j] == '_') :
			
				# Make the move
				board[i][j] = computer

				# compute evaluation function for this
				# move.
				#moveVal = pruning(board, depth, isMax, -1000, 1000)
				moveVal = minimax(board, depth, isMax)
				# Undo the move
				board[i][j] = '_'

				# If the value of the current move is
				# more than the best value, then update
				# best/
				if (moveVal < bestVal) :			
					bestMove = (i, j)
					bestVal = moveVal
	print(bestMove)
	return bestMove

def pruning(board, depth, isMax, alpha, beta):
  score = evaluate(board)
	# If Maximizer has won the game return his/her
  if score == 10:
    return score +depth

	# If Minimizer has won the game return his/her
  if score == -10:
    return score - depth
  
  if not isMovesLeft(board) or depth == 0:
    return 0

  if isMax:                   # if Max-move then
    #alpha = -1000
    for i in range(3):        # for u in U do
      for j in range(3):
        if board[i][j] == '_':
          board[i][j] = computer      # Do move
          alpha = max(alpha, pruning(board, depth-1, 0, alpha, beta))
          board[i][j] = '_'           # Undo move
          if alpha > beta:
            return beta
    return alpha
  else:
   # beta = 1000
    for i in range(3):
      for j in range(3):
        if board[i][j] == '_':
          board[i][j] = player        # Do move
          beta = max(beta, pruning(board, depth-1, 1, alpha, beta))
          board[i][j] = '_'           # Undo move
          if beta > alpha:
            return alpha
    return beta

player, computer = 'x', 'o'

print("Hello to the Tik tak hoe game. What depth should the algorithm use?")
depth = int(input())
board = newBoard()
while isMovesLeft(board):
  newInput = getInput()
  new = adaptBoard(board, newInput, player)
  
  eva = evaluate(board)
  if eva == 10:
    print("Player wins")
    break
  print("Depth is: ", depth)
  move = findBestMove(board, depth, False)
  print(move)
  board = adaptBoard(board, move, computer)
  print(showBoard(board))
  eva = evaluate(board)
  if eva == -10:
    print("Computer wins")
    break
print("no move left, restart programm to play again. Bye")