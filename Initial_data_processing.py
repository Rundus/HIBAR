
import time
print('importing variables: ', end='')
start_time = time.time()


import numpy as np
from cdflib import cdfwrite
from Files import ESA_file_1,ESA_file_2,root,counts_file_low
from Files import mag36200_file,magX_file,magY_file,magZ_file
from Files import hibar_pitch_file,hibar_yaw_file,user_path
from Variables import sensor_names,ESA1_info,ESA2_info,Epochs_start_tt2000
from Variables import zvars_counts_low
from functions import write_var_to_file


# ----------------------------------------
# GET THE INITIAL VARIABLES FOR PROCESSING
# ----------------------------------------

#select the sensor to operate on
selects = [0,1,2,3]

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
#ESA1
ESA1_data = np.transpose(ESA_file_1.varget('data1'))
ESA1_discrete_status = ESA1_data[0]
ESA1_sweepDAC1 = ESA1_data[2]
ESA1_sweepDAC2 = ESA1_data[3]
ESA1_sensor1_data = [ESA1_data[i] for i in range(4,20)]
ESA1_sensor2_data = [ESA1_data[i] for i in range(20,36)]
ESA1_time = ESA_file_1.varget('time')
ESA1_T0 = ESA_file_1.varget('T-0')
ESA1_info = ESA_file_1.cdf_info()
ESA1_zvars = ESA1_info['zVariables']
ESA1_rvars = ESA1_info['rVariables']

#ESA2
ESA2_data = np.transpose(ESA_file_2.varget('data1'))
ESA2_discrete_status = ESA2_data[0]
ESA2_sweepDAC1 = ESA2_data[2]
ESA2_sweepDAC2 = ESA2_data[3]
ESA2_sensor1_data = [ESA2_data[i] for i in range(4,20)]
ESA2_sensor2_data = [ESA2_data[i] for i in range(20,36)]
ESA2_time = ESA_file_2.varget('time')
ESA2_T0 = ESA_file_2.varget('T-0')
ESA2_info = ESA_file_2.cdf_info()
ESA2_zvars = ESA2_info['zVariables']
ESA2_rvars = ESA2_info['rVariables']

print('Done')


#---------------------
# --- OUTPUT FILES ---
#---------------------
ESA1_sensor1_counts_file = cdfwrite.CDF(user_path + root + 'ESA1_sensor1_counts_data',cdf_spec=ESA1_info,delete=True)
ESA1_sensor2_counts_file = cdfwrite.CDF(user_path + root + 'ESA1_sensor2_counts_data',cdf_spec=ESA1_info,delete=True)
ESA2_sensor1_counts_file = cdfwrite.CDF(user_path + root + 'ESA2_senor1_counts_data',cdf_spec=ESA2_info,delete=True)
ESA2_sensor2_counts_file = cdfwrite.CDF(user_path + root + 'ESA2_senor2_counts_data',cdf_spec=ESA2_info,delete=True)

output_files = [ESA1_sensor1_counts_file,ESA1_sensor2_counts_file,ESA2_sensor1_counts_file,ESA2_sensor2_counts_file]



#------------------------------------------------------
# ----------------- BEGIN PROCESSING  -----------------
#------------------------------------------------------

# --- TIME & CALCULATED VALUES FROM BELOW---
ESAtimes = [ESA1_time,ESA2_time]
first_sweep_starts = [7, 22, 31, 1]#index corresponding to the beginning of the first full sweeps for each DACSWEEP. CALCULATED from CDF_INFO
ignored_indicies = [41,26,31,16]#How many indicies at the end of the data should be ignore to clump the data perfectly by length of energies


# --- GET THE "ENERGIES" (SWEEP DACS) for each sensor ---
SWEEPdata = [ESA1_sweepDAC1[first_sweep_starts[0]:(len(ESA1_sweepDAC1) - ignored_indicies[0])],ESA1_sweepDAC2[first_sweep_starts[1]:(len(ESA1_sweepDAC2) - ignored_indicies[1])],ESA2_sweepDAC1[first_sweep_starts[2]:(len(ESA2_sweepDAC1) - ignored_indicies[2])],ESA2_sweepDAC2[first_sweep_starts[3]:(len(ESA2_sweepDAC2) - ignored_indicies[3])]]

