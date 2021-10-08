########MY FUNCTIONS##########
import numpy as np,datetime,math
from bisect import bisect_left


def getMagdat(file):
    xdat = np.transpose(file.varget('MagX'))
    ydat = np.transpose(file.varget('MagY'))
    zdat = np.transpose(file.varget('MagZ'))

    Magdat = np.transpose( np.array([xdat[:][1],ydat[:][1],zdat[:][1]]))

    return Magdat

def UTCtoTT2000(time):
    object = datetime.datetime.utcfromtimestamp(time)
    output = [0,0,0,0,0,0,0,0,0]
    output[0] = object.year
    output[1] = object.month
    output[2] = object.day
    output[3] = object.hour
    output[4] = object.minute
    output[5] = object.second
    output[6] = math.floor(object.microsecond/1000)
    output[7] = object.microsecond % 1000
    return output

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        # return myList[0],pos
        return pos
    if pos == len(myList):
        # return myList[-1],pos
        return pos
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       # return after,pos
       return pos
    else:
       # return before,pos-1
       return pos - 1





# # Functions
# def dataplacer_high(time_index, pitch_index,energy_index):
#     if not isinstance(DiffE_list_high[time_index][pitch_index][energy_index], list):
#         DiffE_list_high[time_index][pitch_index][energy_index] = [DiffEFlux_high[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffE_list_high[time_index][pitch_index][energy_index], list):
#         DiffE_list_high[time_index][pitch_index][energy_index].append(DiffEFlux_high[time_index][pitch_index][energy_index])
#
#     if not isinstance(DiffN_list_high[time_index][pitch_index][energy_index],list):
#         DiffN_list_high[time_index][pitch_index][energy_index] = [DiffNFlux_high[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffN_list_high[time_index][pitch_index][energy_index],list):
#         DiffN_list_high[time_index][pitch_index][energy_index].append(DiffNFlux_high[time_index][pitch_index][energy_index])
#
# def dataplacerchecker_high(time_index, pitch_index,energy_index,checker):
#     if not isinstance(DiffE_list_high[time_index][checker][energy_index], list):
#         DiffE_list_high[time_index][checker][energy_index] = [DiffEFlux_high[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffE_list_high[time_index][checker][energy_index], list):
#         DiffE_list_high[time_index][checker][energy_index].append(DiffEFlux_high[time_index][pitch_index][energy_index])
#
#     if not isinstance(DiffN_list_high[time_index][checker][energy_index], list):
#         DiffN_list_high[time_index][checker][energy_index] = [DiffNFlux_high[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffN_list_high[time_index][checker][energy_index], list):
#         DiffN_list_high[time_index][checker][energy_index].append(DiffNFlux_high[time_index][pitch_index][energy_index])
#
# def dataplacer_low(time_index, pitch_index, energy_index):
#     if not isinstance(DiffE_list_low[time_index][pitch_index][energy_index], list):
#         DiffE_list_low[time_index][pitch_index][energy_index] = [DiffEFlux_low[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffE_list_low[time_index][pitch_index][energy_index], list):
#         DiffE_list_low[time_index][pitch_index][energy_index].append(DiffEFlux_low[time_index][pitch_index][energy_index])
#
#     if not isinstance(DiffN_list_low[time_index][pitch_index][energy_index], list):
#         DiffN_list_low[time_index][pitch_index][energy_index] = [DiffNFlux_low[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffN_list_low[time_index][pitch_index][energy_index], list):
#         DiffN_list_low[time_index][pitch_index][energy_index].append(DiffNFlux_high[time_index][pitch_index][energy_index])
#
# def dataplacerchecker_low(time_index, pitch_index, energy_index, checker):
#     if not isinstance(DiffE_list_low[time_index][checker][energy_index], list):
#         DiffE_list_low[time_index][checker][energy_index] = [DiffEFlux_low[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffE_list_low[time_index][checker][energy_index], list):
#         DiffE_list_low[time_index][checker][energy_index].append(DiffEFlux_low[time_index][pitch_index][energy_index])
#
#     if not isinstance(DiffN_list_low[time_index][checker][energy_index], list):
#         DiffN_list_low[time_index][checker][energy_index] = [DiffNFlux_low[time_index][pitch_index][energy_index]]
#
#     elif isinstance(DiffN_list_low[time_index][checker][energy_index], list):
#         DiffN_list_low[time_index][checker][energy_index].append(DiffNFlux_low[time_index][pitch_index][energy_index])


def write_var_to_file(outputfile,varinfo,vardata,attributes):
    varinfo['Variable'] = attributes[0]
    varattrs = attributes[5]
    varattrs['CATDESC'] = attributes[0]
    varattrs['FIELDNAM'] = attributes[0]
    varattrs['UNITS'] = attributes[1]
    varattrs['SCALETYP'] = attributes[2]
    varattrs['VALIDMIN'] = [attributes[3],'CDF_FLOAT']
    varattrs['VALIDMAX'] = [attributes[4],'CDF_FLOAT']
    varattrs['LABLAXIS'] = attributes[0]
    varattrs['LABL_PTR_1'] = 'LABL_PTR_1'
    varattrs['LABL_PTR_2'] = 'LABL_PTR_2'
    outputfile.write_var(varinfo, var_attrs=varattrs, var_data=vardata)



def write_var_to_file_attitude(outputfile,varinfo,vardata,attributes):
    varinfo['Variable'] = attributes[0]

    varattrs = attributes[5]
    varattrs['CATDESC'] = attributes[0]
    varattrs['DEPEND_0'] = attributes[0]
    varattrs['FIELDNAM'] = attributes[0]
    varattrs['UNITS'] = attributes[1]
    varattrs['SCALETYP'] = attributes[2]
    varattrs['VALIDMIN'] = [attributes[3],'CDF_FLOAT']
    varattrs['VALIDMAX'] = [attributes[4],'CDF_FLOAT']
    varattrs['LABLAXIS'] = attributes[0]
    varattrs['LABL_PTR_1'] = 'LABL_PTR_1'
    varattrs['LABL_PTR_2'] = 'LABL_PTR_2'
    outputfile.write_var(varinfo, var_attrs=varattrs, var_data=vardata)


def printvarinfo(file,zvars,indices):
    for i in indices:
        print('-----',zvars[i],'VARIABLE PARAMETERS-----')
        varinq = file.varinq(zvars[i])
        for thing in varinq:
            print(thing,': ',varinq[thing])

        print('\n')
        print('-----', zvars[i], 'Attribute PARAMETERS-----')
        varatt = file.varattsget(zvars[i])
        for thing in varatt:
            print(thing, ': ', varatt[thing])
        print('\n' * 2)
        # for thing in range(len(indices)):
        #     print(file.varget(zvars[indices[thing]]),'\n')




