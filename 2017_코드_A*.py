# -*- coding: utf-8 -*-
import math


# AlphaBeta, GameTree, GameNode class modify from https://tonypoer.io/2016/10/28/

class AlphaBeta:
    def __init__(self, game_tree, AI_turn):
        self.game_tree = game_tree
        self.root = game_tree.root
        self.AIturn = AI_turn
        return

    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print "AlphaBeta : Utility Value of Root Node = " + str(best_val)
        print "AlphaBeta : Best State is : " + best_state.name
        return best_state.name

    def max_value(self, node, alpha, beta):
        print "AlphaBeta-->MAX : Visited Node :: " + node.name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        print "AlphaBeta-->MIN : Visited Node :: " + node.name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def check_input(self):
        count = [0, 0, 0, 0, 0, 0, 0]
        max = 1

        for x in range(len(self.gridInfo) - 1):
            count[self.gridInfo[x]] += 1

            if max(count) > 6:
                return False
        return True

    def getUtility(self, node):
        assert node is not None

        gridInfo = node.name
        former = 'F'
        latter = 'L'
        ch = self.AIturn

        count = [0, 0, 0, 0, 0, 0, 0]

        grid = [[' ' for col in range(7)] for row in range(6)]

        for x in range(len(gridInfo) - 1):
            count[int(gridInfo[x])] += 1

            if max(count) > 6:
                return 0

        for x in range(0, len(gridInfo)):
            idx = int(gridInfo[x])
            # get index where to put
            for row in range(0, 6):
                if grid[5 - row][idx] == ' ':
                    if x % 2 == 0:  # former's turn
                        grid[5 - row][idx] = former
                    else:  # later's turn
                        grid[5 - row][idx] = latter
                    break

        for iteration in range(0, 2):
            if iteration == 0:
                under = 4.5
            else:
                if ch == 'F':
                    ch = 'L'
                    under = 4.7
                else:
                    ch = 'F'
                    under = 4.7
                    ###################################################
            row_score = 0
            for row in range(6):
                for start in range(4):
                    count = 0
                    for x in range(4):
                        if grid[row][start + x] != ch and grid[row][start + x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if grid[row][start + x] == ch:
                            count = count + 1
                            # count character number
                    if count < 0:
                        score = 0
                    elif count == 0:
                        score = 1
                    else:
                        score = math.pow(under, count)
                    # give score to 4 space set
                    row_score = row_score + score
                    # iterate in row
            # iterate by row
            print "row_score:", row_score
            # column
            col_score = 0
            for col in range(7):
                for start in range(3):
                    count = 0
                    for x in range(4):
                        if grid[start + x][col] != ch and grid[start + x][col] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if grid[start + x][col] == ch:
                            count = count + 1
                            # count character number
                    if count < 0:
                        score = 0
                    else:
                        score = math.pow(under, count)
                    # give score to 4 space set
                    col_score = col_score + score
                    # iterate in col
            # iterate by col
            print "col_score:", col_score
            # right diagonal
            rd_score = 0
            for row in range(3, 6):
                for start in range(3):
                    count = 0
                    for x in range(4):
                        if row - start - x < 0 or start + x > 6:
                            count = -1
                            break
                        if grid[row - start - x][start + x] != ch and grid[row - start - x][start + x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if grid[row - start - x][start + x] == ch:
                            count = count + 1
                            # count character number
                    if count < 0:
                        score = 0
                    else:
                        score = math.pow(under, count)
                    # give score to 4 space set
                    rd_score = rd_score + score
                    # iterate in row diagonally 3 4 5
            # iterate by row 3 4 5
            for col in range(1, 4):
                for start in range(3):
                    count = 0
                    for x in range(4):
                        if 5 - start - x < 0 or col + start + x > 6:
                            count = -1
                            break
                        if grid[5 - start - x][col + start + x] != ch and grid[5 - start - x][col + start + x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if grid[5 - start - x][col + start + x] == ch:
                            count = count + 1
                            # count character number
                    if count < 0:
                        score = 0
                    else:
                        score = math.pow(under, count)
                    # give score to 4 space set
                    rd_score = rd_score + score
                    # iterate in row diagonally 3 4 5
            # iterate by row 3 4 5
            print "rd_score:", rd_score
            # left diagonal
            ld_score = 0
            for row in range(3, 6):
                for start in range(3):
                    count = 0
                    for x in range(4):
                        if row - start - x < 0 or 6 - start - x < 0:
                            count = -1
                            break
                        if grid[row - start - x][6 - start - x] != ch and grid[row - start - x][6 - start - x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if grid[row - start - x][6 - start - x] == ch:
                            count = count + 1
                            # count character number
                    if count < 0:
                        score = 0
                    else:
                        score = math.pow(under, count)
                    # give score to 4 space set
                    ld_score = ld_score + score
                    # iterate in row diagonally 3 4 5
            # iterate by row 3 4 5
            for col in range(3, 7):
                for start in range(3):
                    count = 0
                    for x in range(4):
                        if 5 - start - x < 0 or col - start - x < 0:
                            count = -1
                            break
                        if grid[5 - start - x][col - start - x] != ch and grid[5 - start - x][col - start - x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if grid[5 - start - x][col - start - x] == ch:
                            count = count + 1
                            # count character number
                    if count < 0:
                        score = 0
                    else:
                        score = math.pow(under, count)
                    # give score to 4 space set
                    ld_score = ld_score + score
                    # iterate in row diagonally 3 4 5
            # iterate by row 3 4 5
            print "ld_score:", ld_score

            total_score = row_score + col_score + rd_score + ld_score
            if iteration == 0:
                my_score = total_score
            else:
                opponent_treat = total_score
        ###################################################
        total_score = my_score - opponent_treat
        print "my score : ", my_score
        print "opp treat : ", opponent_treat
        print total_score
        return total_score


class GameNode:
    def __init__(self, name, value=0, parent=None):
        self.name = name  # string
        self.value = value  # an int
        self.parent = parent  # a node reference
        self.children = []  # a list

    def addChild(self, childNode):
        self.children.append(childNode)


class GameTree:
    def __init__(self):
        self.root = None

    def build_tree(self, depth, initial_root, num_child=7):
        self.root = initial_root
        node_list = [self.root]

        parent_idx = 0
        check_list = ['0', '1', '2', '3', '4', '5', '6']
        check = True

        parent_num = 1
        parent_count = 0

        for d in range(depth):
            for p in range(parent_num):
                parent = node_list[parent_idx]
                for ind in range(num_child):
                    child_name = parent.name + str(ind)
                    for col in check_list:
                        if child_name.count(col) > 6:
                            check = False
                    if check:
                        new_node = GameNode(child_name, 0, parent)
                        parent.addChild(new_node)
                        node_list.append(new_node)
                        parent_count += 1
                    check = True
                parent_idx += 1
            parent_num = parent_count
            parent_count = 0

    def print_tree(self):
        node_list = [self.root]

        while len(node_list) != 0:
            new_list = []
            s = ""
            for c in node_list:
                new_list.extend(c.children)
                s += c.name + " "
            print s
            node_list = new_list


class Grid:
    def __init__(self):
        self.grid = [[' ' for col in range(7)] for row in range(6)]
        self.gridInfo = ''
        return

    def print_grid(self):
        print "----------------------"
        for row in range(6):
            print "|",
            for col in range(7):
                print self.grid[row][col] + "|",
            print
        print "----------------------"
        print self.gridInfo

    def put_by_force(self, col_num, ch):
        for row in range(5, -1, -1):
            if self.grid[row][col_num] == ' ':
                self.grid[row][col_num] = ch
                print ch
                return False
        return True

    def clear_grid(self):
        self.grid = [[' ' for col in range(7)] for row in range(6)]

    def remove_recent(self, col_num):
        for row in range(6):
            if self.grid[row][col_num] != ' ':
                self.grid[row][col_num] = ' '
                return False
        return True

    def by_my_advantage(self):
        stringlength = len(self.gridInfo)
        advantage = [0, 0, 0, 0, 0, 0, 0]
        gridcopy = self.grid


        if stringlength % 2 == 0:  # 지금까지 짝수번째 턴이었다면(이제 내가 놓아야함)
            char = "O"  # 현재 차례는 O(홀수) 차례
            oppchar = "X"
        else:
            char = "X"  # 현재 차례는 x(짝수) 차례
            oppchar = "O"

        gridCount = [self.gridInfo.count("0"), self.gridInfo.count("1"), self.gridInfo.count("2"),
                     self.gridInfo.count("3"),
                     self.gridInfo.count("4"),
                     self.gridInfo.count("5"), self.gridInfo.count("6")]  # 각 자리의 최대 인덱스를 구하는 리스트.

        OverGrid = [0, 0, 0, 0, 0, 0, 0]  # Grid(6개 이상 두는걸 예측 못하게!!!)를 넘어갈 경우를 대비한 리스트지용

        for i in range(0, 7):
            if gridCount[i] == 6:  # 만약 최대 인덱스가 6이면 해당 자리의 overgird를 1로 바꿈
                OverGrid[i] = 1
            else:
                OverGrid[i] = 0
        ##############################################################################################################
        ##############################################################################################################
        # row의 경우


        for k in range(0, 7):

            if OverGrid[k] == 1:  # 일단 해당 자리의 overgrid가 1이면 최대 인덱스가 6인 것이므로 재빨리 for문을 벗어난다. advantage는 -100으로 책정
                advantage[k] = -1000
                continue

            count = 0  # row에서 count는 내돌이 있는 자리. empty는 세지 않는다
            fourCount = 0  # 사실 가로는 이어져서 4여야만 connect4를 이룰 수 있으니까 빈칸, 내돌 4개까지만 체크하겠어용
            gridcopy[5 - gridCount[k]][k] = char  # 해당 자리의 돌을 끼얹는다....! 이제부터 이 자리를 기준으로 검사하겠음

            # column에서 emptycount가 있었는데 row는 걍 fourCount로 <내돌 + emptycount>까지 합쳤습니당

            for i in range(0, 7 - k):  # 둔 돌을 기준으로 오른쪽 탐색
                if fourCount == 4:  # 만약 4개를 둘 자리가 충만하다면 걍 점수매기러 바로 ㄱㄱ
                    break
                elif gridcopy[5 - gridCount[k]][k + i].count(char) == 1:  # 내 돌이라면
                    fourCount += 1
                    count += 1
                elif gridcopy[5 - gridCount[k]][k + i] == oppchar:  # 상대편 돌이라면
                    break
                else:  # 빈칸이라면
                    fourCount += 1

            for i in range(0, k):  # 둔 돌을 기준으로 왼쪽 탐색 (단 둔 돌은 제외한다. 오른쪽에서 이미 셌거든용)
                if fourCount == 4:
                    break
                elif gridcopy[5 - gridCount[k]][k - i - 1].count(
                        char) == 1:  # 왼쪽 탐색. 만약 내 돌이 없는 순간(빈칸or 상대편의 돌) 바로 정지+ 방금둔 돌까지 같이 셈
                    count += 1
                    fourCount += 1
                elif gridcopy[5 - gridCount[k]][k - i - 1] == oppchar:
                    break
                else:
                    fourCount += 1

            gridcopy[5 - gridCount[k]][k] = ' '  # 예측한 돌 초기화

            row_advantage = 0  # row advantage를 책정

            if fourCount < 4:
                row_advantage += 0
            elif fourCount >= 4 and count == 0:
                row_advantage += 1
            elif fourCount >= 4 and count == 1:
                row_advantage += 2
            elif count == 2 and fourCount >= 4:
                row_advantage += 4
            elif count == 3 and fourCount >= 4:
                row_advantage += 8
            elif count == 4 and fourCount >= 4:
                row_advantage += 1000
            else:
                row_advantage += 0

            advantage[k] += row_advantage  # row advantage를 해당 자리의 advantage에 저장 row끝




            ##############################################################################################################
            ##############################################################################################################
            # column의 경우

        for k in range(0, 7):

            if OverGrid[k] == 1:  # 일단 해당 자리의 overgrid가 1이면 최대 인덱스가 6인 것이므로 재빨리 for문을 벗어난다. advantage는 -100으로 책정
                advantage[k] = -1000
                continue
            count = 0
            emptycount = 0
            gridcopy[5 - gridCount[k]][k] = char

            # column
            for i in range(0, gridCount[k] + 1):
                if gridcopy[5 - gridCount[k] + i][k].count(char) == 1:
                    count += 1
                elif gridcopy[5 - gridCount[k] + i][k].count(char) != 1:  # 다른 돌이 있으면 탐색 종료
                    break

            for i in range(5 - gridCount[k]):
                emptycount += 1
            gridcopy[5 - gridCount[k]][k] = ' '

            col_advantage = 0
            if count == 0 and emptycount >= 4:
                col_advantage += 1
            if count == 1 and emptycount >= 3:
                col_advantage += 2
            elif count == 2 and emptycount >= 2:
                col_advantage += 4
            elif count == 3 and emptycount >= 1:
                col_advantage += 8
            elif count == 4 and emptycount >= 0:
                col_advantage += 1000
            else:
                col_advantage += 0

            advantage[k] += col_advantage



            ##############################################################################################################
            ##############################################################################################################
            # 대각선의 경우

        for k in range(0, 7):
            if OverGrid[k] == 1:  # 일단 해당 자리의 overgrid가 1이면 최대 인덱스가 6인 것이므로 재빨리 for문을 벗어난다. advantage는 -100으로 책정
                advantage[k] = -1000
                continue
            count1 = 0  # 대각선에서 count는 내돌이 있는 자리. empty는 세지 않는다 이 때 count1은 /방향    count2는 반대방향
            fourCount1 = 0  # 대각선도 이어져서 4여야만 connect4를 이룰 수 있으니까 빈칸, 내돌 4개까지만 체크하겠어용
            fourCount2 = 0
            count2 = 0
            gridcopy[5 - gridCount[k]][k] = char  # 내가 둘 자리

            up = 6 - gridCount[k]  # 내가 둘 돌 포함한 위쪽
            down = gridCount[k] + 1  # 내가 둘 돌 포함한 아래쪽
            right = 7 - k  # 내가 둘 돌 포함한 오른쪽
            left = k + 1  # 내가 둘 돌 포함한 왼쪽

            if up <= right:  # /방향 중에 위쪽 결정 : 이유는 grid 벗어나면 안되니까
                northeast = up
            else:
                northeast = right

            if down <= left:  # /방향 중에 아래쪽
                southwest = down
            else:
                southwest = left

            if up <= left:  # 반대방향 위쪽
                northwest = up
            else:
                northwest = left

            if down <= right:  # 반대방향 아래쪽
                southeast = down
            else:
                southeast = right

            # 대각선도 걍 fourCount로 내돌+emptycount까지 합쳤습니당
            # diagonal
            # /방향 대각선
            for i in range(0, northeast):
                if fourCount1 == 4:  # 만약 4개를 둘 자리가 충만하다면 걍 점수매기러 바로 ㄱㄱ
                    break
                elif gridcopy[5 - gridCount[k] - i][k + i].count(char) == 1:  # /쪽 위쪽 탐색
                    fourCount1 += 1
                    count1 += 1
                elif gridcopy[5 - gridCount[k] - i][k + i] == oppchar:
                    break
                else:
                    fourCount1 += 1

            for i in range(0, southwest - 1):  # /쪽 아래쪽 탐색
                if fourCount1 == 4:
                    break
                elif gridcopy[6 - gridCount[k] + i][k - i - 1].count(char) == 1:
                    count1 += 1
                    fourCount1 += 1
                elif gridcopy[6 - gridCount[k] + i][k - i - 1] == oppchar:
                    break
                else:
                    fourCount1 += 1

            for i in range(0, northwest):  # 반대쪽 위쪽 탐색
                if fourCount2 == 4:
                    break
                elif gridcopy[5 - gridCount[k] - i][k - i].count(char) == 1:
                    count2 += 1
                    fourCount2 += 1
                elif gridcopy[5 - gridCount[k] - i][k - i] == oppchar:
                    break
                else:
                    fourCount2 += 1

            for i in range(0, southeast - 1):  # 반대쪽 아래쪽 탐색
                if fourCount2 == 4:
                    break
                elif gridcopy[6 - gridCount[k] + i][k + i + 1].count(char) == 1:
                    count2 += 1
                    fourCount2 += 1
                elif gridcopy[6 - gridCount[k] + i][k + i + 1] == oppchar:
                    break
                else:
                    fourCount2 += 1

            gridcopy[5 - gridCount[k]][k] = ' '  # 내가 둘 곳 초기화

            # / 방향일 때 advantage
            di_advantage = 0
            if fourCount1 < 4:
                di_advantage += 0
            elif count1 == 0 and fourCount1 >= 4:
                di_advantage += 1
            elif count1 == 1 and fourCount1 >= 4:
                di_advantage += 2
            elif count1 == 2 and fourCount1 >= 4:
                di_advantage += 4
            elif count1 == 3 and fourCount1 >= 4:
                di_advantage += 8
            elif count1 == 4 and fourCount1 >= 4:
                di_advantage += 16
            else:
                di_advantage += 0

            advantage[k] += di_advantage

            # 반대 방향일 때 advantage
            di_advantage = 0
            if fourCount2 < 4:
                di_advantage += 0
            elif count2 == 0 and fourCount2 >= 4:
                di_advantage += 1
            elif count2 == 1 and fourCount2 >= 4:
                di_advantage += 2
            elif count2 == 2 and fourCount2 >= 4:
                di_advantage += 4
            elif count2 == 3 and fourCount2 >= 4:
                di_advantage += 8
            elif count2 == 4 and fourCount2 >= 4:
                di_advantage += 1000
            else:
                di_advantage += 0

            advantage[k] += di_advantage

        for k in range(0, 7):
            if OverGrid[k] == 1:  # 일단 해당 자리의 overgrid가 1이면 최대 인덱스가 6인 것이므로 재빨리 for문을 벗어난다. advantage는 -100으로 책정
                advantage[k] = -1000
                continue
            gridcopy[5 - gridCount[k]][k] = char
            opp_row_Advantage = 0
            for j in range(0, 6):  # 세로세기
                rowCount = 0  # 시작점 체크 count
                for n in range(0, 4):  # 가로 4칸씩 체크(시작점 : 0,1,2,3)
                    oppfourcount = 0  # 4개 확인 되었는지 체크
                    oppcount = 0  # 상대편이 4개 범위에서 둔 돌의 갯수
                    oppemptycount = [9, 9, 9, 9]  # 어느게 상대 4개 범위 중 empty공간인지.
                    oppemptycount_col = [0, 0, 0, 0]
                    for i in range(0, 4):  # 4칸 체크 (0~3, 1~4, 2~5, 3~6)
                        if gridcopy[5 - j][rowCount + i] == oppchar:
                            oppcount += 1
                            oppfourcount += 1
                        elif gridcopy[5 - j][rowCount + i] == char:
                            break
                        else:
                            oppfourcount += 1
                            oppemptycount[i] = rowCount + i  # 어느 부분이 empty인지 체크.... 세로 갯수를 셀거임.
                            for m in range(0, j + 1):
                                if gridcopy[5 - j - m][rowCount + i] != oppchar and gridcopy[5 - j - m][rowCount] != char:
                                    oppemptycount_col[i] += 1
                                else:
                                    break

                    if oppfourcount < 4:
                        opp_row_Advantage += 0
                    elif oppfourcount == 4 and oppcount == 2:
                        for i in range(0, 4):
                            if oppemptycount[i] != 9:
                                if oppemptycount_col[i] > 2:
                                    opp_row_Advantage += 4
                                elif oppemptycount_col[i] == 1 or oppemptycount_col[i] == 2:
                                    opp_row_Advantage += 8
                                else :
                                    opp_row_Advantage += 4
                    elif oppfourcount == 4 and oppcount == 3:
                        for i in range(0, 4):
                            if oppemptycount[i] != 9:
                                if oppemptycount_col[i] == 1:
                                    opp_row_Advantage += 16
                                else:
                                    opp_row_Advantage += 8
                    else:
                        opp_row_Advantage += 0

                    rowCount += 1
            gridcopy[5 - gridCount[k]][k] = ' '
            advantage[k] -= opp_row_Advantage


        for k in range(0, 7):
            if OverGrid[k] == 1:  # 일단 해당 자리의 overgrid가 1이면 최대 인덱스가 6인 것이므로 재빨리 for문을 벗어난다. advantage는 -100으로 책정
                advantage[k] = -1000
                continue
            gridcopy[5 - gridCount[k]][k] = char
            opp_col_Advantage = 0
            for j in range(0, 7):  # 가로세기
                emptycount = 0
                oppcount = 0
                for i in range(0, 6):
                    if gridcopy[5 - i][j] == oppchar:
                        oppcount += 1
                    elif gridcopy[5 - i][j] == char:
                        oppcount = 0
                    else:
                        emptycount = 6 - i
                        break
                if oppcount == 0:
                    opp_col_Advantage += 0
                elif oppcount == 2 and emptycount >= 2:
                    opp_col_Advantage += 8
                elif oppcount == 3 and emptycount >= 1:
                    opp_col_Advantage += 64
                else:
                    opp_col_Advantage += 0
            gridcopy[5 - gridCount[k]][k] = ' '
            advantage[k] -= opp_col_Advantage



        for k in range(0, 7):
            if OverGrid[k] == 1:  # 일단 해당 자리의 overgrid가 1이면 최대 인덱스가 6인 것이므로 재빨리 for문을 벗어난다. advantage는 -100으로 책정
                advantage[k] = -1000
                continue
            gridcopy[5 - gridCount[k]][k] = char
            opp_diagonal_Advantage = 0
            rd_score = 0
            for row in range(3, 6):
                for start in range(3):
                    count = 0
                    emptycount = 0
                    for x in range(4):
                        if row - start - x < 0 or start + x > 6:
                            count = -1
                            break
                        if gridcopy[row - start - x][start + x] != oppchar and gridcopy[row - start - x][start + x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if gridcopy[row - start - x][start + x] == oppchar:
                            count = count + 1
                        elif gridcopy[row - start - x][start + x] == ' ':
                            if row - start - x == 5:
                                emptycount += 1
                            elif gridcopy[row - start - x + 1][start + x] == oppchar or gridcopy[row - start - x + 1][
                                        start + x] == char:
                                emptycount += 1
                            else:
                                emptycount += 0
                                # count character number
                    if count < 0:
                        oppscore = 0
                    elif count == 3 and emptycount == 1:
                        oppscore = 64
                    elif count == 2 and emptycount == 2:
                        oppscore = 64
                    else:
                        oppscore = 0
                    # give score to 4 space set
                    rd_score = rd_score + oppscore
                    # iterate in row diagonally 3 4 5
            # iterate by row 3 4 5
            for col in range(1, 4):
                for start in range(3):
                    emptycount = 0
                    count = 0
                    for x in range(4):
                        if 5 - start - x < 0 or col + start + x > 6:
                            count = -1
                            break
                        if gridcopy[5 - start - x][col + start + x] != oppchar and gridcopy[5 - start - x][
                                            col + start + x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if gridcopy[5 - start - x][col + start + x] == oppchar:
                            count = count + 1
                        elif gridcopy[5 - start - x][col + start + x] == ' ':
                            if 5 - start - x == 5:
                                emptycount += 1
                            elif gridcopy[5 - start - x + 1][col + start + x] == oppchar or gridcopy[5 - start - x + 1][
                                                col + start + x] == char:
                                emptycount += 1
                            else:
                                emptycount += 0
                                # count character number
                    if count < 0:
                        oppscore = 0
                    elif count == 3 and emptycount == 1:
                        oppscore = 64
                    elif count == 2 and emptycount == 1:
                        oppscore = 32
                    elif count == 2 and emptycount == 2:
                        oppscore = 64
                    else:
                        oppscore = 0
                    # give score to 4 space set
                    rd_score = rd_score + oppscore
                    # iterate in row diagonally 3 4 5
            # iterate by row 3 4 5
            # print "rd_score:", rd_score
            # left diagonal
            ld_score = 0
            for row in range(3, 6):
                for start in range(3):
                    emptycount = 0
                    count = 0
                    for x in range(4):
                        if row - start - x < 0 or 6 - start - x < 0:
                            count = -1
                            break
                        if gridcopy[row - start - x][6 - start - x] != oppchar and gridcopy[row - start - x][
                                            6 - start - x] != ' ':
                            count = -1
                            break
                        # if there is one opponent character in 4 space set, no score
                        if gridcopy[row - start - x][6 - start - x] == oppchar:
                            count = count + 1
                        elif gridcopy[row - start - x][6 - start - x] == ' ':
                            if row - start - x == 5:
                                emptycount += 1
                            elif gridcopy[row - start - x + 1][6 - start - x] == oppchar or gridcopy[row - start - x + 1][
                                                6 - start - x] == char:
                                emptycount += 1
                            else:
                                emptycount += 0
                                # count character number
                    if count < 0:
                        oppscore = 0
                    elif count == 3 and emptycount == 1:
                        oppscore = 64
                    elif count == 2 and emptycount == 2:
                        oppscore = 64
                    else:
                        oppscore = 0
                    # give score to 4 space set
                    ld_score = ld_score + oppscore
                    # iterate in row diagonally 3 4 5
                    # iterate by row 3 4 5
                    for col in range(3, 7):
                        for start in range(3):
                            emptycount = 0
                            count = 0
                            for x in range(4):
                                if 5 - start - x < 0 or col - start - x < 0:
                                    count = -1
                                    break
                                if gridcopy[5 - start - x][col - start - x] != oppchar and gridcopy[5 - start - x][
                                                    col - start - x] != ' ':
                                    count = -1
                                    break
                                # if there is one opponent character in 4 space set, no score
                                if gridcopy[5 - start - x][col - start - x] == oppchar:
                                    count = count + 1
                                elif gridcopy[5 - start - x][col - start - x] == ' ':
                                    if 5 - start - x == 5:
                                        emptycount += 1
                                    elif gridcopy[5 - start - x + 1][col - start - x] == oppchar or \
                                                    gridcopy[5 - start - x + 1][
                                                                        col - start - x] == char:
                                        emptycount += 1
                                    else:
                                        emptycount += 0
                                        # count character number
                            if count < 0:
                                oppscore = 0
                            elif count == 3 and emptycount == 1:
                                oppscore = 64
                            elif count == 2 and emptycount == 2:
                                oppscore = 64
                            else:
                                oppscore = 0
                            # give score to 4 space set
                            ld_score = ld_score + oppscore
                    opp_diagonal_Advantage = rd_score + ld_score
                    gridcopy[5 - gridCount[k]][k] = ' '
                    advantage[k] -= opp_diagonal_Advantage
                return advantage.index(max(advantage))

    def put_by_rule(self):

        if self.grid[5][3] == ' ':
            position_x = 5
            position_y = 3
            print 6 - position_x, position_y + 1
            return 3
        else:
            return self.by_my_advantage()

    def check_input(self):
        count = [0, 0, 0, 0, 0, 0, 0]
        max = 1

        for x in range(len(self.gridInfo) - 1):
            count[self.gridInfo[x]] += 1

            if max(count) > 6:
                return False
        return True

if __name__ == "__main__":

    grid = Grid()

    player1_ch = 'O'
    player2_ch = 'X'

    grid.print_grid()
    AI_turn = raw_input("select AI turn, F : former, L : latter…")

    count = 0

    while True:
        if count % 2 == 0:
            ch = player1_ch
        else:
            ch = player2_ch

        print "1: print grid"
        print "2: make move by force"
        print "3: make move by algorithm"
        print "4: make move by rule"
        print "5: remove recent"
        print "6: clear grid"
        print "7: end game"

        choose = input("select ")
        if choose < 1 or choose > 7:
            while choose < 1 or 7 < choose:
                choose = input("choose again ")
        # make right selection
        if choose == 1:
            grid.print_grid()

        elif choose == 2:
            col_num = input("which column to put by force?(0-6) ")
            if col_num > 6 or col_num < 0:
                print "wrong input"
                continue

            if grid.put_by_force(col_num, ch):
                print "There's no place to put…"
                grid.print_grid()
                print "count : ", count
                continue
            else:
                grid.gridInfo = grid.gridInfo + str(col_num)
                grid.print_grid()
                count += 1

        elif choose == 3:
            root = GameNode(grid.gridInfo, 0, None)
            tree = GameTree()
            tree.build_tree(6, root)
            tree.print_tree()

            alphabeta = AlphaBeta(tree, AI_turn)
            best_state_name = alphabeta.alpha_beta_search(tree.root)
            print best_state_name

            grid.gridInfo = grid.gridInfo + best_state_name[len(best_state_name) - 1]
            grid.put_by_force(int(best_state_name[len(best_state_name) - 1]), ch)
            grid.print_grid()
            count += 1

        elif choose == 4:
            col_num = grid.put_by_rule()
            grid.put_by_force(col_num, ch)
            grid.gridInfo = grid.gridInfo + str(col_num)
            grid.print_grid()
            count += 1

        elif choose == 5:  # Do not use this option when nothing is on the board
            col_num = int(grid.gridInfo[len(grid.gridInfo) - 1])

            if grid.remove_recent(col_num):
                print("There's nothing to remove")
                grid.print_grid()
                print "count : ", count
                continue
            else:
                grid.gridInfo = grid.gridInfo[0:len(grid.gridInfo) - 1]
                grid.print_grid()
                count -= 1

        elif choose == 6:
            grid.clear_grid()
            grid.gridInfo = ''
            grid.print_grid()
            count = 0

        elif choose == 7:
            print("Bye :)")
            break

        if len(grid.gridInfo) > 41:
            print("Game is Over :)")
            break

        print "count : ", count
        # above if statements print position