Energies_DACs = [[] for i in range(len(selects))]

for select in selects:
    unique_DACenergies, unique_DACcounts = np.unique(SWEEPdata[select], return_counts=True)
    for i in range(len(unique_DACcounts)):
        if unique_DACcounts[i] >= 5000:
            Energies_DACs[select].append(unique_DACenergies[i])

#adjust the energies to include one more "129" for some reason?
for i in range(len(selects)):
    Energies_DACs[i].append(129)

Energies_DAC = Energies_DACs[0][::-1]

# --- PITCH ANGLE ---
# 4 is ???deg
# Channel 14:  0deg (particles coming down the field)
# 15 and 13 are 22.5 deg
# 12 is 45 deg  (16 is special see below)
# 1 and 11 67.5 deg
# 2 and 10 90 deg
# 3 and 9  112.5deg
# 16 and 8   135deg
# 5 and 7  157.5 deg
# 6   180 deg
channel_map = np.array([4,14,13,15,12,1,11,2,10,3,9,16,8,5,7,6])-1
pitch = [0,0,22.5,22.5,45,67.5,67.5,90,90,112.5,112.5,135,135,157.5,157.5,180]


#---------------------------------------------------------------------
# CALCULATE THE IGNORED ENDING INDICIES AND THE NUMBER OF LOOPS NEEDED
#---------------------------------------------------------------------\
# data = [ESA1_sweepDAC1,ESA1_sweepDAC2,ESA2_sweepDAC1,ESA2_sweepDAC2]
# dataactual = [[] for i in range(4)]
#
# print(data[0][0:50])
# print(data[1][0:50])
# print(data[2][0:50])
# print(data[3][0:50])
#
# first_sweep_starts = []
#
# for i in range(4):
#     for j in range(len(data[0])):
#         if data[i][j] == 129:
#             first_sweep_starts.append(j)
#             break
# print(first_sweep_starts)



# Clump the data by the respective length of energy values and sort it into the appropriate array
# for i in selects:
#     # print(len(Energies_DAC),SWEEPdata[i][0:10],len(SWEEPdata[i]),len(SWEEPdata[i])%len(Energies_DAC) )
#     print(len(Energies_DAC), SWEEPdata[i][0:10], len(SWEEPdata[i]), len(SWEEPdata[i])%len(Energies_DAC),len(SWEEPdata[i][0:(len(SWEEPdata[i]))]) / len(Energies_DAC)   )

No_of_needed_loops = [11137,11137,14718,14719] #How many loops will be needed for proper clumping of each DATSWEEP


#---------------------------------------------------------------------------------------------------------------------------
# CREATE 3D DATA VARIABLE: time vs PitchAngle vs Energies (indexed so 0 --> highest energy and last index is lowest energiy)
#---------------------------------------------------------------------------------------------------------------------------

#Create the storage variables that will be filled later
ESA1_sensor1_data_reduced = [dat[first_sweep_starts[0]:(len(dat) - ignored_indicies[0])] for dat in ESA1_sensor1_data]
ESA1_sensor2_data_reduced = [dat[first_sweep_starts[1]:(len(dat) - ignored_indicies[1])] for dat in ESA1_sensor2_data]
ESA2_sensor1_data_reduced = [dat[first_sweep_starts[2]:(len(dat) - ignored_indicies[2])] for dat in ESA2_sensor1_data]
ESA2_sensor2_data_reduced = [dat[first_sweep_starts[3]:(len(dat) - ignored_indicies[3])] for dat in ESA2_sensor2_data]

ESA1_sensor1_counts = np.zeros(shape=(No_of_needed_loops[0],len(pitch),len(Energies_DAC)))
ESA1_sensor2_counts = np.zeros(shape=(No_of_needed_loops[1],len(pitch),len(Energies_DAC)))
ESA2_sensor1_counts = np.zeros(shape=(No_of_needed_loops[2],len(pitch),len(Energies_DAC)))
ESA2_sensor2_counts = np.zeros(shape=(No_of_needed_loops[3],len(pitch),len(Energies_DAC)))

