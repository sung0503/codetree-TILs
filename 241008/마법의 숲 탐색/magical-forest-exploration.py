from collections import deque

DIRECT = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Forest():
    def __init__(self, r, c):
        self.R = r
        self.C = c
        self.board = []
        self.dic = {}
        self.clear()
        self.count = 0

    def clear(self):
        self.board = [[None] * self.C for _ in range(self.R + 3)]
        self.dic = {}

    def is_reached_bottom(self, r_core):
        return r_core == self.R + 1

    def is_valid_idx(self, r, c):
        return 0 <= r <= self.R + 2 and 0 <= c < self.C

    def is_empty(self, r, c):
        return self.board[r][c] is None

    def able_down(self, r_core, c_core):
        return r_core < self.R + 1 and self.is_empty(r_core + 2, c_core) and self.is_empty(r_core + 1, c_core - 1) and self.is_empty(r_core + 1, c_core + 1)

    def able_left_down(self, r_core, c_core):
        return 1 < c_core and self.is_empty(r_core, c_core - 2) and self.is_empty(r_core + 1, c_core - 1) and self.is_empty(r_core - 1, c_core - 1) \
                and self.is_empty(r_core + 1, c_core - 2) and self.is_empty(r_core + 2, c_core - 1)

    def able_right_down(self, r_core, c_core):
        return c_core < self.C - 2 and self.is_empty(r_core, c_core + 2) and self.is_empty(r_core + 1, c_core + 1) and self.is_empty(r_core - 1, c_core + 1) \
                and self.is_empty(r_core + 1, c_core + 2) and self.is_empty(r_core + 2, c_core + 1)
    
    def update_board(self, r_core, c_core, d_core, reached_bottom=None):
        global DIRECT

        self.count += 1

        door = (r_core + DIRECT[d_core][0], c_core + DIRECT[d_core][1])
        self.board[r_core][c_core] = door
        self.dic[door] = r_core - 1
        for i, j in DIRECT:
            self.board[r_core + i][c_core + j] = door
        
        if reached_bottom:
            return self.R
        
        init_val = r_core - 1
        visit = [[False] * self.C for _ in range(self.R + 3)]
        return self.dfs(*door, visit, init_val)
    
    def dfs(self, r, c, visit, init_val):
        visit[r][c] = True
        res = init_val
        for i, j in DIRECT:
            if self.is_empty(r + i, c + j) and self.board[r + i][c + j] == (r, c) and visit[r+i][c+j]:
                continue
            res = max(res, self.dfs(r+i, c+j, visit, init_val))
        return res

    def explore(self, c_i, d_i):
        # print("\nstart", c_i, d_i)
        r_core = 1
        c_core = c_i
        d_core = d_i
        while True:
            # print(r_core, c_core, d_core)
            if self.is_reached_bottom(r_core):
                # update board with max value R
                return self.update_board(r_core, c_core, d_core, reached_bottom=True)
            if self.able_down(r_core, c_core):
                # go down
                # only update r_core
                r_core += 1
            elif self.able_left_down(r_core, c_core):
                # go left, turn counter clock-wise and go down
                # update r_core & c_core & d_core
                # as a result, r_core += 1 and c_core -= 1 and d_core rotate counter clock-wise
                r_core += 1
                c_core -= 1
                d_core = (4 + d_core - 1) % 4
            elif self.able_right_down(r_core, c_core):
                # go right, turn clock-wise and go down
                # update r_core & c_core & d_core
                # as a result, r_core += 1 and c_core += 1 and d_core rotate clock-wise
                r_core += 1
                c_core += 1
                d_core = (d_core + 1) % 4
            else:
                # not reached to bottom, but nowhere to go
                # identify this is normal end or robot is still out of forest
                # if robot is still out of forest, clear board & return 0
                if r_core < 4:
                    self.clear()
                    return 0
                # update board and return robot's reachable maximum row.
                return self.update_board(r_core, c_core, d_core)

def main():
    R, C, K = map(int, input().split())
    reseult = 0
    forest = Forest(R, C)
    # for i in forest.board:
    #     print(i)
    for k in range(K):
        c_i, d_i = map(int, input().split())
        reseult += forest.explore(c_i - 1, d_i)
        # print(reseult)
        # print(forest.dic)
        # for i in forest.board:
        #     print(i)
    print(reseult)


if __name__ == '__main__':
    main()