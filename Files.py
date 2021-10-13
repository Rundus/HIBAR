from cdflib import cdfread

# ---------------
# FILE REPOSITORY
# ---------------
user_path = "C:/Users/cfeltman/Desktop/"
root = 'HIBAR/'
output_root ='Output/'
mag36200 = 'mag36200'
eepaa1 = 'hibar_esa1'
eepaa2 = 'hibar_esa2'
MagX = 'MagX'
MagY = 'MagY'
MagZ = 'MagZ'
hibar_gyro_pitch = 'hibar_gyro_pitch'
hibar_gyro_yaw = 'hibar_gyro_yaw'



# -------FILES--------
mag36200_file = cdfread.CDF(user_path + root + "/" + mag36200)
ESA_file_1 = cdfread.CDF(user_path + root + "/" + eepaa1 + '.cdf')
ESA_file_2 = cdfread.CDF(user_path + root + "/" + eepaa2 + '.cdf')
magX_file = cdfread.CDF(user_path + root + '/' + MagX + '.cdf')
magY_file = cdfread.CDF(user_path + root + '/' + MagY + '.cdf')
magZ_file = cdfread.CDF(user_path + root + '/' + MagZ + '.cdf')
hibar_pitch_file = cdfread.CDF(user_path + root + '/' + hibar_gyro_pitch + '.cdf')
hibar_yaw_file = cdfread.CDF(user_path + root + '/' + hibar_gyro_yaw + '.cdf')


# # --- POST-INITIAL DATA PROCESSING FILES ---
ESA1_sensor1_L0_file = cdfread.CDF(user_path+ root  +'ESA1_sensor1_counts_data' + '.cdf' )
ESA1_sensor2_L0_file = cdfread.CDF(user_path+ root  +'ESA1_sensor2_counts_data' + '.cdf' )
ESA2_sensor1_L0_file = cdfread.CDF(user_path+ root  +'ESA2_sensor1_counts_data' + '.cdf' )
ESA2_sensor2_L0_file = cdfread.CDF(user_path+ root  +'ESA2_sensor2_counts_data' + '.cdf' )

# INFORMATION NEEDED FOR EPOCH in Initial_data_processing
root_trice = 'C:/Users/cfeltman/Desktop/TRICE/' # My labtop
counts_file_low = cdfread.CDF(root_trice + 'TRICE_52004_l1_eepaa_20181208T082243_v1.1.2_COUNTS.cdf')