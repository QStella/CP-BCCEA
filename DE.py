# DE 中的操作
import copy
import random
import numpy as np


# 变异
def mutate(Chromo, pm):

    PopSize = Chromo.shape[0]
    Dimension = Chromo.shape[1]
    Mutant = []
    Chromo_List = Chromo.tolist().copy()
    for i in range(PopSize):
        r0, r1, r2 = 0, 0, 0
        while r0 == r1 or r1 == r2 or r0 == r2 or r0 == i:
            r0 = random.randint(0, PopSize - 1)
            r1 = random.randint(0, PopSize - 1)
            r2 = random.randint(0, PopSize - 1)
        dif = Chromo[r1, :] - Chromo[r2, :]
        rand = [random.random() for i in range(Dimension)]

        for d in range(Dimension):
            if dif[d] != 0:
                dif[d] = Chromo[r2][d]
            if rand[d] <= pm:
                dif[d] = 0

        add = list(copy.deepcopy(dif))
        for k in range(Dimension):
            if add[k] == 0 or (add[k] != 0 and add[k] == Chromo_List[r0][k]):
                pass
            else:
                if add[k] != Chromo[r0][k] != 0:
                    a1 = add[k]
                    p1 = Chromo_List[r0].index(a1)
                    num = Chromo_List[r0][k]
                    Chromo_List[r0][k] = Chromo_List[r0][p1]
                    Chromo_List[r0][p1] = num
        v = Chromo_List[r0]
        Mutant.append(v)
    return np.array(Mutant)


# 交叉操作
def crossover(Chromo):
    PopSize = Chromo.shape[0]
    Dimension = Chromo.shape[1]
    Chromo_List = Chromo.tolist()
    for i in range(PopSize):
        g1 = random.randrange(Dimension)

        r0, r1 = 0, 0
        while r0 == r1:
            r0 = random.randint(0, PopSize - 1)
            r1 = random.randint(0, PopSize - 1)

        p11 = Chromo_List[r0][:g1 + 1].copy()
        p12 = Chromo_List[r0][g1 + 1:].copy()

        p21 = Chromo_List[r1][:g1 + 1].copy()
        p22 = Chromo_List[r1][g1 + 1:].copy()

        # 冲突检测判断(因为都是末尾交叉，所以只判断从开头到交叉点)
        for j in range(len(p11)):
            for k in range(len(p22)):
                if p11[j] == p22[k]:
                    number = p12[k]
                    Flag = 1
                    while Flag != 0:
                        for z in range(len(p22)):
                            if number == p22[z]:
                                number = p12[z]
                                break
                            if z == len(p22) - 1:
                                Flag = 0
                    p11[j] = number

        for j in range(len(p21)):
            for k in range(len(p12)):
                if p21[j] == p12[k]:
                    number = p22[k]
                    Flag = 1
                    while Flag != 0:
                        for z in range(len(p12)):
                            if number == p12[z]:
                                number = p22[z]
                                break
                            if z == len(p12) - 1:
                                Flag = 0
                    p21[j] = number

        p1 = p11 + p22
        p2 = p21 + p12

        Chromo_List[r0] = p1.copy()
        Chromo_List[r1] = p2.copy()

        i += 1

    return np.array(Chromo_List)


def selection(Chromo, PopSize, Fit):
    Fit = Fit[:, np.newaxis]
    New_Chromo = np.hstack((Chromo, Fit))                              # 拼接数组和 Fit
    Selection_Chromo = New_Chromo[np.lexsort(New_Chromo.T)][0:PopSize, :].copy()  # 最后一列排序，并选择前POP个
    return Selection_Chromo
