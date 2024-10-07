from collections import defaultdict
import heapq


MAX_INT = 2**31 - 1


class Tour():
    def __init__(self, n, m, arr):
        self.n = n
        self.m = m
        self.connection = [[MAX_INT] * n for _ in range(n)]
        for i in range(n):
            self.connection[i][i] = 0
        for i in range(m):
            s, d, w = arr[i*3], arr[i*3 + 1], arr[i*3 + 2]
            if w < self.connection[s][d]:
                self.connection[s][d] = w
                self.connection[d][s] = w
        self.cost = [MAX_INT] * n
        self.update_cost(0)
        self.products = defaultdict(lambda : None)
        self.minheap = []

    def update_cost(self, src):
        self.cost = [MAX_INT] * self.n
        visit = [False for _ in range(self.n)]
        cur = src
        self.cost[src] = 0
        while (sum(visit) < self.n - 1): #when last
            visit[cur] = True
            buff = []
            for i in range(self.n):
                if not visit[i]:
                    if self.cost[i] > self.cost[cur] + self.connection[cur][i]:
                        self.cost[i] = self.cost[cur] + self.connection[cur][i]
                    heapq.heappush(buff, (self.cost[i], i))
            _c, cur = heapq.heappop(buff)

    def new_product(self, idx, rev, dst):
        profit = rev - self.cost[dst]
        self.products[idx] = (rev, dst)
        heapq.heappush(self.minheap, (-profit, idx))
    
    def cancel(self, idx):
        self.products[idx] = None
        # for i, p in enumerate(self.minheap):
        #     if p[1] == idx:
        #         self.minheap[i] = (p[0], -1) #removed flag
        #         return
    
    def sell(self):
        while True:
            if not self.minheap or self.minheap[0][0] > 0:
                print(-1)
                return
            m_p, idx = heapq.heappop(self.minheap)
            if self.products[idx] is not None:
                break
        print(idx)

    def change_src(self, src):
        self.update_cost(src)
        # new_heap = []
        # for m_p, idx in self.minheap:
        #     if self.products[idx] is None:
        #         continue
        #     new_heap.append((self.cost[self.products[idx][1]] - self.products[idx][0], idx))
        for i in range(len(self.minheap)):
            if self.products[idx] is None:
                self.minheap[i] = (MAX_INT, idx)
            else:
                self.minheap[i] = (self.cost[self.products[idx][1]] - self.products[idx][0], idx)
        # heapq.heapify(new_heap)
        # self.minheap = new_heap
        heapq.heapify(self.minheap)


def main():
    Q = int(input())
    tour = None
    for i in range(Q):
        data = list(map(int, input().split()))
        if data[0] == 100:
            tour = Tour(data[1], data[2], data[3:])
        elif data[0] == 200:
            tour.new_product(data[1], data[2], data[3])
        elif data[0] == 300:
            tour.cancel(data[1])
        elif data[0] == 400:
            tour.sell()
        elif data[0] == 500:
            tour.change_src(data[1])
        else:
            print("ERROR")
        # print(tour.cost)
        # print(tour.minheap)


if __name__ == '__main__':
    main()