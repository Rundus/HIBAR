import numpy as np
from Variables import ESA1_info, ESA2_info,ESA1_data,ESA2_data
from Variables import ESA1_T0,ESA2_T0,ESA1_time,ESA2_time
from Variables import ESA1_sweepDAC1,ESA1_sweepDAC2,ESA2_sweepDAC1,ESA2_sweepDAC2
from Variables import ESA1_T0,ESA2_T0


print(ESA1_info,ESA2_T0)
print(ESA2_info)
#------2. INQUIRE ABOUT ONE VARIABLE INFORMATION--------
#Note: Only works for zVariables
# print(file.varinq("Energy"))

#------3. INQUIRE ABOUT AN ATTRIBUTE--------
# print(file.attinq("Instrument_type"))

#------4. GET A VARIABLES ATTRIBUTE--------
#print(file.varattsget("Energy",expand=True))
# print(file.varattsget("Energy",expand=False))


#------5. GET ALL GLOBAL ATTRIBUTES--------
# print(file.globalattsget())


#------6. GET VARIABLE DATA--------

# print( file.varget("Differential_Energy_Flux",expand=True)  )
# print( file.varget("Pitch_Angle",expand=False)  )

#------7. EPOCHRANGE--------

# print(info["zVariables"])
# print(file.epochrange("Differential_Energy_Flux"))
# print(file.epochrange("Epoch"))

# ------- PRINT SUB-ATTRIBUTE INFORMATION -------

# Attriinquire = file.attinq(attribute=attnum)
# print(file.attinq(attribute=attnum))
#
# for i in range(0, Attriinquire['max_gr_entry']+1):
#     print("\nSub-attribute number " + str(i+1) + " is:")
#     print(file.attget(attribute=attnum, entry=i))

########################################################################################################################################################################################################
