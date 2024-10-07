from collections import defaultdict
import heapq


MAX_INT = 2**31 - 1


class Tour():
    def __init__(self, n, m, arr):
        self.src = 0
        self.connection = [[MAX_INT] * n for _ in range(n)]
        for i in range(n):
            self.connection[i][i] = 0
        for i in range(m):
            s, d, w = arr[i*3], arr[i*3 + 1], arr[i*3 + 2]
            if w < self.connection[s][d]:
                self.connection[s][d] = w
                self.connection[d][s] = w
        for k in range(n):
            for src in range(n):
                for dst in range(n):
                    self.connection[src][dst] = min(self.connection[src][dst], self.connection[src][k] + self.connection[k][dst])
        self.products = defaultdict(lambda : None)
        self.minheap = []

    def cost(self, dst):
        return self.connection[self.src][dst]

    def new_product(self, idx, rev, dst):
        profit = rev - self.cost(dst)
        self.products[idx] = (rev, dst)
        heapq.heappush(self.minheap, (-profit, idx))
    
    def cancel(self, idx):
        self.products[idx] = None
        for i, p in enumerate(self.minheap):
            if p[1] == idx:
                self.minheap[i] = (p[0], -1) #removed flag
                return
    
    def sell(self):
        if not self.minheap or self.minheap[0][0] > 0:
            print(-1)
            return
        while True:
            if self.minheap[0][0] > 0:
                print(-1)
                return
            m_p, idx = heapq.heappop(self.minheap)
            if idx != -1:
                self.products[idx] = None
                break
        print(idx)

    def change_src(self, src):
        self.src = src
        new_heap = []
        for m_p, idx in self.minheap:
            new_heap.append((self.cost(self.products[idx][1]) - self.products[idx][0], idx))
        heapq.heapify(new_heap)
        self.minheap = new_heap


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
        # print(tour.products)
        # print(tour.minheap)


if __name__ == '__main__':
    main()