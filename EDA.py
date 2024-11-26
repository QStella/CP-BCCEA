# EDA 产生解
import copy

import numpy as np


class EDA:
    def __init__(self, Min_range, Max_range, Num_Job, Num_Stage, Rounds, Size, A, Chromo):
        self.Job = Num_Job
        self.Stage = Num_Stage
        self.Min_range = Min_range              # 下届
        self.Max_range = Max_range              # 上界
        # self.Dimension = Dim                    # 维度
        self.Rounds = Rounds                    # 迭代次数
        self.Pop_Size = Size                    # 种群数量
        self.Learning_rage = A                  # 矩阵的学习率
        self.Cur_Round = 1
        self.Chromo = Chromo           # 学习的种群

        self.Pro_matrix = np.full((self.Job, self.Job), 1 / self.Job)       # 概率矩阵
        self.JobLoc = None
        self.BlockStr = None
        self.GoodInformation = None

    def get_location(self):
        self.JobLoc = np.zeros((self.Job, self.Job))
        for s in range(len(self.Chromo)):
            Loc = np.zeros((self.Job, self.Job))
            for j in range(self.Job):
                p = self.Chromo[s].index(self.Chromo[s][j])
                for i in range(self.Stage):
                    if p <= i:
                        Loc[i][self.Chromo[s][j] - 1] = 1
                    else:
                        Loc[i][self.Chromo[s][j] - 1] = 0
            self.JobLoc = self.JobLoc + Loc

    def get_structure(self):
        self.BlockStr = np.zeros((self.Job, self.Job))
        for s in range(len(self.Chromo)):
            Block = np.zeros((self.Job, self.Job))
            for k in range(1, self.Job + 1):
                for j in range(1, self.Job + 1):
                    if k == j:
                        # Block[k][j] = -1
                        Block[k-1][j-1] = 0
                    else:
                        p1 = self.Chromo[s].index(k)
                        p2 = self.Chromo[s].index(j)
                        if p2 == p1 + 1:
                            Block[k-1][j-1] = 1
                        else:
                            Block[k-1][j-1] = 0
            self.BlockStr = self.BlockStr + Block

        # print(self.BlockStr)

    def get_contemporary(self):
        self.GoodInformation = np.zeros((self.Job, self.Job))
        for j in range(self.Job):
            self.GoodInformation[j] = 1 / 2 * ((1 / ((j + 1) * self.Job)) * self.JobLoc[j] + self.BlockStr[j])

        for i in range(self.Job):
            for j in range(self.Job):
                if self.GoodInformation[i][j] < 0:                # 保留两位小数，并且将之前的负数进行修正
                    self.GoodInformation[i][j] = 0
                    self.GoodInformation[i][j] = 1 / 2 * ((1 / ((j + 1) * self.Job)) * self.JobLoc[j] + self.GoodInformation[i][j])

    # 更新概率矩阵
    def update_pmatrix(self):
        # print(self.Pro_matrix)
        self.Pro_matrix = (1 - self.Learning_rage) * self.Pro_matrix + self.Learning_rage * self.GoodInformation
        return self.Pro_matrix

    def get_new(self):
        # 归一化概率矩阵
        New_Matrix = np.zeros((self.Pro_matrix.shape[0], self.Pro_matrix.shape[1]))
        for j in range(self.Pro_matrix.shape[0]):
            arr = np.array(self.Pro_matrix[j, :] / min(self.Pro_matrix[j, :]))
            New_Matrix[j, :] = (arr / sum(arr)).copy()
        self.Pro_matrix = copy.deepcopy(New_Matrix)

        # 形成新的个体
        New_Chromo = []
        for j in range(New_Matrix.shape[0]):
            # print(New_Matrix[j, :])
            # print(sum(New_Matrix[j, :]))

            x = np.random.choice(a=self.Job, size=1, replace=False, p=New_Matrix[j, :])
            x1 = int(x[0]+1)
            New_Chromo.append(x1)
            New_Matrix[:, New_Chromo[j]-1] = 0
            if j != (New_Matrix.shape[0] - 1):
                for i in range(New_Matrix.shape[0]):
                    sum_arr = np.sum(New_Matrix[i, :])
                    New_Matrix[i, :] = (np.divide(New_Matrix[i, :], sum_arr)).copy()
        return New_Chromo
