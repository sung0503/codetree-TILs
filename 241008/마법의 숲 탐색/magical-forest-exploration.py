from collections import deque

DIRECT = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Forest():
    def __init__(self, r, c):
        self.R = r
        self.C = c
        self.board = []
        self.clear_borad()

    def clear_borad(self):
        self.board = [[-1] * self.C for _ in range(self.R + 3)]

    def is_reached_bottom(self, r_core):
        return r_core == self.R + 1

    def is_valid_idx(self, r, c):
        return 0 <= r <= self.R + 2 and 0 <= c < self.C

    def is_empty(self, r, c):
        # return self.is_valid_idx(r, c) and self.board[r][c] == -1.
        return self.board[r][c] == -1.

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
        if reached_bottom:
            self.board[r_core][c_core] = self.R
            for i, j in DIRECT:
                self.board[r_core + i][c_core + j] = self.R
            return self.R
        max_value = r_core - 1
        r_door, c_door = r_core + DIRECT[d_core][0], c_core + DIRECT[d_core][1]
        for i, j in DIRECT:
            t_r, t_c = r_door + i, c_door + j
            if self.is_valid_idx(t_r, t_c):
                max_value = max(max_value, self.board[t_r][t_c])
        self.board[r_core][c_core] = max_value
        for i, j in DIRECT:
            self.board[r_core + i][c_core + j] = max_value
        return max_value

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
                    self.clear_borad()
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
        # for i in forest.board:
        #     print(i)
    print(reseult)


if __name__ == '__main__':
    main()