import numpy as np


def divide_lot(num_job, num_stage, PT, QL):
    lotTime = []
    for i in range(num_job):
        sl = []
        for j in range(num_stage):
            l = np.ceil(PT[i][j] / QL[i])
            sl.append(int(l))
        lotTime.append(sl)

    # print("每个作业每一批的处理时间:", lotTime)
    return lotTime