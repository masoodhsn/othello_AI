import pygame
import sys
import game


def main():
    pygame.init()
    othello=game.othello()
    screen = pygame.display.set_mode((othello.SCREEN_SIZE, othello.SCREEN_SIZE))
    pygame.display.set_caption("Othello Game")
    clock = pygame.time.Clock()

    board = othello.create_board()
    turn = "B"  # بازیکن سیاه شروع می‌کند

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # کلیک چپ
                pos = pygame.mouse.get_pos()
                row, col = othello.get_cell_from_mouse(pos)
                if othello.is_valid_move(board, row, col, turn):
                    othello.apply_move(board, row, col, turn)
                    turn = othello.toggle_turn(turn)
                    if not othello.has_valid_move(board, turn):
                        turn = othello.toggle_turn(turn)
                        if not othello.has_valid_move(board, turn):
                            print("Game Over!")
                            pygame.quit()
                            sys.exit()

        othello.draw_board(screen, board)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()