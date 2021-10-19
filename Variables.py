
#---------------------
# HIBAR VARIABLES FILE
#---------------------
import cdflib
from cdflib import cdfread
import numpy as np
from Files import ESA_file_1,ESA_file_2,user_path
from Files import mag36200_file,magX_file,magY_file,magZ_file
from Files import hibar_pitch_file,hibar_yaw_file
from Files import counts_file_low

from Files import ESA1_sensor1_L0_file,ESA1_sensor2_L0_file,ESA2_sensor1_L0_file,ESA2_sensor2_L0_file


# --- GENERAL VARIABLES ---
sensor_names = ['ESA1_sensor1','ESA1_sensor2','ESA2_sensor1','ESA2_sensor2']

# --- MAGNETOMETER INFORMATION ---
mag36200_time = mag36200_file.varget('time')
mag36200_x = mag36200_file.varget('x')
mag36200_y = mag36200_file.varget('y')
mag36200_z = mag36200_file.varget('z')
mag36200_t0 = mag36200_file.varget('t0')

magX_data = magX_file.varget('data')
magX_time = magX_file.varget('time')
magX_T0 = magX_file.varget('T-0')

magY_data = magY_file.varget('data')
magY_time = magY_file.varget('time')
magY_T0 = magY_file.varget('T-0')

magZ_data = magZ_file.varget('data')
magZ_time = magZ_file.varget('time')
magZ_T0 = magZ_file.varget('T-0')

# --- ESA INFORMATION ---

# SCOTT GAVE THESE VALUES IN EMAIL
engy_per_volt = 7.9  # In eV?
geometric_factor = 1.66e-4 # in seconds
Deadtime = 1.6e-6 # in seconds
acquisition_interval = 850e-6 # in seconds



#ESA1
ESA1_data = np.transpose(ESA_file_1.varget('data1'))
ESA1_discrete_status = ESA1_data[0]
ESA1_sweepDAC1 = ESA1_data[2]
ESA1_sweepDAC2 = ESA1_data[3]
ESA1_sensor1_data = [ESA1_data[i] for i in range(4,21)]
ESA1_sensor2_data = [ESA1_data[i] for i in range(21,36)]
ESA1_time = ESA_file_1.varget('time')
ESA1_info = ESA_file_1.cdf_info()
ESA1_zvars = ESA1_info['zVariables']
ESA1_rvars = ESA1_info['rVariables']

#ESA2
ESA2_data = np.transpose(ESA_file_2.varget('data1'))
ESA2_discrete_status = ESA2_data[0]
ESA2_sweepDAC1 = ESA2_data[2]
ESA2_sweepDAC2 = ESA2_data[3]
ESA2_sensor1_data = [ESA2_data[i] for i in range(4,21)]
ESA2_sensor2_data = [ESA2_data[i] for i in range(21,36)]
ESA2_time = ESA_file_2.varget('time')
ESA2_info = ESA_file_2.cdf_info()
ESA2_zvars = ESA2_info['zVariables']
ESA2_rvars = ESA2_info['rVariables']

# --- GYRO-PITCH INFORMATION ---
hibar_pitch_data = hibar_pitch_file.varget('data')
hibar_pitch_time = hibar_pitch_file.varget('time')
hibar_pitch_T0 = hibar_pitch_file.varget('T-0')

# --- GYRO-YAW INFORMATION ---
hibar_yaw_data = hibar_yaw_file.varget('data')
hibar_yaw_time = hibar_yaw_file.varget('time')
hibar_yaw_T0 = hibar_yaw_file.varget('T-0')


# --- EPOCH INFORMATION ---
ESA1_T0 = ESA_file_1.varget('T-0')
ESA2_T0 = ESA_file_2.varget('T-0')
Epochs_start = [2003,1,27,7,50,2,000,000,000,000]
Epochs_start_tt2000 = np.array(cdflib.epochs.CDFepoch.compute_tt2000(Epochs_start))
counts_low_info = counts_file_low.cdf_info()
zvars_counts_low = counts_low_info['zVariables']









