import cdflib
import numpy as np
from Variables import ESA1_info, ESA2_info,ESA1_data,ESA2_data
from Variables import ESA1_T0,ESA2_T0,ESA1_time,ESA2_time
from Variables import ESA1_sweepDAC1,ESA1_sweepDAC2,ESA2_sweepDAC1,ESA2_sweepDAC2

# Eochs_startp = [2017,2,2 ,2,2 ,2,987,654,321,999]
Epochs_start = [2003,1,27,7,50,2,000,000,000,000]
Epochs_start_computed = np.array(cdflib.epochs.CDFepoch.compute_epoch(Epochs_start))
Epochs_start_computedtt = np.array(cdflib.epochs.CDFepoch.compute_tt2000(Epochs_start))
print(Epochs_start_computed,Epochs_start_computedtt)

Epoch1 = np.array((ESA1_time)*(10**(9)) + Epochs_start_computedtt,dtype='int64')

print(Epoch1[0:5])

for i in range(10):
    print(cdflib.cdfepoch.breakdown_tt2000(Epoch1[i]))