ESA1_sensor1_DACvals = np.zeros(shape=(No_of_needed_loops[0],len(Energies_DAC)))
ESA1_sensor2_DACvals = np.zeros(shape=(No_of_needed_loops[1],len(Energies_DAC)))
ESA2_sensor1_DACvals = np.zeros(shape=(No_of_needed_loops[2],len(Energies_DAC)))
ESA2_sensor2_DACvals = np.zeros(shape=(No_of_needed_loops[3],len(Energies_DAC)))

ESA1_sensor1_times = np.zeros(shape=(No_of_needed_loops[0],len(Energies_DAC)))
ESA1_sensor2_times = np.zeros(shape=(No_of_needed_loops[1],len(Energies_DAC)))
ESA2_sensor1_times = np.zeros(shape=(No_of_needed_loops[2],len(Energies_DAC)))
ESA2_sensor2_times = np.zeros(shape=(No_of_needed_loops[3],len(Energies_DAC)))

ESA1_sensor1_epoch = np.zeros(shape=(No_of_needed_loops[0]))
ESA1_sensor2_epoch = np.zeros(shape=(No_of_needed_loops[1]))
ESA2_sensor1_epoch = np.zeros(shape=(No_of_needed_loops[2]))
ESA2_sensor2_epoch = np.zeros(shape=(No_of_needed_loops[3]))

ESA1_sensor1_sweep_duration = np.zeros(shape=(No_of_needed_loops[0]))
ESA1_sensor2_sweep_duration = np.zeros(shape=(No_of_needed_loops[1]))
ESA2_sensor1_sweep_duration = np.zeros(shape=(No_of_needed_loops[2]))
ESA2_sensor2_sweep_duration = np.zeros(shape=(No_of_needed_loops[3]))




ESA_sensor_data_reduced = [ESA1_sensor1_data_reduced,ESA1_sensor2_data_reduced,ESA2_sensor1_data_reduced,ESA2_sensor2_data_reduced]
counts_output = [ESA1_sensor1_counts,ESA1_sensor2_counts,ESA2_sensor1_counts,ESA2_sensor2_counts]
ESA_sensor_times = [ESA1_sensor1_times,ESA1_sensor2_times,ESA2_sensor1_times,ESA2_sensor2_times]
ESA_sensor_DACvals = [ESA1_sensor1_DACvals,ESA1_sensor2_DACvals,ESA2_sensor1_DACvals,ESA2_sensor2_DACvals]
ESA_sensor_epochs = [ESA1_sensor1_epoch,ESA1_sensor2_epoch,ESA2_sensor1_epoch,ESA2_sensor2_epoch]
ESA_sensor_sweep_durations = [ESA1_sensor1_sweep_duration,ESA1_sensor2_sweep_duration,ESA2_sensor1_sweep_duration,ESA2_sensor2_sweep_duration]

