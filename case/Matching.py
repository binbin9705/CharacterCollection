
import re

class Matching(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def start(self):
        for s in range(len(self.name)):
            print(self.name[s])



if __name__ == '__main__':
    name=['小明','小胖','小区']
    age=18
    demo=Matching(name=name,age=age)
    demo.start()
