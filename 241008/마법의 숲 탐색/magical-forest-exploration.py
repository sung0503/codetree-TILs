from collections import defaultdict
from collections import deque

DIRECT = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Forest:
    def __init__(self, r, c):
        self.R = r
        self.C = c
        self.board = []
        self.robots = {}
        self.score = {}
        self.count = 0
        self.clear()

    def clear(self):
        self.board = [[None] * self.C for _ in range(self.R + 3)]
        self.robots = {}
        self.score = {}
        self.count = 0

    def is_reached_bottom(self, r_core):
        return r_core == self.R + 1

    def is_valid_idx(self, r, c):
        return 0 <= r <= self.R + 2 and 0 <= c < self.C

    def is_empty(self, r, c):
        return self.board[r][c] is None

    def able_down(self, r_core, c_core):
        return (
            r_core < self.R + 1
            and self.is_empty(r_core + 2, c_core)
            and self.is_empty(r_core + 1, c_core - 1)
            and self.is_empty(r_core + 1, c_core + 1)
        )

    def able_left_down(self, r_core, c_core):
        return (
            1 < c_core
            and self.is_empty(r_core, c_core - 2)
            and self.is_empty(r_core + 1, c_core - 1)
            and self.is_empty(r_core - 1, c_core - 1)
            and self.is_empty(r_core + 1, c_core - 2)
            and self.is_empty(r_core + 2, c_core - 1)
        )

    def able_right_down(self, r_core, c_core):
        return (
            c_core < self.C - 2
            and self.is_empty(r_core, c_core + 2)
            and self.is_empty(r_core + 1, c_core + 1)
            and self.is_empty(r_core - 1, c_core + 1)
            and self.is_empty(r_core + 1, c_core + 2)
            and self.is_empty(r_core + 2, c_core + 1)
        )

    def update_board(self, r_core, c_core, d_core, reached_bottom=None):
        global DIRECT

        self.count += 1
        cur_robot = self.count

        self.robots[cur_robot] = (r_core, c_core, d_core)
        self.board[r_core][c_core] = cur_robot
        for i, j in DIRECT:
            self.board[r_core + i][c_core + j] = cur_robot
        self.score[cur_robot] = min(self.R, r_core - 1)

        if reached_bottom:
            return self.score[cur_robot]

        visit = [False] * (self.count + 1)
        return max(self.score[cur_robot], self.dfs(cur_robot, visit))

    def dfs(self, cur_robot, visit):
        visit[cur_robot] = True
        r_core, c_core, d_core = self.robots[cur_robot]
        r_door, c_door = r_core + DIRECT[d_core][0], c_core + DIRECT[d_core][1]
        res = self.score[cur_robot]
        for i, j in DIRECT:
            n_r, n_c = r_door + i, c_door + j
            if not self.is_valid_idx(n_r, n_c):
                continue
            if self.is_empty(n_r, n_c):
                continue
            if self.board[n_r][n_c] == cur_robot:
                continue
            if visit[self.board[n_r][n_c]]:
                continue
            res = max(res, self.dfs(self.board[n_r][n_c], visit))
        return res

    def explore(self, c_i, d_i):
        r_core = 1
        c_core = c_i
        d_core = d_i
        while True:
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
    for k in range(K):
        c_i, d_i = map(int, input().split())
        reseult += forest.explore(c_i - 1, d_i)
    print(reseult)


if __name__ == "__main__":
    main()