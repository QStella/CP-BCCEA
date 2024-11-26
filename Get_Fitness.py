# 计算种群的适应度值
import numpy as np
from Schedule import CoDecode


def Fitness(Chromo, N, S, STMach, LotQ, ProcessTime):
    Fit = []
    # print("=======================================")
    # print(Chromo)
    for i in range(Chromo.shape[0]):
        Fe_Solution = Chromo[i].tolist()
        # print("!!!!", Fe_Solution)
        De_Solution = CoDecode(N, S, Fe_Solution, STMach, LotQ, ProcessTime)
        Machine_Time, Batch_Processing_Time, Process_Selection_Machine, Job_Start_Time, Job_End_Time = De_Solution.stage_decode()
        max_val = 0
        for sublist in Job_End_Time:
            sublist_max = max(sublist)
            if max_val is None or sublist_max > max_val:
                max_val = sublist_max
        fit = max_val
        Fit.append(fit)
    return np.array(Fit)




