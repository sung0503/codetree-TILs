from collections import deque


class Node():
    def __init__(self, mid, pid, color, max_depth):
        self.mid = mid
        self.pid = pid
        self.color = color
        self.max_depth = max_depth
        self.depth_remain = max_depth - 1
        self.child_ids = []


class Trees():
    def __init__(self):
        self.root_ids = []
        self.nodes = {}

    def regist_node(self, node):
        self.nodes[node.mid] = node

    def add_root(self, node):
        self.root_ids.append(node.mid)
        self.regist_node(node)
    
    def add_node(self, node):
        # check max_depth
        if self.nodes[node.pid].depth_remain > 0:
            self.nodes[node.pid].child_ids.append(node.mid)
            node.depth_remain = min(self.nodes[node.pid].depth_remain - 1, node.max_depth - 1)
            self.regist_node(node)
    
    def change_color(self, mid, color_to):
        que = deque([mid])
        while que:
            cur_id = que.popleft()
            self.nodes[cur_id].color = color_to
            node = self.nodes[cur_id]
            for child_id in node.child_ids:
                que.append(child_id)

    def get_color(self, mid):
        print(self.nodes[mid].color)
    
    def calc_value(self):
        res = 0
        for i in self.root_ids:
            res += (self.dfs(i))[1]
        print(res)
    
    def dfs(self, mid):
        value = 0
        color_set = set([self.nodes[mid].color])
        for child_id in self.nodes[mid].child_ids:
            child_color_set, child_value = self.dfs(child_id)
            color_set |= child_color_set
            value += child_value
        value += len(color_set) * len(color_set)
        return color_set, value


def main():
    Q = int(input())
    trees = Trees()
    for _ in range(Q):
        data = list(map(int, input().split()))
        if data[0] == 100:
            node = Node(data[1], data[2], data[3], data[4])
            if data[2] == -1:
                # add root
                trees.add_root(node)
            else:
                trees.add_node(node)
        elif data[0] == 200:
            trees.change_color(data[1], data[2])
        elif data[0] == 300:
            trees.get_color(data[1])
        elif data[0] == 400:
            trees.calc_value()
        else:
            raise NotImplementedError("Undefined Operation")


if __name__ == '__main__':
    main()