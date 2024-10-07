# import heapq


# MAX_INT = 2**31 - 1


# class Tour():
#     def __init__(self, n, m, arr):
#         self.n = n
#         self.m = m
#         self.connection = [[] for _ in range(n)]
#         for i in range(m):
#             s, d, w = arr[i*3], arr[i*3 + 1], arr[i*3 + 2]
#             self.connection[s].append((d, w))
#             self.connection[d].append((s, w))
#         self.cost = []
#         self.update_cost(0)
#         self.products = {}
#         self.minheap = []
#         self.product_ids = set()

#     def update_cost(self, src):
#         self.cost = [MAX_INT] * self.n
#         self.cost[src] = 0
#         pq = [(0, src)]
#         while pq:
#             cur_cost, cur = heapq.heappop(pq)
#             if cur_cost > self.cost[cur]:
#                 continue
#             for nxt, w in self.connection[cur]:
#                 nxt_cost = self.cost[cur] + w
#                 if nxt_cost < self.cost[nxt]:
#                     self.cost[nxt] = nxt_cost
#                     heapq.heappush(pq, (nxt_cost, nxt))

#     def new_product(self, idx, rev, dst):
#         profit = rev - self.cost[dst]
#         self.products[idx] = (rev, dst)
#         self.product_ids.add(idx)
#         if profit >= 0:
#             heapq.heappush(self.minheap, (-profit, idx))

#     def cancel(self, idx):
#         self.product_ids.discard(idx)

#     def sell(self):
#         while self.minheap:
#             m_p, idx = heapq.heappop(self.minheap)
#             if idx in self.product_ids:
#                 print(idx)
#                 self.product_ids.discard(idx)
#                 return
#         print(-1)

#     def change_src(self, src):
#         self.update_cost(src)
#         self.minheap = []
#         for idx in self.product_ids:
#             profit = self.products[idx][0] - self.cost[self.products[idx][1]]
#             if profit >= 0:
#                 # heapq.heappush(self.minheap, (-profit, idx))
#                 self.minheap.append((-profit, idx))
#         heapq.heapify(self.minheap)


# def main():
#     Q = int(input())
#     tour = None
#     for i in range(Q):
#         data = list(map(int, input().split()))
#         if data[0] == 100:
#             tour = Tour(data[1], data[2], data[3:])
#         elif data[0] == 200:
#             tour.new_product(data[1], data[2], data[3])
#         elif data[0] == 300:
#             tour.cancel(data[1])
#         elif data[0] == 400:
#             tour.sell()
#         elif data[0] == 500:
#             tour.change_src(data[1])
#         else:
#             print("ERROR")
#         # print(tour.cost)
#         # print(tour.minheap)


# if __name__ == '__main__':
#     main()


from collections import defaultdict
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
        self.cost = [MAX_INT] * n
        self.update_cost(0)
        self.products = defaultdict(lambda : None)
        self.minheap = []

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
        new_heap = []
        for m_p, idx in self.minheap:
            if self.products[idx] is None:
                continue
            new_heap.append((self.cost[self.products[idx][1]] - self.products[idx][0], idx))
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
        # print(tour.cost)
        # print(tour.minheap)


if __name__ == '__main__':
    main()