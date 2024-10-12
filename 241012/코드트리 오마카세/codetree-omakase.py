from collections import defaultdict
from collections import heapq


class Table():
    def __init__(self, l):
        self.L = l
        self.susi_dic = defaultdict(list) # key: name, val: list of susi's x ordered by minheap
        self.cur_time = 0
    
    def add_susi(self, x, name):
        heapq.heappush(susi_dic{name}, x)
    
    def add_customer(self, x, name, n):
        pass

    def move_time_to(self, t):
        pass

    def picture(self):
        pass


def main():
    L, Q = list(map(int, input().split()))
    table = Table(L)
    for i in range(Q):
        ip = list(map(int, input().split()))
        table.move_time_to(ip[1])
        if ip[0] == 100:
            add_susi(ip[2], i[3])
        elif ip[0] == 200:
            add_customer(ip[2], ip[3], ip[4])
        elif ip[0] == 300:
            table.picture()
        else:
            raise Exception("ERROR")


if __name__ == "__main__":
    main()