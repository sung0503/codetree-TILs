import heapq
from collections import defaultdict

INF = float('inf')
n, m = 0, 0
adj = []
cost = []
item_dict = defaultdict(int)

class Item:
    def __init__(self, item_id, revenue, dest):
        self.item_id = item_id
        self.revenue = revenue
        self.dest = dest
        self.profit = 0

        self.update_profit()

    def __lt__(self, other):
        if self.profit == other.profit:
            return self.item_id < other.item_id
        return self.profit > other.profit

    def update_profit(self):
        # revenue - cost
        global cost
        if cost[self.dest] == INF:
            self.profit = -1
        else:
            self.profit = self.revenue - cost[self.dest]

def dijkstra(start):
    global n, cost, adj
    cost = [INF] * n
    cost[start] = 0
    pq = [(0, start)]

    while pq:
        cur_cost, cur = heapq.heappop(pq)
        if cur_cost > cost[cur]:
            continue
        for nxt, w in adj[cur]:
            nxt_cost = cost[cur] + w
            if nxt_cost < cost[nxt]:
                cost[nxt] = nxt_cost
                heapq.heappush(pq, (nxt_cost, nxt))

def sell(pq):
    global item_dict

    while pq:
        if pq[0].profit < 0:
            break
        item = heapq.heappop(pq)
        if item_dict[item.item_id] == 1:
            return item.item_id
    return -1

def update_item(pq):
    global cost
    for i in range(len(pq)):
        pq[i].update_profit()
    heapq.heapify(pq)

def main():
    global Q, n, m, adj, cost, item_dict
    Q = int(input())
    cmds = list(map(int, input().split()))
    n, m = cmds[1], cmds[2]
    adj = [[] for _ in range(n)]
    for i in range(3, len(cmds), 3):
        v, u, w = cmds[i:i + 3]
        adj[v].append((u, w))
        adj[u].append((v, w))

    dijkstra(0)
    pq_item = []

    for _ in range(Q - 1):
        cmd = list(map(int, input().split()))
        if cmd[0] == 200:
            _, item_id, revenue, dest = cmd
            item = Item(item_id, revenue, dest)
            heapq.heappush(pq_item, item)
            item_dict[item_id] = 1
                
        elif cmd[0] == 300:
            _, item_id = cmd
            item_dict[item_id] = 0
        elif cmd[0] == 400:
            ret = sell(pq_item)
            print(ret)
        elif cmd[0] == 500:
            _, s = cmd
            dijkstra(s)
            update_item(pq_item)
        #print(item_dict)

if __name__ == '__main__':
    main()