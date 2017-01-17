import queue
import functools

@functools.total_ordering
class AbstractTree:
    def expand(self):
        return list(self.branches)
    def __eq__(self, other):
        return self.root==other.root
    def __lt__(self, other):
        return self.root<other.root

class ListTree(AbstractTree):
    def __init__(self, root, branches=None):
        self.root = root
        self.branches = branches if branches is not None else []

class AbstractCostTree(AbstractTree):
    def expand_costs(self):
        return zip(list(self.branches),list(self.costs))

class ListCostTree(AbstractCostTree):
    def __init__(self, root, branches=None, costs=None):
        self.root = root
        self.branches = branches if branches is not None else []
        self.costs = costs if costs is not None else [1]*len(self.branches)
    def add_bc(self, branch, cost):
        self.branches.append(branch)
        self.costs.append(cost)

def dfs(tree, goal):
    if goal(tree.root):
        return [tree.root]
    for b in tree.expand():
        res = dfs(b, goal)
        if res is not None:
            return res+[tree.root]
    return None

def bfs(tree, goal):
    q = queue.Queue()
    q.put((tree,[tree.root]))
    while not q.empty():
        c = q.get()
        if goal(c[0].root):
            return c[1]
        for i in c[0].expand():
            q.put((i,[i.root]+c[1]))
        
def ucs(tree, goal):
    q = queue.PriorityQueue()
    q.put( (0,tree,[tree.root]) )
    while not q.empty():
        c = q.get()
        if goal(c[1].root):
            return c[2],c[0]
        for i in c[1].expand_costs():
            if i[0].root not in c[2]:
                q.put((i[1]+c[0],i[0],[i[0].root]+c[2]))