for select in selects:
    wengy = Energies_DAC
    wSWEEPs = SWEEPdata[select]
    clump_size = len(wengy)
    wDACvals = ESA_sensor_DACvals[select]
    wESA_sensor_Times = ESA_sensor_times[select]
    wcounts = counts_output[select]
    wESA_sensor_data_reduced = ESA_sensor_data_reduced[select]
    wSensor_Epoch = ESA_sensor_epochs[select]
    wSWEEPduration = ESA_sensor_sweep_durations[select]

    #Select the time
    if select == 0 or select == 1:
        wtime = ESAtimes[0]
    elif select== 2 or select == 3:
        wtime = ESAtimes[1]


    # for i in range(No_of_needed_loops[select]):
    for i in range(No_of_needed_loops[select]):

        if i % 200 == 0:
            print('Storing data for ' + sensor_names[select] + ': ' + str(round(100 * (i / No_of_needed_loops[select]), 1)) + '%', end='\r')
        elif i == (No_of_needed_loops[select] - 1):
            print('Storing data for ' + sensor_names[select] + ':' + ' 100%')

        clump_start = (0 + i *clump_size)
        clump_end = (clump_size +  i *clump_size)

        wDACvals[i] = wSWEEPs[clump_start:clump_end]
        wESA_sensor_Times[i] = wtime[clump_start:clump_end]
        wSensor_Epoch[i] = wtime[clump_start]
        wSWEEPduration[i] = sum(wtime[clump_start:clump_end])


        #Store data by pitch
        for j in range(len(channel_map)):
            wcounts[i][j] = wESA_sensor_data_reduced[channel_map[j]][clump_start:clump_end]

    # -------------------------
    # CREATE THE EPOCH VARIABLE
    # -------------------------
    wSensor_Epoch_tt2000 = np.array((wSensor_Epoch)*(10**(9)) + Epochs_start_tt2000,dtype='float64')

    #-------------------
    # WRITE OUT THE DATA
    # -------------------

    print(0)
    #COUNTS
    vardata = wcounts
    attrs = ['counts', [-1.e+31], [vardata.min()], [vardata.max()], 'linear', 'counts', 'nnspectrogram']
    infos = [0, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': 'ESA', 'DEPEND_0': 'epoch', 'DEPEND_1 ': 'pitch_angle','DEPEND_2':'energy', 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': 'ESA', 'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 2,
               'Dim_Sizes': [len(pitch),len(Energies_DAC)], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print(1)
    # ESA SENSOR DATA POINT TIME OCCURANCE
    vardata = wESA_sensor_Times
    attrs = ['ESA_data_time_since_launch', [-1.e+31], [vardata.min()], [vardata.max()], 'linear', 'seonds', 'nnspectrogram']
    infos = [1, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DEPEND_0': 'epoch', 'DEPEND_1': 'energy',
                     'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'LABL_PTR_1': 'eepaa_LABL_1', 'LABL_PTR_2': 'eepaa_LABL_2', 'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 1,
               'Dim_Sizes': [len(Energies_DAC)], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print(2)
    # EPOCH
    vardata = wSensor_Epoch_tt2000
    # vardata = wSensor_Epoch
    attrs = ['epoch', [-1.e+31], [vardata.min()], [vardata.max()], 'linear', 'ns', 'series']
    infos = [2, 33, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'LABL_PTR_1': attrs[5], 'LABL_PTR_2': 'eepaa_LABL_2', 'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'support_data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': 'CDF_TIME_TT2000', 'Num_Elements': 1, 'Num_Dims': 0,
               'Dim_Sizes': [], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='int64'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    # vardata = np.array(roll_output_epoch[select], dtype='float64')
    # attributes = ['Roll_Epoch', 'ns', 'linear', vardata.min(), vardata.max(),counts_file_low.varattsget(zvars_counts_low[0], expand=True)]
    # attrs = attributes[5]
    # attrs['VAR_TYPE'] = 'support_data'
    # attributes[5] = attrs
    # varinfo = counts_file_low.varinq(zvars_counts_low[0])
    # write_var_to_file(sun_spike_noise_file_low, varinfo, vardata, attributes)



    print(3)
    # ENERGY
    vardata = np.array(Energies_DAC, dtype='float64')
    attrs = ['energy', [-1.e+31], [vardata.min()], [vardata.max()], 'linear', 'DAC_val_units', 'series']
    infos = [3, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'LABL_PTR_1': attrs[5], 'LABL_PTR_2': 'eepaa_LABL_2', 'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE':'Support_data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 1,
               'Dim_Sizes': [], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print(4)
    # PITCH
    vardata = np.array(pitch, dtype='float64')
    attrs = ['pitch_angle', [-1.e+31], [vardata.min()], [vardata.max()], 'linear', 'deg', 'series']
    infos = [4, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'LABL_PTR_1': attrs[5], 'LABL_PTR_2': 'eepaa_LABL_2', 'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'Support_data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 1,
               'Dim_Sizes': [], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print(5)
    # SWEEP DURATION
    vardata = wSWEEPduration
    attrs = ['Sweep_duration', [-1.e+31], [vardata.min()], [vardata.max()], 'linear', 'seconds', 'series']
    infos = [5, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'LABL_PTR_1': attrs[5], 'LABL_PTR_2': 'eepaa_LABL_2', 'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'Support_data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 1,
               'Dim_Sizes': [], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)
    print(6)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

print("--- %s seconds for Initial_data_processing---" % (time.time() - start_time) ,'\n')