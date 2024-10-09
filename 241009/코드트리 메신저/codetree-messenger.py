import copy


class Chat_Tree():
    def __init__(self, n, data):
        self.pi_list = [0] + [data[1 + i] for i in range(n)]
        self.auth_list = [0] + [data[1 + n + i] for i in range(n)]
        self.alarm = [True] * (n + 1)
        self.children = [[None, None] for _ in range(n + 1)]
        for ci in range(1, n + 1):
            pi = self.pi_list[ci]
            if self.children[pi][0] is None:
                self.children[pi][0] = ci
            elif self.children[pi][1] is None:
                self.children[pi][1] = ci
            else:
                raise Exception("longer than 2")

    def change_alarm(self, ci):
        self.alarm[ci] = not self.alarm[ci]

    def change_authority(self, ci, power):
        self.auth_list[ci] = power

    def change_parent(self, ci1, ci2):
        pi1 = self.pi_list[ci1]
        pi2 = self.pi_list[ci2]
        # change parent id
        self.pi_list[ci1] = pi2
        self.pi_list[ci2] = pi1
        # next, change parent's child (relink)
        if self.children[pi1][0] == ci1:
            self.children[pi1][0] = ci2
        else:
            self.children[pi1][1] = ci2
        if self.children[pi2][0] == ci2:
            self.children[pi2][0] = ci1
        else:
            self.children[pi2][1] = ci1

    def count_alarm_reachable(self, ci):
        count = 0
        for child in self.children[ci]:
            if child is not None:
                count += self.dfs(child, 1)
        print(count)

    def dfs(self, ci, threshold):
        # check this chat can propagate alarm to parent
        if not self.alarm[ci]:
            return 0
        # count chat which can reach alarm to ci
        if self.auth_list[ci] < threshold:
            count = 0
        else:
            count = 1
        for child in self.children[ci]:
            if child is not None:
                count += self.dfs(child, threshold + 1)
        return count

    # def print_tree(self):
    #     for i in range(len(self.pi_list)):
    #         print(f"ci:{i} pi:{self.pi_list[i]} al:{self.alarm[i]} au:{self.auth_list[i]} c:{self.children[i]}")


def main():
    N, Q = list(map(int, input().split()))
    data = list(map(int, input().split()))
    assert data[0] == 100 and len(data) == 2 * N + 1
    tree = Chat_Tree(N, data)
    for i in range(Q - 1):
        data = list(map(int, input().split()))
        if data[0] == 200:
            tree.change_alarm(data[1])
        elif data[0] == 300:
            tree.change_authority(*data[1:])
        elif data[0] == 400:
            tree.change_parent(*data[1:])
        elif data[0] == 500:
            # tree.print_tree()
            tree.count_alarm_reachable(data[1])
        else:
            raise Exception("Invalid operation")


if __name__ == '__main__':
    main()