import json
import os
import copy


class MyStruct:
    def __init__(self, number, father, win, loss, state):
        self.number = number
        self.father = father
        self.win = win
        self.loss=loss
        self.state = state

    def to_dict(self):
        return {
            'number': self.number,
            'father': self.father,
            'win': self.win,
            'loss': self.loss,
            'state': self.state
        }
    


class Data:

    def save(self,data):    
        data_dict = [item.to_dict() for item in data]        
        try:
            with open("data.json", 'w') as file:
                json.dump(data_dict, file, indent=4)
            print("data saved successfully")
        except Exception as e:
            print(f"Error on saveing data: {e}")




    def fetch(self):
        if not os.path.exists("data.json"):
            print("data.json not found")
            print("create data.json with initial data")
            state=[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
            initial_data=[MyStruct(0,-1,0,0,state)]
            self.save(initial_data)
            return [item.to_dict() for item in initial_data]

        else:
            print("data.json founded")
            try:
                with open("data.json", 'r') as file:
                    loaded_data_dict = json.load(file)
                print("data fetched successfully")
            except Exception as e:
                print(f"Error on saveing data: {e}")

            return loaded_data_dict
        

    def best(self):
        datas=self.fetch()
        out=[]
        max=-10000
        for item in datas:
            if (item['win']-item['loss']>max):
                max=item['win']-item['loss']
                out=copy.deepcopy(item['state'])

        return out


