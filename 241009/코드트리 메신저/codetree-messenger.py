class Chat():
    def __init__(self, ci, pi, a):
        self.ci = ci
        self.pi = pi
        self.alarm = True # if false, don't propagate alarm to parent
        self.authority = a
        self.left = None
        self.right = None


class Chat_Tree():
    def __init__(self, n, pi_arr, au_arr):
        self.chat_list = [None] * (n + 1)
        self.chat_list[0] = Chat(0, 0, 0)
        for i, (pi, au) in enumerate(zip(pi_arr, au_arr)):
            parent = self.chat_list[pi]
            chat = Chat(i + 1, pi, au)
            self.chat_list[i + 1] = chat
            if parent.left is None:
                parent.left = chat.ci
            elif parent.right is None:
                parent.right = chat.ci
            else:
                raise Exception("longer than 2")

    def change_alarm(self, ci):
        chat = self.chat_list[ci]
        chat.alarm = not chat.alarm

    def change_authority(self, ci, power):
        chat = self.chat_list[ci]
        chat.authority = power

    def get_pi(self, ci):
        return self.chat_list[ci].pi

    def change_parent(self, c1, c2):
        p1 = self.chat_list[c1].pi
        p2 = self.chat_list[c2].pi
        if self.chat_list[p1].left == c1:
            self.chat_list[p1].left = c2
        else:
            self.chat_list[p1].right = c2
        if self.chat_list[p2].left == c2:
            self.chat_list[p2].left = c1
        else:
            self.chat_list[p2].right = c1

    def count_alarm_reachable(self, c):
        print(self.dfs(c, 0) - 1)

    def dfs(self, ci, threshold):
        # check this chat can propagate alarm to parent
        chat = self.chat_list[ci]
        if not chat.alarm or chat.authority < threshold:
            return 0
        # count chat which can reach alarm to ci
        count = 1
        if chat.left is not None:
            count += self.dfs(chat.left, threshold + 1)
        if chat.right is not None:
            count += self.dfs(chat.right, threshold + 1)
        return count

    def print_tree(self):
        for chat in self.chat_list:
            print(f"pi:{chat.pi} ci:{chat.ci} al:{chat.alarm} au:{chat.authority} l:{chat.left} r:{chat.right}")


def main():
    N, Q = list(map(int, input().split()))
    data = list(map(int, input().split()))
    assert data[0] == 100 and len(data) == 2 * N + 1
    tree = Chat_Tree(N, data[1: N + 1], data[N + 1:])
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