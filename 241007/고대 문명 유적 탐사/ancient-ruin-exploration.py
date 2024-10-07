import collections
import copy
import heapq


NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
ROT_COORDS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
ROTSATIONS = [2, 4, 6]

RUIN_SIZE = 5


class Ruin():
    def __init__(self, board=None):
        if board is None:
            self.board = [[0] * RUIN_SIZE for _ in range(RUIN_SIZE)]
        else:
            self.board = copy.deepcopy(board)
        self.init_visit()
    
    def init_visit(self):
        self.visit = [[False] * RUIN_SIZE for _ in range(RUIN_SIZE)]

    def is_wrong_coord(self, x, y):
        return x < 0 or 4 < x or y < 0 or 4 < y

    def rotate(self, x, y, r):
        assert r == 2 or r == 4 or r == 6
        new_ruin = Ruin(self.board)
        for idx, (ori_i, ori_j) in enumerate(ROT_COORDS):
            rot_i, rot_j = ROT_COORDS[(idx + r) % 8]
            new_ruin.board[x + rot_i][y + rot_j] = self.board[x + ori_i][y + ori_j]
        return new_ruin
    
    def calc_score(self):
        score = 0
        for x in range(RUIN_SIZE):
            for y in range(RUIN_SIZE):
                if not self.visit[x][y]:
                    self.visit[x][y] = True
                    q = collections.deque([(x, y)])
                    trace = collections.deque([(x, y)])
                    while q:
                        cur = q.popleft()
                        for n in NEIGHBORS:
                            nx, ny = cur[0] + n[0], cur[1] + n[1]
                            if not self.is_wrong_coord(nx, ny) and self.board[nx][ny] == self.board[x][y] and not self.visit[nx][ny]:
                                q.append((nx, ny))
                                trace.append((nx, ny))
                                self.visit[nx][ny] = True
                    if len(trace) >= 3:
                        score += len(trace)
                        while (trace):
                            t = trace.popleft()
                            self.board[t[0]][t[1]] = 0
        return score
    
    def fill(self, que):
        for y in range(5):
            for x in range(4, -1, -1):
                if self.board[x][y] == 0:
                    self.board[x][y] = que.popleft()

    def chain(self, que):
        score = 0
        while True:
            self.init_visit()
            cur_score = self.calc_score()
            if cur_score == 0:
                break
            score += cur_score
            self.fill(que)
        return score


def rotation_stage(ruin):
    max_score = 0
    selected_ruin = None
    for r in [2, 4, 6]:
        for y in range(1, 4):
            for x in range(1, 4):
                new_ruin = ruin.rotate(x, y, r)
                score = new_ruin.calc_score()
                if score > max_score:
                    max_score = score
                    selected_ruin = new_ruin
    return max_score, selected_ruin


def main():
    k, m = map(int, input().split())
    initial_board = [list(map(int, input().split())) for i in range(5)]
    ruin = Ruin(initial_board)
    buff = collections.deque(map(int, input().split()))
    log = []
    for i in range(k):
        score, ruin = rotation_stage(ruin)
        if score == 0:
            break
        ruin.fill(buff)
        score += ruin.chain(buff)
        log.append(f"{score}")
    print(" ".join(log))


if __name__ == '__main__':
    main()