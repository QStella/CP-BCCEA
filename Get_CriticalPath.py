import copy

import numpy as np
from Lot import divide_lot
from Schedule import CoDecode
from Machine import Mach


def machine_job(num_job, num_stage, num_mach, sequence, job_machs):
    MJ = np.zeros((num_mach, num_job,), dtype=int)  # 每台机器上运行的作业
    # print(MJ.shape)
    for i in range(len(sequence)):
        # print(SL[sequence[i]])
        for j in range(num_stage):
            # print(SL[sequence[i]][j])
            MJ[job_machs[sequence[i]][j] - 1][i] = sequence[i]
    # print(MJ)
    return MJ


def calculate_forward(num_job, fc, num_lots, lots_time):
    forward_C = []
    count_job = np.zeros(num_job, dtype=int)
    for i in range(fc.shape[0]):  # 当前机器编号
        forward_CS = []
        # print("%s机器------" % i, fc[i])
        pro_id_index = np.nonzero(fc[i])  # 提取非0元素
        # print(pro_id_index)
        pro_id = fc[i][pro_id_index]  # 当前机器上的作业
        # print(pro_id)
        for j in range(len(pro_id)):  # 当前机器所在作业的编号
            # print("第%s个:" % j)
            jc = []
            now_id = pro_id[j]
            # print("@@", now_id)
            now_stage_id = count_job[now_id - 1]
            # print("当前阶段：", now_stage_id)
            # print(QL[now_id - 1])
            for k in range(num_lots[now_id - 1]):
                f = lots_time[now_id][now_stage_id][k * 2 + 1]
                jc.append(f)
            count_job[now_id - 1] += 1  # 放在处理完一个作业循环之后
            forward_CS.append(jc)
        forward_C.append(forward_CS)
    # print("前向完成时间：", forward_C)
    # print(count_job)
    # print(len(forward_C))
    return forward_C


