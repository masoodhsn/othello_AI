import pygame
import sys
import game
import copy
import Data_control


def main():
    learn=False
    pygame.init()
    othello=game.othello()
    data=Data_control.Data(8)
    screen = pygame.display.set_mode((othello.SCREEN_SIZE, othello.SCREEN_SIZE))
    pygame.display.set_caption("Othello Game")
    clock = pygame.time.Clock()



    board = othello.create_board()
    back_board=copy.deepcopy(board)
    turn = "B"  # ‌black player is start

    while True:
        learn_data_w=data.give_me_score_board()
        score_board_w=list(learn_data_w.values())[0]['state']
        learn_data_b=data.give_me_score_board()
        score_board_b= list(learn_data_b.values())[0]['state']
        
        while(score_board_b == score_board_w):
            learn_data_b=data.give_me_score_board()
            score_board_b= list(learn_data_b.values())[0]['state']
            if not learn: break

        if learn:
            print("score board B: "+str(list(learn_data_b)[0]))
            for i in score_board_b:
                print(i)
   
        print("score board W: "+str(list(learn_data_w)[0]))
        for i in score_board_w:
            print(i)


        while True:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    board=copy.deepcopy(back_board)

                
                elif not learn and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn == "B":  # کلیک چپ

                    row, col = othello.get_cell_from_mouse(pos)
                    if othello.is_valid_move(board, row, col, "B"):
                        print(str(row)+" "+str(col))
                        back_board = copy.deepcopy(board)
                        othello.apply_move(board, row, col, "B")
                        turn = othello.toggle_turn("B")
                    #print("B:"+str(othello.score(board,"B")))

            if not learn:
                othello.draw_board(screen, board)
                pygame.display.flip()
                clock.tick(30)

            if learn and turn=="B":
                i,j=othello.minmax_search(board,score_board_b,"B")
                if i>=0 and j>=0:
                    othello.apply_move(board, i, j, "B")
                    turn = othello.toggle_turn("B")
                    #print("W:"+str(othello.score(board,"B")))
            elif turn=="W":
                i,j=othello.minmax_search(board,score_board_w,"W")
                if i>=0 and j>=0:
                    othello.apply_move(board, i, j, "W")
                    turn = othello.toggle_turn("W")
                    #print("W:"+str(othello.score(board,"W")))
            
            if not othello.has_valid_move(board, turn):
                        turn = othello.toggle_turn(turn)
                        if not othello.has_valid_move(board, turn):
                            print("Game Over!")
                            B,W=othello.final_score(board) 
                            board=othello.create_board()
                            if W>B :
                                list(learn_data_w.values())[0]['win']+=1
                                print(str(str(list(learn_data_w)[0]))+" is winner")
                            else:
                                list(learn_data_b.values())[0]['win']+=1
                                print(str(str(list(learn_data_b)[0]))+" is winner")

                            if learn:                            
                                data.save(learn_data_b)
                            data.save(learn_data_w)
                            if not learn:
                                pygame.quit()
                                sys.exit()
                            break;

if __name__ == "__main__":
    main()