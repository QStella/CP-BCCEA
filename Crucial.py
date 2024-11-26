# 求解关键路径函数
import copy
import math
import numpy as np
from Get_CriticalPath import machine_job, calculate_path, calculate_forward, calculate_backward
from Get_CriticalBlock import calculate_critical_job
from Schedule import CoDecode
from Lot import divide_lot
from Machine import Mach
from Get_Fitness import Fitness


def get_crucial(Chromo, N, S, M, STMach, LotQ, ProcessTime):
    Return_Chromo = []
    for i in range(Chromo.shape[0]):
        Fe_Solution = Chromo[i].tolist()

        De_Solution = CoDecode(N, S, Fe_Solution, STMach, LotQ, ProcessTime)
        Machine_Time, Batch_Processing_Time, Process_Selection_Machine, Job_Start_Time, Job_End_Time = De_Solution.stage_decode()
        Lot_ProcessTime = divide_lot(N, S, ProcessTime, LotQ)
        MA = Mach(STMach, N, Fe_Solution)
        Job_on_Machine = machine_job(N, S, M, Fe_Solution, Process_Selection_Machine)
        FC = calculate_forward(N, Job_on_Machine, LotQ, Batch_Processing_Time)
        BC = calculate_backward(FC, Job_on_Machine, MA, LotQ, Lot_ProcessTime, Process_Selection_Machine)
        PA = calculate_path(FC, BC, Job_on_Machine)
        crucial_job = calculate_critical_job(Job_on_Machine, Process_Selection_Machine, Fe_Solution, N, S, LotQ, PA)
        temp = []
        # print(crucial_job)

        for j in range(len(crucial_job)):
            tp = copy.deepcopy(Fe_Solution)
            crucial_job_index = tp.index(crucial_job[j])
            del tp[crucial_job_index]
            # print(tp)

            seq = []
            for t in range(len(tp)+1):
                tp.insert(t, crucial_job[j])
                seq = tp.copy()
                # print(seq)
                temp.append(seq)
                tp.remove(crucial_job[j])

        Temp_Fit = Fitness(np.array(temp), N, S, STMach, LotQ, ProcessTime)
        Fe_Solution_Fit = Fitness(np.array(Fe_Solution)[np.newaxis, :], N, S, STMach, LotQ, ProcessTime)

        Number = Fe_Solution_Fit
        Good = Fe_Solution.copy()
        for num in range(len(Temp_Fit)):
            if Temp_Fit[num] < Number:
                Good = temp[num]
                Number = Temp_Fit[num]
        Return_Chromo.append(Good)
    return np.array(Return_Chromo)



if __name__ == '__main__':
    Jobs = 6  # 作业数量
    Stages = 4  # 工序数量
    QL = [2, 2, 5, 3, 2, 4]  # 每个作业可分为几批
    QJ = [10, 43, 60, 27, 45, 60]  # 作业总量
    stageMach = [2, 2, 3, 2]  # 每个阶段的机器数量
    Num_QL = np.sum(QL)
    Num_M = np.sum(stageMach)
    PT = [[73, 57, 81, 65],  # 每个作业在每个阶段的处理时间
          [60, 84, 93, 91],
          [83, 69, 82, 54],
          [99, 57, 80, 61],
          [61, 56, 53, 82],
          [76, 82, 92, 96]]
    a_Solution = [[3, 6, 2, 1, 4, 5],
                  [3, 5, 1, 2, 4, 6]]
    a_Solution1 = np.array(a_Solution)
    # print(type(a_Solution1))
    get_crucial(a_Solution1, Jobs, Stages, Num_M, stageMach, QL, PT)
