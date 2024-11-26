import numpy as np
import matplotlib.pyplot as plt


def Gant(seq, stages, num_M, JT, SM, CT, LQ, SGM):
    color_lib = ['#64B6EA', '#FB8857', '#A788EB', '#80D172', '#F48FB1', '#61D4D5',
                 '#C3BCE6', '#F8D889', '#69CDE0', '#5EB7F1', '#EDA462', '#F6C4E6',
                 '#55EFC4', '#1BB5E1', '#74B9FF', '#D3DE9E', '#7F8C8D', '#C9C9C9',
                 '#2ED573', '#C0E5BC', '#8C8FD5', '#BDF4FC', '#F1787D', '#FC7A77']

    for i in range(len(seq)):
        nj = seq[i]
        for k in range(stages):
            for q in range(LQ[nj - 1]):
                plt.barh(SM[nj][k], width=JT[nj][k][q * 2 + 1] - JT[nj][k][q * 2], height=0.5, left=JT[nj][k][q * 2],
                         edgecolor='black', color=color_lib[i])

    plt.yticks(np.arange(0, num_M+1, 1))
    # 划分每个阶段的机器
    a = SGM[0]
    for i in range(len(SGM) - 1):
        plt.axhline(a + 0.5, c='k', ls='--', lw=2)
        a += SGM[i + 1]

    # Cmax的位置
    max_val = 0
    for sublist in CT:
        sublist_max = max(sublist)
        if max_val is None or sublist_max > max_val:
            max_val = sublist_max
    print(max_val)
    plt.axvline(x=max_val, linestyle='--', color='#D2691E')
    plt.annotate("Cmax=%s" % max_val, xy=(max_val, 0), xytext=(max_val, -1), color='#D2691E')

    plt.show()