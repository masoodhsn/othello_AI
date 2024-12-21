import pygame
import sys
import game
import copy
import Data_control


def main():
    learn=True
    pygame.init()
    othello=game.othello()
    data=Data_control.Data()
    screen = pygame.display.set_mode((othello.SCREEN_SIZE, othello.SCREEN_SIZE))
    pygame.display.set_caption("Othello Game")
    clock = pygame.time.Clock()

    score_board=data.best()
    board = othello.create_board()
    back_board=copy.deepcopy(board)
    turn = "B"  # ‌black player is start


    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                board=copy.deepcopy(back_board)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn == "B":  # کلیک چپ

                row, col = othello.get_cell_from_mouse(pos)
                if othello.is_valid_move(board, row, col, "B"):
                    print(str(row)+" "+str(col))
                    back_board = copy.deepcopy(board)
                    othello.apply_move(board, row, col, "B")
                    turn = othello.toggle_turn("B")
                #print("B:"+str(othello.score(board,"B")))


            elif turn=="W":
                i,j=othello.minmax_search(board,score_board)
                if i>=0 and j>=0:
                    othello.apply_move(board, i, j, "W")
                    turn = othello.toggle_turn("W")
                    #print("W:"+str(othello.score(board,"W")))
                

            if not othello.has_valid_move(board, turn):
                        turn = othello.toggle_turn(turn)
                        if not othello.has_valid_move(board, turn):
                            print("Game Over!")
                            othello.final_score(board) 
                            pygame.quit()
                            sys.exit()

        othello.draw_board(screen, board)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()