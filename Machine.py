# 机器类
class Mach:
    def __init__(self, stageMach, num_job, solution):
        self.stageMachQty = stageMach
        self.job = num_job
        self.sequence = solution
        self.mach_pro_id = None
        self.Stage_nowMachTime = None
        self.alMTime = None

    def getMachProcId(self):
        procQty = len(self.stageMachQty)  # 工序数量
        self.mach_pro_id = []
        midIdx = 1
        for i in range(procQty):
            self.mach_pro_id.append([])
            for j in range(self.stageMachQty[i]):
                self.mach_pro_id[i].append(midIdx)
                midIdx += 1
        # print("每个阶段的可用机器id:", self.mach_pro_id)
        return self.mach_pro_id

    def getSingleMT(self):
        self.Stage_nowMachTime = []
        for j in range(len(self.stageMachQty)):
            self.Stage_nowMachTime.append([0] * self.stageMachQty[j])
        # print("每个阶段的机器时间：", self.Stage_nowMachTime)
        return self.Stage_nowMachTime

    def getMachProcTime(self):
        self.alMTime = dict()
        for j in range(self.job):
            t = {self.sequence[j]: self.Stage_nowMachTime}
            self.alMTime.update(t)
        return self.alMTime
