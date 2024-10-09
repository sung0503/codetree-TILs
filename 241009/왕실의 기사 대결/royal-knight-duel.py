from collections import deque
import copy


class Knight():
    def __init__(self, kid, r, c, h, w, k):
        self.kid = kid
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.life = k
        self.damage = 0


class Fight():
    def __init__(self, L, N):
        self.L = L
        self.board = [[2] * (L + 2) for _ in range(L + 2)]
        self.board_knights = [[0] * (L + 2) for _ in range(L + 2)]
        self.knights = [None * (N + 1)]
        self.direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def init_board(self, data):
        for i in range(self.L):
            for j in range(self.L):
                self.board[1 + i][1 + j] = data[i][j]

    def new_knight(self, knight):
        kid = knight.kid
        self.knights[kid] = knight
        r = knight.r
        c = knight.c
        h = knight.h
        w = knight.w
        for i in range(h):
            for j in range(w):
                self.board_knights[r + i][c + j] = kid

    def push(self, kid, d):
        if self.knights[kid] is None:
            return
        que = deque([kid])
        buff = set()
        r_m, c_m = self.direction[d]
        # using bfs, move if move is possible, else, do nothing.
        while que:
            cur_id = que.popleft()
            neighbor = []
            # print(cur_id)
            # print(neighbor)
            r = self.knights[cur_id].r
            c = self.knights[cur_id].c
            h = self.knights[cur_id].h
            w = self.knights[cur_id].w
            if d == 0:      # up
                for j in range(self.knights[cur_id].w):
                    if self.board[r - 1][c + j] == 2:
                        # check moveable
                        return
                    nid = self.board_knights[r - 1][c + j]
                    if nid == 0 or nid in buff:
                        continue
                    neighbor.append(nid)
            elif d == 2:    # down
                for j in range(self.knights[cur_id].w):
                    if self.board[r + h][c + j] == 2:
                        # check moveable
                        return
                    nid = self.board_knights[r + h][c + j]
                    if nid == 0 or nid in buff:
                        continue
                    neighbor.append(nid)
            elif d == 1:    # right
                for i in range(self.knights[cur_id].h):
                    if self.board[r + i][c + w] == 2:
                        # check moveable
                        return
                    nid = self.board_knights[r + i][c + w]
                    if nid == 0 or nid in buff:
                        continue
                    neighbor.append(nid)
            elif d == 3:    # left
                for i in range(self.knights[cur_id].h):
                    if self.board[r + i][c - 1] == 2:
                        # check moveable
                        return
                    nid = self.board_knights[r + i][c - 1]
                    if nid == 0 or nid in buff:
                        continue
                    neighbor.append(nid)
            else:           # error
                raise NotImplementedError("Undefined move direction")
            # get all neighbor knigts & remove dup
            n_set = set(neighbor)
            for nid in n_set:
                que.append(nid)
                buff.add(nid)
        # update knight status
        # print("update phase")
        for nid in buff:
            self.remove_from_board_knights(nid)
            self.knights[nid].r += r_m
            self.knights[nid].c += c_m
        for nid in buff
            # update damage of each moved knight
            self.update_damage(nid)
            if self.knights[nid].damage >= self.knights[nid].life:
                self.knights[nid] = None
            else:
                self.add_to_board_knights(nid)
        self.remove_from_board_knights(kid)
        self.knights[kid].r += r_m
        self.knights[kid].c += c_m
        self.add_to_board_knights(kid)
        # no update for first knight
    
    def remove_from_board_knights(self, kid):
        knight = self.knights[kid]
        r = knight.r
        c = knight.c
        h = knight.h
        w = knight.w
        for i in range(h):
            for j in range(w):
                self.board_knights[r + i][c + j] = 0
    
    def add_to_board_knights(self, kid):
        knight = self.knights[kid]
        r = knight.r
        c = knight.c
        h = knight.h
        w = knight.w
        for i in range(h):
            for j in range(w):
                self.board_knights[r + i][c + j] = kid
    
    def update_damage(self, kid):
        # update knight instance
        knight = self.knights[kid]
        r = knight.r
        c = knight.c
        dm = 0
        for i in range(knight.h):
            for j in range(knight.w):
                if self.board[r + i][c + j] == 1:
                    dm += 1
        knight.damage += dm

    def calc_total_damage(self):
        total_damage = 0
        for k in self.knights:
            if k is not None:
                total_damage += k.damage
        return total_damage
    
    def print_status(self):
        for l in self.board:
            print(l)
        self.print_board()

    def print_board(self):
        print()
        for l in self.board_knights:
            print(l)


def main():
    L, N, Q = list(map(int, input().split()))
    game = Fight(L)
    data = [list(map(int, input().split())) for _ in range(L)]
    game.init_board(data)
    for n in range(N):
        knight = Knight(n + 1, *map(int, input().split()))
        game.new_knight(knight)

    # game.print_status()

    for _ in range(Q):
        game.push(*map(int, input().split()))
        # game.print_board()

    print(game.calc_total_damage())


if __name__=='__main__':
    main()