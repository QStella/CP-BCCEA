# 初始化种群
import numpy as np
import random


def init(PopSize, Dimension):
    Chromo = np.array([random.sample(range(Dimension), Dimension) for tmp in range(PopSize)])+1
    return Chromo
