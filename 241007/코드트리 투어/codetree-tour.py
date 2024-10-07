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
        self.products = []

    def cost(self, dst):
        return self.connection[self.src][dst]

    def new_product(self, idx, rev, dst):
        profit = rev - self.cost(dst)
        heapq.heappush(self.products, (-profit, idx, rev, dst))
    
    def cancel(self, idx):
        for p in self.products:
            if p[1] == idx:
                self.products.remove(p)
                heapq.heapify(self.products)
                return
    
    def sell(self):
        if not self.products or self.products[0][0] > 0:
            print(-1)
            return
        m_p, idx, rev, dst = heapq.heappop(self.products)
        print(idx)

    def change_src(self, src):
        self.src = src
        new_products = []
        for p, idx, rev, dst in self.products:
            new_products.append((self.cost(dst) - rev, idx, rev, dst))
        heapq.heapify(new_products)
        self.products = new_products


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


if __name__ == '__main__':
    main()