# empty = -1
# rudolph = -2
# santa = Pi

R_dir = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]
S_dir = [(-1,0), (0,1), (1,0), (0,-1)]

class Game():
    def __init__(self, N, P, C, D, Rr, Rc):
        self.n = N
        self.board = [[-1] * N for _ in range(N)]
        self.Rr = Rr - 1
        self.Rc = Rc - 1
        self.board[self.Rr][self.Rc] = -2
        self.santas = [None] * P
        for _ in range(P):
            Pi, Sr, Sc = list(map(int, input().split()))
            Pi -= 1
            Sr -= 1
            Sc -= 1
            self.board[Sr][Sc] = Pi
            self.santas[Pi] = (Sr, Sc)
        self.is_active = [True] * P
        self.is_sturn = [0] * P
        self.count_active = P
        self.score= [0] * P
        self.Rpw = C
        self.Spw = D
    
    def recover_sturn(self):
        for i in range(len(self.is_sturn)):
            if self.is_sturn[i] > 0:
                self.is_sturn[i] -= 1

    def distance(self, Sr, Sc):
        return (self.Rr-Sr)*(self.Rr-Sr) + (self.Rc-Sc)*(self.Rc-Sc)

    def distance_r(self, Rr, Rc, Sr, Sc):
        return (Rr-Sr)*(Rr-Sr) + (Rc-Sc)*(Rc-Sc)
    
    def is_invalid(self, r, c):
        return r < 0 or r >= self.n or c < 0 or c >= self.n
    
    def is_unmoveable_santa(self, r, c):
        return self.is_invalid(r, c) or self.board[r][c] >= 0
   
    def rudolph_direction(self, Sr, Sc):
        global R_dir
        cur_dis = self.distance(Sr, Sc)
        next_dir = None
        for d in R_dir:
            new_dis = self.distance_r(self.Rr + d[0], self.Rc + d[1], Sr, Sc)
            if new_dis < cur_dis:
                cur_dis = new_dis
                next_dir = d
        assert next_dir is not None
        return next_dir

    def santa_direction(self, Sr, Sc):
        global S_dir
        cur_dis = self.distance(Sr, Sc)
        next_dir = None
        for d in S_dir:
            new_Sr, new_Sc = Sr + d[0], Sc + d[1]
            if self.is_unmoveable_santa(new_Sr, new_Sc):
                continue
            new_dis = self.distance(new_Sr, new_Sc)
            if new_dis < cur_dis:
                cur_dis = new_dis
                next_dir = d
        # nextdir maybe None
        return next_dir

    def higher_priority(self, Sr1, Sc1, Sr2, Sc2):
        assert Sr1 != Sr2 or Sc1 != Sc2
        # return True if S2 is higher
        if Sr1 < Sr2:
            return True
        elif Sr1 > Sr2:
            return False
        else:
            return Sc1 < Sc2
    
    def hit_santa(self, Si, power, Dr, Dc):
        self.is_sturn[Si] = 2
        self.chain(Si, power, Dr, Dc)
    
    def chain(self, Si, power, Dr, Dc):
        santa = self.santas[Si]
        self.board[santa[0]][santa[1]] = -1
        NSr, NSc = santa[0] + Dr * power, santa[1] + Dc * power
        if self.is_invalid(NSr, NSc):
            self.is_active[Si] = False
            self.count_active -= 1
            return
        if self.board[NSr][NSc] != -1:
            assert self.board[NSr][NSc] != -2
            self.chain(self.board[NSr][NSc], 1, Dr, Dc)
        self.board[NSr][NSc] = Si
        self.santas[Si] = (NSr, NSc)

    def rudolph_stage(self):
        nearest_santa = None
        new_dist = 5001
        for Si, cur_santa in enumerate(self.santas):
            if not self.is_active[Si]:
                continue
            cur_dist = self.distance(*cur_santa)
            if cur_dist < new_dist or (cur_dist == new_dist and self.higher_priority(*nearest_santa, *cur_santa)):
                # dist is shorter
                # or dist is same but priority is higher
                new_dist = cur_dist
                nearest_santa = cur_santa
        direction = self.rudolph_direction(*nearest_santa)
        # print(direction)
        #update
        self.board[self.Rr][self.Rc] = -1
        self.Rr += direction[0]
        self.Rc += direction[1]
        if self.board[self.Rr][self.Rc] != -1:
            # rudolph hit santa, throw santa
            Si = self.board[self.Rr][self.Rc]
            self.score[Si] += self.Rpw
            self.hit_santa(Si, self.Rpw, *direction)
        self.board[self.Rr][self.Rc] = -2

    def sanata_stage(self):
        for Si in range(len(self.santas)):
            if not self.is_active[Si]:
                continue
            elif self.is_sturn[Si]:
                continue
            santa = self.santas[Si]
            d = self.santa_direction(*santa)
            if d is None:
                continue
            # print(Si, santa, d)
            # update board
            next_Sr, next_Sc = santa[0] + d[0], santa[1] + d[1]
            if self.Rr == next_Sr and self.Rc == next_Sc:
                self.score[Si] += self.Spw
                self.hit_santa(Si, self.Spw - 1, -d[0], -d[1])
            else:
                self.board[santa[0]][santa[1]] = -1
                self.board[next_Sr][next_Sc] = Si
                self.santas[Si] = (next_Sr, next_Sc)
            # self.print_status()

    def survive(self):
        for i in range(len(self.score)):
            if(self.is_active[i]):
                self.score[i] += 1

    def play(self):
        self.recover_sturn()
        self.rudolph_stage()
        # self.print_status()
        self.sanata_stage()
        self.survive()
        # self.print_status()

    # def print_status(self):
    #     print(self.Rr, self.Rc)
    #     print(self.santas)
    #     print(self.is_active)
    #     print(self.is_sturn)
    #     print(self.score)
    #     for l in self.board:
    #         for i in l:
    #             if i == -1:
    #                 print(" ", end=', ')
    #             elif i == -2:
    #                 print("R", end=', ')
    #             else:
    #                 print(i, end = ', ')
    #         print()    
    #     print()
    
    def print_score(self):
        print(" ".join(str(i) for i in self.score))


def main():
    N, M, P, C, D = list(map(int, input().split()))
    Rr, Rc = list(map(int, input().split()))
    game = Game(N, P, C, D, Rr, Rc)
    # game.print_status()
    for m in range(M):
        # print(f"STAGE{m}")
        game.play()
        if game.count_active == 0:
            break
    game.print_score()


if __name__ == '__main__':
    main()