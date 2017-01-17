from treesearch import *
import functools

@functools.total_ordering
class TuringMachine:
    def __init__(self, table, start, tape='', read = 0):
        self.table = table
        self.state = start
        self.read = read
        self.tape = tape
    def __eq__(self, other):
        return self.read == other.read
    def __lt__(self, other):
        return self.read<other.read
    def step(self):
        if self.read>=len(self.tape):
            return "Next"
        move = self.table[self.state+self.tape[self.read]]
        self.tape = self.tape[:self.read]+move[0]+self.tape[self.read+1:]
        if move[1]=='<':
            if self.read==0:
                self.tape = '0'+self.tape
            else:
                self.read-=1
        elif move[1]=='>':
            self.read+=1
        self.state = move[2]
        return move
    def run(self, max_steps=1000):
        move = ''
        i=0
        while move is not 'Next' and i<max_steps:
            move = self.step()
            i+=1
        if i==max_steps:
            return "Time up", i
        return "Next", i
    def next_symbol(self, sym):
        self.tape+=sym
    def run_on_input(self, input_tape):
        msg = ('',0)
        i=0
        while msg[0] is not 'Time up' and i<len(input_tape):
            self.next_symbol(input_tape[i])
            i+=1
            msg = self.run()
        return msg
    @property
    def full_state(self):
        return self.tape[:self.read] + self.state + self.tape[self.read:]
    def copy(self):
        return TuringMachine(self.table, self.state, self.tape, self.read)

class UniversalTreeTimed(AbstractCostTree):
    def __init__(self, tm, symbol):
        self.tm = tm
        self.root = (symbol,tm)
        self.branches = None
        self.costs = None
    def expand(self):
        if self.branches is None:
            self.expand_costs()
        return self.branches
    def expand_costs(self):
        if self.branches is None:
            self.branches = []
            self.costs = []
            b0, b1 = self.tm.copy(), self.tm.copy()
            b0.next_symbol('0')
            b1.next_symbol('1')
            res0, res1 = b0.run(), b1.run()
            if res0[0] == 'Next':
                self.branches.append(UniversalTreeTimed(b0, '0'))
                self.costs.append(res0[1])
            if res1[0] == 'Next':
                self.branches.append(UniversalTreeTimed(b1, '1'))
                self.costs.append(res1[1])
        return AbstractCostTree.expand_costs(self)
        
tm = TuringMachine({'A0':'1>B','A1':'1>A','B0':'0<A','B1':'0>B'},'A')
tree = UniversalTreeTimed(tm.copy(),'')
#print(tm.run_on_input('11000001'))
#print(tm.full_state)
res = ucs(tree, lambda root: root[1].full_state.find('11000001')>=0)
print([r[0] for r in res[0][::-1]], res[1])
