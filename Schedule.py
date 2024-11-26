 # 调度类
import numpy as np
import copy

from Machine import Mach
from JOB import Job
from Lot import divide_lot


class CoDecode:
    def __init__(self, num_job, num_stage, solution, stageMach, num_lot, ptime):
        self.job = num_job
        self.stage = num_stage
        self.stMach = stageMach
        self.sequence = solution
        self.lott = num_lot
        self.pt = ptime
        self.machineNum = np.sum(stageMach)
        self.nowJob = None
        machArray = Mach(self.stMach, self.job, self.sequence)
        self.Machines = machArray.getMachProcId()                    # 每个阶段可用的机器[[1, 2], [3, 4], [5, 6, 7], [8, 9]]
        self.SingleMTime = machArray.getSingleMT()
        self.AllMTime = machArray.getMachProcTime()                  # 每个作业在每个阶段所用的机器时间
        jobArray = Job(self.job, self.sequence, self.stage, self.lott)
        self.Selected_mach = jobArray.getJob_machTable()             # 在每个阶段选择的机器
        self.JobLotTime = jobArray.getLTime()
        self.ST = jobArray.getSTime()
        self.ET = jobArray.getETime()
        self.LotTime = divide_lot(self.job, self.stage, self.pt, self.lott)

    def decode(self):
        for k in range(self.stage):                                 # 按阶段排序
            nowMachIds = self.Machines[k]                           # 获取当前工序的可用机器编码
            # print("可用机器：", nowMachIds)
            self.SingleMTime = copy.deepcopy(self.AllMTime[self.nowJob])
            idm = np.argmin(self.SingleMTime[k])  # 在可选择的机器的列表中的索引
            nowMachId = nowMachIds[idm]
            # print("选择的机器编号：", nowMachId)
            self.Selected_mach[self.nowJob][k] = nowMachId

            if k == 0:
                for sl in range(self.lott[self.nowJob - 1]):               # 按批次循环
                    if sl == 0:
                        self.JobLotTime[self.nowJob][k][sl] = self.SingleMTime[k][idm]
                        self.JobLotTime[self.nowJob][k][sl + 1] = self.JobLotTime[self.nowJob][k][sl] + \
                                                                  self.LotTime[self.nowJob - 1][k]
                    else:
                        self.JobLotTime[self.nowJob][k][sl * 2] = self.JobLotTime[self.nowJob][k][sl * 2 - 1]
                        self.JobLotTime[self.nowJob][k][sl * 2 + 1] = self.JobLotTime[self.nowJob][k][sl * 2] + \
                                                                      self.LotTime[self.nowJob - 1][k]
            else:
                for sl in range(self.lott[self.nowJob - 1]):

                    if sl == 0:
                        self.JobLotTime[self.nowJob][k][sl] = max(self.SingleMTime[k][idm],
                                                                  self.JobLotTime[self.nowJob][k - 1][sl + 1])
                        self.JobLotTime[self.nowJob][k][sl + 1] = self.JobLotTime[self.nowJob][k][sl] + \
                                                                  self.LotTime[self.nowJob - 1][k]
                    else:
                        self.JobLotTime[self.nowJob][k][sl * 2] = max(self.JobLotTime[self.nowJob][k][sl * 2 - 1],
                                                                      self.JobLotTime[self.nowJob][k - 1][sl * 2 + 1])
                        self.JobLotTime[self.nowJob][k][sl * 2 + 1] = self.JobLotTime[self.nowJob][k][sl * 2] + \
                                                                      self.LotTime[self.nowJob - 1][k]

            self.ST[self.sequence.index(self.nowJob)][k] = self.JobLotTime[self.nowJob][k][0]
            self.ET[self.sequence.index(self.nowJob)][k] = self.JobLotTime[self.nowJob][k][-1]
            # self.SingleMTime[k][idm] = self.SingleMTime[k][idm] + self.ET[self.sequence.index(self.nowJob)][k]  # 作业排序完成之后更新机器表9
            self.SingleMTime[k][idm] = self.ET[self.sequence.index(self.nowJob)][k]  # 作业排序完成之后更新机器表9

            # print("更新单个作业的机器时间：", self.SingleMTime)
            self.AllMTime.update({self.nowJob: self.SingleMTime})

        # print("***********************************")
        # print(self.AllMTime)
        # print(self.JobLotTime)
        # print(self.Selected_mach)
        # print(self.ST)
        # print(self.ET)

    def stage_decode(self):
        for x in range(len(self.sequence)):
            self.nowJob = self.sequence[x]
            # print("作业编号：", self.nowJob)
            self.decode()

            if x < (len(self.sequence)-1):
                list1 = self.AllMTime[self.sequence[x]]
                list2 = self.AllMTime[self.sequence[x + 1]]
                listAdd = []
                for _ in range(len(list1)):
                    listAdd.append(list(np.array(list1[_]) + np.array(list2[_])))

                self.AllMTime.update({self.sequence[x + 1]: listAdd})
        return self.AllMTime, self.JobLotTime, self.Selected_mach, self.ST, self.ET

