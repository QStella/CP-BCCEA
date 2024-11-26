# 作业类

class Job:
    def __init__(self, num_job, solution, num_stage, num_lot):
        self.sequence = solution
        self.job = num_job
        self.stage = num_stage
        self.lott = num_lot
        self.jmTable = None
        self.StartTime = None
        self.EndTime = None
        self.LotSET = None

    def getJob_machTable(self):
        self.jmTable = dict()
        for i in range(len(self.sequence)):
            t = {self.sequence[i]: [0 for i in range(self.stage)]}
            # print(t)
            self.jmTable.update(t)
        # print("每个作业在每个阶段所选择的机器编号", self.jmTable)
        return self.jmTable

    def getSTime(self):
        self.StartTime = []
        for i in range(self.job):
            t = [0 for k in range(self.stage)]
            # print(t)
            self.StartTime.append(t)
        # print(self.StartTime)
        return self.StartTime

    def getETime(self):
        self.EndTime = []
        for i in range(self.job):
            t = [0 for k in range(self.stage)]
            # print(t)
            self.EndTime.append(t)
        # print(self.EndTime)
        return self.EndTime

    def getLTime(self):
        self.LotSET = dict()
        for i in range(len(self.sequence)):
            t = {self.sequence[i]: [[0 for j in range(self.lott[self.sequence[i]-1] * 2)] for k in range(self.stage)]}
            self.LotSET.update(t)
        # print("每个作业每一批的开始结束时间：", self.LotSET)
        return self.LotSET
