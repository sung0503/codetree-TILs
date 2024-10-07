import collections
import copy
import heapq


LOOKS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
ROT = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]


def is_wrong_coord(x, y):
    return x < 0 or 4 < x or y < 0 or 4 < y


def is_right_center(x, y):
    return 0 < x < 4 and 0 < y < 4


def make_check_board(board):
    check_board = [[0] * 5 for i in range(5)]
    is_unchecked = 1
    for i in range(5):
        for j in range(5):
            if (check_board[i][j] == 1):
                for l in LOOKS:
                    if is_wrong_coord(i + l[0], j + l[1]):
                        continue
                    if (board[i + l[0]][j + l[1]] == board[i][j]):
                        check_board[i + l[0]][j + l[1]] = 1
            else:
                same = 0
                for l in LOOKS:
                    if is_wrong_coord(i + l[0], j + l[1]):
                        continue
                    if (board[i + l[0]][j + l[1]] == board[i][j]):
                        same += 1
                if same >= 2:
                    is_unchecked = 0
                    check_board[i][j] = 1
                    for l in LOOKS:
                        if is_wrong_coord(i + l[0], j + l[1]):
                            continue
                        if (board[i + l[0]][j + l[1]] == board[i][j]):
                            check_board[i + l[0]][j + l[1]] = 1
    return check_board, is_unchecked


def calc_score(board):
    check_board, is_unchecked = make_check_board(board)
    if is_unchecked:
        return 0
    score = 0
    for i in range(5):
        for j in range(5):
            if check_board[i][j] == 1:
                score += 1
    return score


def make_rotated_board(board, x, y, rot):
    assert rot == 2 or rot == 4 or rot == 6
    new_board = copy.deepcopy(board)
    for i, (ori_i, ori_j) in enumerate(ROT):
        rot_i, rot_j = ROT[(i + rot) % 8]
        new_board[x + rot_i][y + rot_j] = board[x + ori_i][y + ori_j]
    return new_board


def make_final_selected_board(board):
    max_score = 0
    selected_board = None
    for r in [2, 4, 6]:
        for y in range(1, 4):
            for x in range(1, 4):
                new_board = make_rotated_board(board, x, y, r)
                score = calc_score(new_board)
                if score > max_score:
                    max_score = score
                    selected_board = new_board
    return selected_board


def do_update(board, check_board, buff):
    score = 0
    for j in range(5):
        for i in range(4, -1, -1):
            if check_board[i][j] == 1:
                score += 1
                board[i][j] = buff.popleft()
    return score


def chain_rule(board, buff):
    final_score = 0
    while True:
        check_board, is_unchecked = make_check_board(board)
        if is_unchecked:
            break
        score = do_update(board, check_board, buff)
        final_score += score
    return final_score


def main():
    k, m = map(int, input().split())
    initial_board = [list(map(int, input().split())) for i in range(5)]
    buff = collections.deque(map(int, input().split()))
    current_board = initial_board
    score = []
    for i in range(k):
        selected_board = make_final_selected_board(current_board)
        if selected_board == None:
            break
        score.append(f"{chain_rule(selected_board, buff)}")
        current_board = selected_board
    print(" ".join(score))


if __name__ == '__main__':
    main()