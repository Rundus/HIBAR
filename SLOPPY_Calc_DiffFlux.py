


import time

start_time = time.time()
print('importing variables: ', end='')
import numpy as np
import itertools
from cdflib import cdfwrite
from Variables import ESA1_sensor1_L0_counts,ESA1_sensor2_L0_counts,ESA2_sensor1_L0_counts,ESA2_sensor2_L0_counts,Deadtime,geometric_factor,Energies_ion,Energies_electron
from Variables import ESA1_sensor1_L0_SweepDuration,ESA1_sensor2_L0_SweepDuration,ESA2_sensor1_L0_SweepDuration,ESA2_sensor2_L0_SweepDuration,ESA1_sensor1_L0_epoch,ESA1_sensor2_L0_epoch,ESA2_sensor1_L0_epoch,ESA2_sensor2_L0_epoch
from Variables import ESA1_info,ESA2_info,pitch,sensor_names,acquisition_interval
from Files import user_path,root,output_root,ESA1_sensor1_L0_file,ESA2_sensor2_L0_file



#---------------------
# --- OUTPUT FILES ---
#---------------------
ESA1_sensor1_diffFlux_file = cdfwrite.CDF(user_path + root + output_root + 'ESA1_sensor1_DiffFlux_data',cdf_spec=ESA1_info,delete=True)
ESA1_sensor2_diffFlux_file = cdfwrite.CDF(user_path + root + output_root + 'ESA1_sensor2_DiffFlux_data',cdf_spec=ESA1_info,delete=True)
ESA2_sensor1_diffFlux_file = cdfwrite.CDF(user_path + root + output_root + 'ESA2_sensor1_DiffFlux_data',cdf_spec=ESA2_info,delete=True)
ESA2_sensor2_diffFlux_file = cdfwrite.CDF(user_path + root + output_root + 'ESA2_sensor2_DiffFlux_data',cdf_spec=ESA2_info,delete=True)

output_files = [ESA1_sensor1_diffFlux_file,ESA1_sensor2_diffFlux_file,ESA2_sensor1_diffFlux_file,ESA2_sensor2_diffFlux_file]

#-------------------------
# --- OUTPUT VARIABLES ---
#-------------------------


ESA1_sen1_diffN = np.zeros(shape=(len(ESA1_sensor1_L0_counts),len(ESA1_sensor1_L0_counts[0]),len(ESA1_sensor1_L0_counts[0][0])-1))
ESA1_sen1_diffE = np.zeros(shape=(len(ESA1_sensor1_L0_counts),len(ESA1_sensor1_L0_counts[0]),len(ESA1_sensor1_L0_counts[0][0])-1))

ESA1_sen2_diffN = np.zeros(shape=(len(ESA1_sensor2_L0_counts),len(ESA1_sensor2_L0_counts[0]),len(ESA1_sensor2_L0_counts[0][0])-1))
ESA1_sen2_diffE = np.zeros(shape=(len(ESA1_sensor2_L0_counts),len(ESA1_sensor2_L0_counts[0]),len(ESA1_sensor2_L0_counts[0][0])-1))

ESA2_sen1_diffN = np.zeros(shape=(len(ESA2_sensor1_L0_counts),len(ESA2_sensor1_L0_counts[0]),len(ESA2_sensor1_L0_counts[0][0])-1))
ESA2_sen1_diffE = np.zeros(shape=(len(ESA2_sensor1_L0_counts),len(ESA2_sensor1_L0_counts[0]),len(ESA2_sensor1_L0_counts[0][0])-1))

ESA2_sen2_diffN = np.zeros(shape=(len(ESA2_sensor2_L0_counts),len(ESA2_sensor2_L0_counts[0]),len(ESA2_sensor2_L0_counts[0][0])-1))
ESA2_sen2_diffE = np.zeros(shape=(len(ESA2_sensor2_L0_counts),len(ESA2_sensor2_L0_counts[0]),len(ESA2_sensor2_L0_counts[0][0])-1))

ESA_counts = [ESA1_sensor1_L0_counts,ESA1_sensor2_L0_counts,ESA2_sensor1_L0_counts,ESA2_sensor2_L0_counts]
ESA_diffN = [ESA1_sen1_diffN,ESA1_sen2_diffN,ESA2_sen1_diffN,ESA2_sen2_diffN]
ESA_diffE = [ESA1_sen1_diffE,ESA1_sen2_diffE,ESA2_sen1_diffE,ESA2_sen2_diffE]
ESA_epochs = [ESA1_sensor1_L0_epoch,ESA1_sensor2_L0_epoch,ESA2_sensor1_L0_epoch,ESA2_sensor2_L0_epoch]
ESA_SweepDuration = [ESA1_sensor1_L0_SweepDuration,ESA1_sensor2_L0_SweepDuration,ESA2_sensor1_L0_SweepDuration,ESA2_sensor2_L0_SweepDuration]


# --- Some Variables ---
selects = [0,1,2,3]

print('Done')

#---------------------------
# --- CALCULATE DIFFFLUX ---
#---------------------------


