import heapq


MAX_INT = 2**31 - 1


class Tour():
    def __init__(self, n, m, arr):
        self.n = n
        self.m = m
        self.connection = [[] for _ in range(n)]
        for i in range(m):
            s, d, w = arr[i*3], arr[i*3 + 1], arr[i*3 + 2]
            self.connection[s].append((d, w))
            self.connection[d].append((s, w))
        self.cost = []
        self.update_cost(0)
        self.products = {}
        self.minheap = []
        self.product_ids = set()

    def update_cost(self, src):
        self.cost = [MAX_INT] * self.n
        self.cost[src] = 0
        pq = [(0, src)]
        while pq:
            cur_cost, cur = heapq.heappop(pq)
            if cur_cost > self.cost[cur]:
                continue
            for nxt, w in self.connection[cur]:
                nxt_cost = self.cost[cur] + w
                if nxt_cost < self.cost[nxt]:
                    self.cost[nxt] = nxt_cost
                    heapq.heappush(pq, (nxt_cost, nxt))

        # while (sum(visit) < self.n - 1): #when last
        #     visit[cur] = True
        #     buff = []
        #     for i in range(self.n):
        #         if not visit[i]:
        #             if self.cost[i] > self.cost[cur] + self.connection[cur][i]:
        #                 self.cost[i] = self.cost[cur] + self.connection[cur][i]
        #             heapq.heappush(buff, (self.cost[i], i))
        #     _c, cur = heapq.heappop(buff)

    def new_product(self, idx, rev, dst):
        profit = rev - self.cost[dst]
        self.products[idx] = (rev, dst)
        self.product_ids.add(idx)
        if profit >= 0:
            heapq.heappush(self.minheap, (-profit, idx))
    
    def cancel(self, idx):
        self.product_ids.discard(idx)
    
    def sell(self):
        while self.minheap:
            m_p, idx = heapq.heappop(self.minheap)
            if idx in self.product_ids:
                print(idx)
                self.product_ids.discard(idx)
                return
        print(-1)

    def change_src(self, src):
        self.update_cost(src)
        self.minheap = []
        for idx in self.product_ids:
            profit = self.products[idx][0] - self.cost[self.products[idx][1]]
            if profit >= 0:
                # heapq.heappush(self.minheap, (-profit, idx))
                self.minheap.append((-profit, idx))
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