def calculate_backward(fct, mj, mach_id, num_lots, lots_time, job_machs):
    backward_C = []
    j_machine = []

    num_stage_jobid = mach_id.getMachProcId()
    # print("----", num_stage_jobid)
    backward_C = copy.deepcopy(fct)
    # print(backward_C)

    for i in range(mj.shape[0]):
        pro_id_index = np.nonzero(mj[i])        # 提取非0元素索引
        pro_id = list(mj[i][pro_id_index])           # 当前机器上的作业
        j_machine.append(pro_id)
    # print("每个机器上的作业：", j_machine)

    for k in range(len(num_stage_jobid) - 1, -1, -1):  # 找出此阶段包含的机器
        # print("阶段k---------------------------------", k)
        # print(num_stage_jobid[k])
        if k == len(num_stage_jobid) - 1:       # 最后一个阶段机器
            last = []  # 存储最后一个阶段所有机器上最后加工工件的完工时间
            for k1 in range(len(num_stage_jobid[k]) - 1, -1, -1):
                last.append(fct[num_stage_jobid[k][k1] - 1][-1][-1])
            smax_num = max(last)
            for k2 in range(len(num_stage_jobid[k]) - 1, -1, -1):
                now_machine = num_stage_jobid[k][k2]
                now_machine_job = j_machine[now_machine-1]
                for t in range(len(now_machine_job) - 1, -1, -1):
                    for j in range(num_lots[now_machine_job[t] - 1] - 1, -1, -1):
                        now_job_pt = backward_C[num_stage_jobid[k][k2] - 1][t]
                        if t == len(now_machine_job) - 1:
                            if j == num_lots[now_machine_job[t] - 1] - 1:
                                now_job_pt[j] = smax_num
                            else:
                                now_job_pt[j] = now_job_pt[j + 1] - lots_time[now_machine_job[t] - 1][k]
                        else:
                            if j == num_lots[now_machine_job[t] - 1] - 1:

                                now_job_pt[j] = backward_C[num_stage_jobid[k][k2] - 1][t + 1][0] - lots_time[now_machine_job[t+1]-1][k]
                            else:
                                now_job_pt[j] = now_job_pt[j + 1] - lots_time[now_machine_job[t] - 1][k]

                # print("$$$$$$$", backward_C[num_stage_jobid[k][k2] - 1])
            # print(backward_C)

        else:        # 非最后阶段
            for k1 in range(len(num_stage_jobid[k]) - 1, -1, -1):
                now_machine = num_stage_jobid[k][k1]
                now_machine_job = j_machine[now_machine - 1]
                for t in range(len(now_machine_job) - 1, -1, -1):
                    last_stage_id = job_machs[now_machine_job[t]][k + 1]
                    last_stage_id_index = j_machine[last_stage_id - 1].index(now_machine_job[t])
                    for j in range(num_lots[now_machine_job[t] - 1] - 1, -1, -1):
                        now_job_pt = backward_C[num_stage_jobid[k][k1] - 1][t]
                        if t == len(now_machine_job) - 1:
                            if j == num_lots[now_machine_job[t] - 1] - 1:
                                last_stage_job_pt = backward_C[last_stage_id - 1][last_stage_id_index][j]
                                now_job_pt[j] = last_stage_job_pt - lots_time[now_machine_job[t] - 1][k + 1]
                            else:
                                last_stage_job_pt = backward_C[last_stage_id - 1][last_stage_id_index][j]
                                last_stage_job_pts = last_stage_job_pt - lots_time[now_machine_job[t]-1][k+1]
                                now_job_pts = now_job_pt[j+1] - lots_time[now_machine_job[t]-1][k]
                                now_job_pt[j] = min(last_stage_job_pts, now_job_pts)

                        else:
                            if j == num_lots[now_machine_job[t] - 1] - 1:
                                last_stage_job_pt = backward_C[last_stage_id - 1][last_stage_id_index][j]
                                last_stage_job_pts = last_stage_job_pt - lots_time[now_machine_job[t] - 1][k + 1]
                                now_job_pts = backward_C[now_machine - 1][t+1][0]-lots_time[now_machine_job[t+1]-1][k]
                                now_job_pt[j] = min(last_stage_job_pts, now_job_pts)

                            else:

                                last_stage_job_pt = backward_C[last_stage_id - 1][last_stage_id_index][j]

                                last_stage_job_pts = last_stage_job_pt - lots_time[now_machine_job[t] - 1][k + 1]

                                now_job_pts = now_job_pt[j + 1] - lots_time[now_machine_job[t] - 1][k]

                                now_job_pt[j] = min(last_stage_job_pts, now_job_pts)

    # print("后向完成时间：", backward_C)
    return backward_C


def calculate_path(f, b, mj):
    path = []
    for i in range(len(f)):
        path1 = []
        for j in range(len(f[i])):
            path12 = []
            for s in range(len(f[i][j])):
                if f[i][j][s] == b[i][j][s]:
                    h = 1
                else:
                    h = 0
                    # print("0")
                path12.append(h)
            path1.append(path12)
        path.append(path1)
    # print("关键路径：", path)
    return path


if __name__ == '__main__':
    Jobs = 6  # 作业数量
    Stages = 4  # 工序数量
    QL = [2, 2, 5, 3, 2, 4]  # 每个作业可分为几批
    QJ = [10, 43, 60, 27, 45, 60]  # 作业总量
    stageMach = [2, 2, 3, 2]  # 每个阶段的机器数量
    Num_M = np.sum(stageMach)
    PT = [[73, 57, 81, 65],  # 每个作业在每个阶段的处理时间
          [60, 84, 93, 91],
          [83, 69, 82, 54],
          [99, 57, 80, 61],
          [61, 56, 53, 82],
          [76, 82, 92, 96]]
    a_Solution = [3, 6, 2, 1, 4, 5]
    p = divide_lot(Jobs, Stages, PT, QL)
    print("批次加工时间：", p)

    c = CoDecode(Jobs, Stages, a_Solution, stageMach, QL, PT)
    JLT, SL = c.stage_decode()[1:3]
    m = Mach(stageMach, Jobs, a_Solution)

    g = machine_job(Jobs, Stages, Num_M, a_Solution, SL)
    FC = calculate_forward(Jobs, g, QL, JLT)
    BC = calculate_backward(FC, g, m, QL, p, SL)
    print()
    calculate_path(FC, BC, g)