for select in selects:
    wCounts = ESA_counts[select]
    wDiffN = ESA_diffN[select]
    wDiffE = ESA_diffE[select]
    range_limits = [len(wDiffN),len(wDiffN[0]),len(wDiffN[0][0])]
    ranges = [range(range_limits[0]),range(range_limits[1]),range(range_limits[2])]
    wSweepDuration = ESA_SweepDuration[select]
    wEpoch = ESA_epochs[select]

    # if select == 3:
    #     wEngy = [int(Energies_ion[i]) for i in range(len(Energies_ion))]
    # else:
    #     wEngy = [int(Energies_electron[i]) for i in range(len(Energies_electron))]

    if select == 3:
        wEngy = Energies_ion
    else:
        wEngy = Energies_electron


    for tme,ptch,engy in itertools.product(*ranges):

        if tme % 200 == 0:
            print('Calculating Fluxes for ' + sensor_names[select] + ': ' + str(round(100 * (tme / range_limits[0]), 1)) + '%', end='\r')
        elif tme == (range_limits[0] - 1) and ptch == range_limits[1] and engy == range_limits[2]:
            print('Calculating Fluxes for ' + sensor_names[select] + ':' + ' 100%')

        # print(wEngy[engy],wCounts[tme][ptch][engy],geometric_factor,wSweepDuration[tme][engy],Deadtime)

        val = (wSweepDuration[tme][engy] - (wCounts[tme][ptch][engy]*Deadtime)   )
        val = acquisition_interval
        wDiffN[tme][ptch][engy] = (wEngy[engy] * wCounts[tme][ptch][engy]) / (wEngy[engy]*geometric_factor * (val))

        wDiffE[tme][ptch][engy] = (wCounts[tme][ptch][engy]) / (wEngy[engy] * geometric_factor * (val))





    # -------------------
    # WRITE OUT THE DATA
    # -------------------


    # DIFFERNTIAL NUMBER FLUX
    print('Check 0')

    vardata = wDiffN
    attrs = ['Differential_Number_Flux', np.array([-2], dtype='float64'), [vardata.min()], [vardata.max()], 'linear', 'counts!cm!U-2!N str!U-1!N s!U-1!N eV!U-1!N',
             'nnspectrogram']

    infos = [0, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': sensor_names[select] + ' ' + attrs[0], 'DEPEND_0': 'epoch', 'DEPEND_1 ': 'pitch_angle',
                     'DEPEND_2': 'Energy', 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 2,
               'Dim_Sizes': [range_limits[1], range_limits[2]], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print('Check 1')

    # DIFFERNTIAL Energy FLUX
    vardata = wDiffN
    attrs = ['Differential_Energy_Flux', np.array([-2], dtype='float32'), [vardata.min()], [vardata.max()], 'linear','cm!U-2!N str!U-1!N s!U-1!N eV/eV','nnspectrogram']
    infos = [1, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': sensor_names[select] + ' ' + attrs[0], 'DEPEND_0': 'epoch', 'DEPEND_1 ': 'pitch_angle',
                     'DEPEND_2': 'Energy', 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 2,
               'Dim_Sizes': [range_limits[1],range_limits[2]], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print('Check 2')

    # EPOCH
    vardata = np.array(wEpoch,dtype='float64')
    attrs = ['epoch', np.array([-1.e+31], dtype='float64'), [vardata.min()], [vardata.max()], 'linear', 'ns', 'series']
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




    print('Check 3')

    # ENERGY
    vardata = np.array(wEngy[0:(len(wEngy)-1)],dtype='float64')
    attrs = ['Energy', np.array([-1e+31], dtype='float64'), [vardata.min()], [vardata.max()], 'linear', 'eV', 'series']
    infos = [3, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float64'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'UNITS': attrs[5], 'VALIDMIN': attrs[2], 'VALIDMAX': attrs[3], 'VAR_TYPE': 'Support_data',
                     'SCALETYP': attrs[4]}

    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 1,
               'Dim_Sizes': [], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    # if select ==3:
    #     engyfile = ESA2_sensor2_L0_file
    # else:
    #     engyfile = ESA1_sensor1_L0_file
    #
    # engydata = engyfile.varget('Energy')
    # vardata1 = engydata[0]
    # vardata = vardata1[0:(len(vardata1)-1)]
    # info = engyfile.cdf_info()
    # zvars = info['zVariables']
    # varinfo = engyfile.varinq(zvars[3])
    # varinfo['Last_Rec'] = len(vardata)
    # varinfo['Dim_Sizes'] = [len(vardata)]
    # varattributes['VALIDMIN'] = [-30000]
    # varattributes['VALIDMAX'] = [30000]
    # varattributes = engyfile.varattsget(zvars[3])
    # output_files[select].write_var(varinfo,var_attrs =varattributes,var_data= vardata )

    print('Check 4')
    # PITCH
    vardata = pitch[0]
    attrs = ['pitch_angle', np.array([-1.e+31], dtype='float32'), [0], [180], 'linear', 'deg', 'series']
    infos = [4, 44, len(vardata), attrs[0], [-9223372036854775807]]
    varattributes = {'CATDESC': attrs[0], 'DISPLAY_TYPE': attrs[6], 'FIELDNAM': attrs[0],
                     'FILLVAL': np.array(attrs[1], dtype='float32'), 'FORMAT': 'E12.2', 'LABLAXIS': attrs[0],
                     'UNITS': attrs[5], 'VALIDMIN': attrs[2],
                     'VALIDMAX': attrs[3], 'VAR_TYPE': 'Support_data', 'SCALETYP': attrs[4]}
    varinfo = {'Variable': attrs[0], 'Num': infos[0], 'Var_Type': 'zVariable', 'Data_Type': infos[1],
               'Data_Type_Description': infos[3], 'Num_Elements': 1, 'Num_Dims': 1,
               'Dim_Sizes': [len(vardata)], 'Sparse': 'No_sparse', 'Last_Rec': infos[2],
               'Rec_Vary': True, 'Dim_Vary': [], 'Pad': np.array(infos[4], dtype='float32'), 'Compress': 0,
               'Block_Factor': 0}
    output_files[select].write_var(varinfo, var_attrs=varattributes, var_data=vardata)

    print('Check 5')





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

print("--- %s seconds for Initial_data_processing---" % (time.time() - start_time) ,'\n')