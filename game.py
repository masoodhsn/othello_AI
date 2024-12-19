import pygame
import copy

class othello:
	def __init__(self):
		# تنظیمات صفحه
		self.BOARD_SIZE = 8  # تعداد خانه‌ها در هر ردیف و ستون
		self.CELL_SIZE = 80  # اندازه هر خانه
		self.SCREEN_SIZE = self.BOARD_SIZE * self.CELL_SIZE
		self.STEP = 3

		# رنگ‌ها
		self.WHITE = (255, 255, 255)
		self.BLACK = (0, 0, 0)
		self.GREEN = (34, 139, 34)
		self.GRAY = (169, 169, 169)

		# جهت‌ها برای بررسی حرکت
		self.DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
 
	def create_board(self):
		board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
		# قرار دادن مهره‌های اولیه
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


	# تشخیص کلیک روی خانه‌ها
	def get_cell_from_mouse(self,pos):
		x, y = pos
		row = y // self.CELL_SIZE
		col = x // self.CELL_SIZE
		return row, col


	# بررسی حرکت معتبر
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

	# اعمال حرکت و تغییر مهره‌ها
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

	# بررسی پایان بازی
	def has_valid_move(self,board, turn):
		for row in range(self.BOARD_SIZE):
			for col in range(self.BOARD_SIZE):
				if self.is_valid_move(board, row, col, turn):
					return True
		return False



	# تغییر نوبت بازیکن
	def toggle_turn(self,turn):
		return "W" if turn == "B" else "B"


	def score(self,board,turn):
		score=0
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if (board[i][j]==turn):
					if ((i ==0 and j == 0) or (i ==0 and j == self.BOARD_SIZE-1) or (i == self.BOARD_SIZE-1 and j == 0) or (i == self.BOARD_SIZE-1 and j == self.BOARD_SIZE-1)):
						score+= self.BOARD_SIZE * 4;

					else:						
						i_t = abs(i - (self.BOARD_SIZE-1)/2)
						j_t = abs(j - (self.BOARD_SIZE-1)/2)
						maxi=  i_t if i_t>j_t else j_t
						score += (maxi%2) * 3 + maxi * 2 + 1

		return(score)


	def minmax_search(self,board):
		t1,t2,s=self.max_value(board,self.STEP-1)
		return t1,t2

	def max_value(self,board,step):
		if(step==-1): return -1,-1,self.score(board,"W")
		score=0
		ii,jj=0,0
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if(self.is_valid_move(board,i,j,"W")):
					temp_board= copy.deepcopy(board)
					self.apply_move(temp_board,i,j,"W")
					t1,t2,s=self.min_value(temp_board,step-1)
					if (s > score):
						score=s
						ii=i
						jj=j

		return ii,jj,score


	def min_value(self,board,step):
		if(step==-1): return -1,-1,self.score(board,"W")
		score=10000
		ii,jj=0,0
		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if(self.is_valid_move(board,i,j,"B")):
					temp_board= copy.deepcopy(board)
					self.apply_move(temp_board,i,j,"B")
					t1,t2,s=self.max_value(temp_board,step-1)
					if (s < score):
						score=s
						ii=i
						jj=j 

		return ii,jj,score
