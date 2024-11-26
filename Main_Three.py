# BCCEAP 算法主函数
import numpy as np
import pandas as pd
import math
import time
import os

from InitPop import init
from DE import mutate, crossover, selection
from EDA import EDA
from Get_Fitness import Fitness
from Crucial import get_crucial
from Schedule import CoDecode
from DrawGant import Gant

np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # 数组打印整行


if __name__ == "__main__":

    # Job_Data = [20, 40, 60, 80, 100, 150, 200]
    Job_Data = [80]
    # Job_Data = [10]
    ProcData = [4, 6, 8, 10]

    Algorithm_Number = 5               # 算法运行次数

    OS_Path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 根目录

    for Job in Job_Data:
        for Proc in ProcData:
            print()
            print()
            print("=================================================")
            print("运行数据集: " + str(Job) + "_" + str(Proc))

            # 读取数据
            Path = "../Data/" + str(Job) + "_" + str(Proc)               # 数据存放路径
            LotQ = np.loadtxt(Path + "/Batch.csv", delimiter=',', dtype=np.int32)                 # 读取每个工件可以分成多少批次数量
            STMach = np.loadtxt(Path + "/Machine.csv", delimiter=',', dtype=np.int32)             # 读取每道工序的可选机器
            ProcessTime = np.loadtxt(Path + "/Process_Time.csv", delimiter=',', dtype=np.int32)   # 每个作业的每道工序加工时间

            # 参数定义
            N = Job                      # 作业数量
            S = Proc                      # 工序数量
            M = sum(STMach)            # 机器总数

            Pop_Size = 50
            Pm = 0.2                   # 变异率
            Gen = 20                  # 迭代次数

            # EDA 参数
            Min_range = 0                # 下届
            Max_range = 5                # 上界
            Rounds = 10                  # 迭代次数
            a = 0.3

            # Time = 5 * N * S                    # 停止时间
            Time = N * S                    # 停止时间

            for algorithm_num in range(Algorithm_Number):
                print("--------------------------------------------------")
                print("第" + str(algorithm_num + 1) + "次....")

                StartTime = time.time()

                Chromo = init(Pop_Size, N)           # 初始化种群
                Bet_Seq = []
                Bet_Fit = math.inf
                EDA_Learning_Chromo = []

                for gen in range(Gen):
                    # print(gen)

                    EndTime = time.time()

                    if EndTime - StartTime > Time:
                        break
                    Mu_Chromo = mutate(Chromo, Pm)                  # 变异
                    CR_Chromo = crossover(Mu_Chromo)                # 交叉

                    # 如果是第一次，就拿初始种群学习
                    if len(EDA_Learning_Chromo) == 0:
                        EDA_Learning_Chromo = Chromo.copy()

                    # EDA 学习并生成解
                    p = EDA(Min_range, Max_range, N, S, Rounds, Pop_Size, a, EDA_Learning_Chromo.tolist())
                    p.get_location()
                    p.get_structure()
                    p.get_contemporary()
                    ProbabilityM = p.update_pmatrix()
                    EDA_Population = []
                    for i in range(Pop_Size):
                        Q = p.get_new()
                        EDA_Population.append(Q)

                    # 将学习到的EDA矩阵、父代矩阵、子代矩阵合并，并求 Fit
                    New_Chromo = np.vstack((Chromo, CR_Chromo))  # 经过DE之后的种群
                    New_Chromo_EDA = np.vstack((New_Chromo, np.array(EDA_Population)))   # DE和EDA种群混合

                    New_Chromo_DE_EDA = np.vstack((CR_Chromo, np.array(EDA_Population)))  # 第三个种群，将DE和EDA的种群放在一起
                    Th_Chromo = np.vstack((New_Chromo_EDA, New_Chromo_DE_EDA))

                    Fit = Fitness(Th_Chromo, N, S, STMach, LotQ, ProcessTime)
                    Se_Chromo = selection(Th_Chromo, Pop_Size, Fit)  # 选择 (最终选取 Pop_Size 个)

                    # 划分矩阵 (正常矩阵、关键矩阵)
                    Common_Chromo = Se_Chromo[0: int(Pop_Size * 0.5), 0: N].copy()
                    Crucial_Chromo = Se_Chromo[int(Pop_Size * 0.5):, 0: N].copy()

                    # 求解关键路径矩阵
                    Crucial_Path_Chromo = get_crucial(Crucial_Chromo, N, S, M, STMach, LotQ, ProcessTime)

                    # 将关键路径矩阵与正常矩阵拼接，形成下一代种群
                    Stack_Chromo = np.vstack((Common_Chromo, Crucial_Path_Chromo))

                    Chromo = Stack_Chromo.copy()

                    EDA_Learning_Chromo = Crucial_Path_Chromo.copy()

                    # 更新最优解
                    Fit_Stack = Fitness(Stack_Chromo, N, S, STMach, LotQ, ProcessTime)
                    Se_Stack = selection(Stack_Chromo, Pop_Size, Fit_Stack)  # 选择 (最终选取 Pop_Size 个)

                    if Se_Stack[0, -1] < Bet_Fit:
                        Bet_Seq = Se_Stack[0, 0: N].copy()
                        Bet_Fit = Se_Stack[0, -1]

                    End = time.time()

                print("最优解：" + str(Bet_Fit))

                # 保存结果
                Str_Name = str(Job) + "_" + str(Proc)
                Path_Result_BCCEAP = OS_Path + "/Result_Three/" + Str_Name + "/BCCEAP"
                Folder_BCCEAP = os.path.exists(Path_Result_BCCEAP)
                if not Folder_BCCEAP:                    # 判断是否存在文件夹，如果不在则创建文件夹
                    os.makedirs(Path_Result_BCCEAP)
                Path_Result_BCCEAP_Num = Path_Result_BCCEAP + "/" + str(algorithm_num + 1) + ".csv"
                Fit_Matrix = np.zeros((1, 1))
                Fit_Matrix[0, 0] = Bet_Fit
                df = pd.DataFrame(Fit_Matrix)
                df.to_csv(Path_Result_BCCEAP_Num, index=False, header=False)


    # De_Solution = CoDecode(N, S, Bet_Seq.tolist(), STMach, LotQ, ProcessTime)
    # Machine_Time, Batch_Processing_Time, Process_Selection_Machine, Job_Start_Time, Job_End_Time = De_Solution.stage_decode()
    # Gant(Bet_Seq.tolist(), S, np.sum(STMach), Batch_Processing_Time, Process_Selection_Machine, Job_End_Time, LotQ, STMach)








