import pygame

class othello:
	def __init__(self):
		# تنظیمات صفحه
		self.BOARD_SIZE = 8  # تعداد خانه‌ها در هر ردیف و ستون
		self.CELL_SIZE = 80  # اندازه هر خانه
		self.SCREEN_SIZE = self.BOARD_SIZE * self.CELL_SIZE

		# رنگ‌ها
		self.WHITE = (255, 255, 255)
		self.BLACK = (0, 0, 0)
		self.GREEN = (34, 139, 34)
		self.GRAY = (169, 169, 169)
 
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




	# تغییر نوبت بازیکن
	def toggle_turn(self,turn):
		return "W" if turn == "B" else "B"

	# قرار دادن مهره
	def place_piece(self,board, row, col, turn):
		if board[row][col] is None:  # اگر خانه خالی است
			board[row][col] = turn
			return True
		return False