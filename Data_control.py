import json
import os
import copy
import random


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



    def save(self,data): 
        fe=self.fetch()

        for key, value in data.items():
            if key in fe:
                fe[key] = value 
            else:
                fe.update(data)

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
        games=0
        for i in in_set:
            games+=in_set[i]['number']+1

        choose=random.randint(0,games)
        win=0
        for i in in_set:
            win+=in_set[i]['win']+1
            if choose<=win: return {i:in_set[i]}

        return -1
        
    def find(seld,data,board):
        for i in data:
            if data[i]['state']==board:
                return True
        
        return False


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
                if not self.find(data,temp):
                    out =MyStruct(int(list(data)[-1])+1,str(node),0,0,temp).to_dict()
                    node=str(int(list(data)[-1])+1)

        out[node]['number']+=1
        return out
            






if not os.path.exists("data.json"):
    data=Data(8)
    state=[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
    initial_data=MyStruct(0,-1,0,0,state).to_dict()
    data.save(initial_data)

