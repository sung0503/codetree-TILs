MAX_ID = 100005  # ID의 최대값입니다
MAX_DEPTH = 105  # 트리의 최대 깊이입니다
COLOR_MAX = 5

class Node:
    def __init__(self):
        self.id = 0
        self.color = 0
        self.lastUpdate = 0  # 노드가 추가 된 시점 혹은 가장 마지막으로 색깔 변경 명령이 주어진 시점입니다
        self.maxDepth = 0  # node가 가질 수 있는 최대 깊이입니다
        self.parentId = 0  # 부모노드의 id를 저장합니다
        self.childIds = []  # 자식노드의 id들을 저장합니다

# 점수 조회 명령을 간편히 구현하기 위한 class입니다
class ColorCount:
    def __init__(self):
        self.cnt = [0] * (COLOR_MAX + 1)

    def __add__(self, obj):
        res = ColorCount()
        for i in range(1, COLOR_MAX + 1):
            res.cnt[i] = self.cnt[i] + obj.cnt[i]
        return res

    # 서로다른 색의 개수의 제곱을 반환합니다
    def score(self):
        result = 0
        for i in range(1, COLOR_MAX + 1):
            result += 1 if self.cnt[i] else 0
        return result * result

nodes = [Node() for _ in range(MAX_ID)]
isRoot = [False] * MAX_ID

# 해당 node가 자식노드를 가질 수 있는지 확인합니다
# 해당 과정에서는 root까지 조상들을 각각 탐색하며 maxDepth를 확인합니다
def canMakeChild(curr, needDepth):
    if curr.id == 0:
        return True
    if curr.maxDepth <= needDepth:
        return False
    return canMakeChild(nodes[curr.parentId], needDepth + 1)

# curr 노드의 색깔 정보와 해당 색깔이 설정된 시간을 return 합니다.
# root에 도달할때까지 부모를 거슬러 올라가며 lastUpdate시간을 이용하여 현재 노드가 가져야하는 색깔을 계산합니다
def getColor(curr):
    if curr.id == 0:
        return 0, 0
    info = getColor(nodes[curr.parentId])  # root부터 내려온 색변화 정보를 가져옵니다
    if info[1] > curr.lastUpdate:
        return info
    else:
        return curr.color, curr.lastUpdate  # 나의 색 변화 정보가 가장 최신이라면 이것을 child에게 반환해줍니다.

def getBeauty(curr, color, lastUpdate):
    # root에서부터 내려온 색 정보보다 현재 노드의 색정보가 최신이라면 갱신합니다
    if lastUpdate < curr.lastUpdate:
        lastUpdate = curr.lastUpdate
        color = curr.color
    result = [0, ColorCount()]
    result[1].cnt[color] = 1
    for childId in curr.childIds:
        child = nodes[childId]
        # 각 자식이 이루는 SubTree에서의 점수와 color count 값을 가져옵니다
        subResult = getBeauty(child, color, lastUpdate)
        result[1] = result[1] + subResult[1]
        result[0] += subResult[0]
    result[0] += result[1].score()
    return result

if __name__ == "__main__":
    Q = int(input())
    # Q개의 query에 대해 명령을 수행합니다
    for i in range(1, Q + 1):
        query = list(map(int, input().split()))
        T = query[0]
        if T == 100:
            mId, pId, color, maxDepth = query[1:]
            # 부모의 Id가 -1인 경우 root노드입니다
            if pId == -1:
                isRoot[mId] = True
            # 현재 노드를 만드려는 위치에 노드를 만들 수 있는지 확인합니다
            if isRoot[mId] or canMakeChild(nodes[pId], 1):
                # node 정보를 기입해줍니다
                nodes[mId].id = mId
                nodes[mId].color = color
                nodes[mId].maxDepth = maxDepth
                nodes[mId].parentId = 0 if isRoot[mId] else pId
                nodes[mId].lastUpdate = i

                if not isRoot[mId]:
                    nodes[pId].childIds.append(mId)
        elif T == 200:
            mId, color = query[1:]
            # 색 변화 명령에 대해 lastUpdate를 갱신하여 lazy update를 가능하게 준비합니다.
            # 시간복잡도를 위하여 색 변화 명령에 대해 subtree에 모두 갱신하는 것이 아닌, 추후 get_color, get_beauty 명령에서 lazy한 계산 가능한 형태로 만듭니다.
            nodes[mId].color = color
            nodes[mId].lastUpdate = i
        elif T == 300:
            mId = query[1]
            # mId번 node가 가지는 색깔을 계산합니다
            print(getColor(nodes[mId])[0])
        elif T == 400:
            beauty = 0
            for i in range(1, MAX_ID):
                # root 노드들에 대해 점수를 계산합니다
                if isRoot[i]:
                    beauty += getBeauty(nodes[i], nodes[i].color, nodes[i].lastUpdate)[0]
            print(beauty)