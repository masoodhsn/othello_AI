import pygame
import copy

class othello:
	def __init__(self):
		# تنظیمات صفحه
		self.BOARD_SIZE = 8  # it must be even
		self.CELL_SIZE = 80  
		self.SCREEN_SIZE = self.BOARD_SIZE * self.CELL_SIZE
		self.STEP = 4

		# رنگ‌ها
		self.WHITE = (255, 255, 255)
		self.BLACK = (0, 0, 0)
		self.GREEN = (34, 139, 34)
		self.GRAY = (169, 169, 169)

		self.DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
 
	def create_board(self):
		board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
		mid = self.BOARD_SIZE // 2
		board[mid - 1][mid - 1] = "W"
		board[mid][mid] = "W"
		board[mid - 1][mid] = "B"
		board[mid][mid - 1] = "B"
		return board


	def draw_board(self,screen, board):
		screen.fill(self.GREEN)
		for row in range(self.BOARD_SIZE):
			for col in range(self.BOARD_SIZE):
				rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
				pygame.draw.rect(screen, self.BLACK, rect, width=1)  # رسم خطوط خانه‌ها
            
				# رسم مهره‌ها
				if board[row][col] == "W":
					pygame.draw.circle(screen, self.WHITE, rect.center, self.CELL_SIZE // 3)
				elif board[row][col] == "B":
					pygame.draw.circle(screen, self.BLACK, rect.center, self.CELL_SIZE // 3)


	def get_cell_from_mouse(self,pos):
		x, y = pos
		row = y // self.CELL_SIZE
		col = x // self.CELL_SIZE
		return row, col


	

	
	def is_valid_move(self,board, row, col, turn):
		if board[row][col] is not None:
			return False
		opponent = "W" if turn == "B" else "B"

		for dr, dc in self.DIRECTIONS:
			r, c = row + dr, col + dc
			has_opponent = False
			while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and board[r][c] == opponent:
				has_opponent = True
				r += dr
				c += dc
			if has_opponent and 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and board[r][c] == turn:
				return True
		return False

	def apply_move(self,board, row, col, turn):
		opponent = "W" if turn == "B" else "B"
		board[row][col] = turn
		for dr, dc in self.DIRECTIONS:
			r, c = row + dr, col + dc
			path = []
			while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and board[r][c] == opponent:
				path.append((r, c))
				r += dr
				c += dc
			if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and board[r][c] == turn:
				for pr, pc in path:
					board[pr][pc] = turn


	def has_valid_move(self,board, turn):
		for row in range(self.BOARD_SIZE):
			for col in range(self.BOARD_SIZE):
				if self.is_valid_move(board, row, col, turn):
					return True
		return False




	def toggle_turn(self,turn):
		return "W" if turn == "B" else "B"


	def score(self,board,turn,score_board):
		score=0
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if (board[i][j]==turn):
					if(i<self.BOARD_SIZE/2 and j<self.BOARD_SIZE/2):
						score+=score_board[i][j]
					elif(i<self.BOARD_SIZE/2 and j>=self.BOARD_SIZE/2):
						score+=score_board[i][self.BOARD_SIZE-1-j]
					elif(i>=self.BOARD_SIZE/2 and j<self.BOARD_SIZE/2):
						score+=score_board[self.BOARD_SIZE-1-i][j]
					elif(i>=self.BOARD_SIZE/2 and j>=self.BOARD_SIZE/2):
						score+=score_board[self.BOARD_SIZE-1-i][self.BOARD_SIZE-1-j]

		return(score)


	def minmax_search(self,board,score_board,turn):
		t1,t2,s=self.max_value(board,self.STEP-1,score_board,turn,1000)
		return t1,t2

	def max_value(self,board,step,score_board,turn,limit):
		opponent = "W" if turn == "B" else "B"
		if(step==-1 or not self.has_valid_move(board, turn)): return -1,-1,self.score(board,turn,score_board)
		score=0
		ii,jj=-1,-1
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if(self.is_valid_move(board,i,j,turn)):
					temp_board= copy.deepcopy(board)
					self.apply_move(temp_board,i,j,turn)
					t1,t2,s=self.min_value(temp_board,step-1,score_board,opponent,score)
					if (s > score and s>0):
						score=s
						ii=i
						jj=j
						if(s>limit):
							return -1,-1,0
				

		return ii,jj,score


	def min_value(self,board,step,score_board,turn,limit):
		opponent = "W" if turn == "B" else "B"
		if(step==-1 or not self.has_valid_move(board, turn)): return -1,-1,self.score(board,turn,score_board)
		score=10000
		ii,jj=-1,-1
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if(self.is_valid_move(board,i,j,turn)):
					temp_board= copy.deepcopy(board)
					self.apply_move(temp_board,i,j,turn)
					t1,t2,s=self.max_value(temp_board,step-1,score_board,opponent,score)
					if (s < score and s >0):
						score=s
						ii=i
						jj=j 
						if(s<limit):
							return -1,-1,0

		return ii,jj,score

	def final_score(self,board):
		b_score=0
		w_score=0
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if(board[i][j]=="B"):
					b_score+=1
				if(board[i][j]=="W"):
					w_score+=1

		print("black:" + str(b_score))
		print("white:" + str(w_score))

		return b_score,w_score