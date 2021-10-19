import cdflib
import numpy as np
from Variables import ESA1_info, ESA2_info,ESA1_data,ESA2_data
from Variables import ESA1_T0,ESA2_T0,ESA1_time,ESA2_time
from Variables import ESA1_sweepDAC1,ESA1_sweepDAC2,ESA2_sweepDAC1,ESA2_sweepDAC2
from Variables import ESA2_discrete_status,ESA1_discrete_status

#
# uniques,counts = np.unique(ESA1_discrete_status,return_counts=True)
# print(uniques)
# print(counts)
# uniques,counts = np.unique(ESA2_discrete_status,return_counts=True)
# print(uniques)
# print(counts)

engy_per_volt = 7.9

print(np.round(np.array([-10.3,-10.3,-11.6,-13,-15,-16.9,-18.9,-21.3,-24.5,-27.8,-31.7,-35.9,-40.9,-46.1,-52.5,-60,-67.7,-76.9,-87.3,-99.1,-113.5,-129,-145.7,-165.2,-188.9,-214.9,-246.2,-279.5,-318.5,-360,-413,-471,-532,-605,-692,-786,-900,-1022,-1156,-1322,-1509,-1714,-1963,-2231,-2540],dtype='float64') * engy_per_volt,0))