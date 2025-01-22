import json
import os
import copy
import random
from math import floor


class MyStruct:
    def __init__(self, number, father, win, loss, state):
        self.number = number
        self.father = father
        self.win = win
        self.loss=loss
        self.state = state

    def to_dict(self):
        return {
            str(self.number):{
            'father': self.father,
            'win': self.win,
            'number': self.loss,
            'state': self.state
            }
        }
    


class Data:
    def __init__(self, board_size):
        self.BOARD_SIZE=board_size



    def save(self,data,win): 
        fe=self.fetch()
        for key, value in data.items():
            if key in fe:
                fe[key] = value 
            else:
                fe.update(data)

        father=list(data.values())[0]["father"]
        while(father != -1):
            
            data={str(father):fe[str(father)]}
            data[str(father)]['number']+=1
            if win == 1:
                data[str(father)]['win']+=1

            for key, value in data.items():
                if key in fe:
                    fe[key] = value 
                else:
                    fe.update(data)

            father=list(data.values())[0]["father"]


        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(fe, json_file, ensure_ascii=False, indent=4)




    def fetch(self):
        try:
        
            with open("data.json", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}

        return data
        

    def set_ret(self,data,id):
        out={}
        out={id:data[id]}
        for i in data:
            if str(data[i]["father"]) == list(out)[0]:
                out.update({i:data[i]})
        return out
    
    def select(self,in_set): 
        games=(len(in_set))*100

        choose=random.randint(0,games)
        win=0
        for i in in_set:
            win+=floor((in_set[i]['win']+1)/in_set[i]['number']*100)
            if choose<=win: return {i:in_set[i]}

        return -1
        
    def find(seld,data,board):
        for i in data:
            if data[i]['state']==board:
                return True
        
        return False


    def normalizer(self,board):
        min=board[0][0]
        for i in range(len(board)):
            for j in range(len(board)):
                if(min>board[i][j]):
                    min=board[i][j]
                    if min == 1:
                        return board
                    
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j]-=min-1
        return board


    def give_me_score_board(self):
        data=self.fetch()
        out={}
        out=self.select(self.set_ret(data,"0"))
        node='0'

        while out == -1 or list(out.keys())[0]!=node:
            if(out != -1):
                node = list(out.keys())[0]
                out=self.select(self.set_ret(data,node)) 
            else:
                out = {node:data[node]}
                i=random.randint(0,int(self.BOARD_SIZE/2)-1)
                j=random.randint(0,int(self.BOARD_SIZE/2)-1)
                temp=copy.deepcopy(out[node]['state'])
                temp[i][j]+=1
                temp=self.normalizer(temp)
                if not self.find(data,temp):
                    out =MyStruct(int(list(data)[-1])+1,str(node),0,0,temp).to_dict()
                    node=str(int(list(data)[-1])+1)

        out[node]['number']+=1
        return out
            

if not os.path.exists("data.json"):
    data=Data(8)
    state=[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
    initial_data=MyStruct(0,-1,0,1,state).to_dict()
    data.save(initial_data,0)
    state=[[200,15,15,15],[15,8,8,8],[15,8,10,10],[15,8,10,1]]
    initial_data=MyStruct(1,0,0,1,state).to_dict()
    data.save(initial_data,0)
    state=[[20,10,10,10],[10,5,5,5],[10,5,2,2],[10,5,2,1]]
    initial_data=MyStruct(2,0,0,1,state).to_dict()
    data.save(initial_data,0)

