import numpy as np
from Lot import divide_lot
from Schedule import CoDecode
from Get_CriticalPath import machine_job, calculate_path, calculate_forward, calculate_backward
from Machine import Mach


def calculate_critical_job(mj, job_machs, sequence, num_job, num_stage, num_lots, path):
    j_machine = []
    critical_job = []
    label = np.zeros((num_stage, num_job))
    for i in range(mj.shape[0]):
        pro_id_index = np.nonzero(mj[i])        # 提取非0元素索引
        pro_id = list(mj[i][pro_id_index])           # 当前机器上的作业
        j_machine.append(pro_id)
    # print("每个机器上的作业：", j_machine)
    # print(job_machs)
    for i in range(len(sequence)):
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        now_j = sequence[i]
        # print("当前工件：", now_j)
        now_jm = job_machs[sequence[i]]
        # print("所分配的所有机器：", now_jm)
        for j in range(num_stage):
            # print("--", now_jm[j])
            # print(j_machine[now_jm[j]-1])
            now_jm_index = j_machine[now_jm[j]-1].index(now_j)
            # print(now_jm_index)
            for k in range(num_lots[now_j-1]):
                # print("++", path[now_jm[j] - 1][now_jm_index][k])
                # print("11")
                if path[now_jm[j]-1][now_jm_index][k] == 1:

                    label[j][now_j-1] += 1
    # print(label)
    # print(type(label))
    for i in range(label.shape[1]):
        result = all(label[:, i] >= 1)
        # print("!!", result)
        if result == 1:
            critical_job.append(i+1)
    # print("关键工件：", critical_job)
    return critical_job





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
    a_Solution = [3, 6, 2, 1, 4, 5]
    # a = CriticalPath(Jobs, Stages, QL, a_Solution, PT)
    c = CoDecode(Jobs, Stages, a_Solution, stageMach, QL, PT)
    m = Mach(stageMach, Jobs, a_Solution)
    p = divide_lot(Jobs, Stages, PT, QL)
    JLT, SL = c.stage_decode()[1:3]
    print(SL)
    g = machine_job(Jobs, Stages, Num_M, a_Solution, SL)
    FC = calculate_forward(Jobs, g, QL, JLT)
    BC = calculate_backward(FC, g, m, QL, p, SL)
    PA = calculate_path(FC, BC, g)
    calculate_critical_job(g, SL, a_Solution, Jobs, Stages, QL, PA)


