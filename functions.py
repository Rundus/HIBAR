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
    if (after - myNumber) < (myNumber - before):
       #  return after,pos
       return pos
    else:
       #  return before,pos-1
       return pos - 1



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

def dataplacer(time,pitch,engy,Edat,Ndat,Elist,Nlist):
    if not isinstance(Elist[time][pitch][engy], list):
        Elist[time][pitch][engy] = [Edat[time][pitch][engy]]

    elif isinstance(Elist[time][pitch][engy], list):
        Elist[time][pitch][engy].append(Edat[time][pitch][engy])

    if not isinstance(Nlist[time][pitch][engy], list):
        Nlist[time][pitch][engy] = [Ndat[time][pitch][engy]]

    elif isinstance(Nlist[time][pitch][engy], list):
        Nlist[time][pitch][engy].append(Ndat[time][pitch][engy])

def dataplacer_checker(time,pitch,engy,Edat,Ndat,Elist,Nlist,checker):
    if not isinstance(Elist[time][checker][engy], list):
        Elist[time][checker][engy] = [Edat[time][pitch][engy]]

    elif isinstance(Elist[time][checker][engy], list):
        Elist[time][checker][engy].append(Edat[time][pitch][engy])

    if not isinstance(Nlist[time][checker][engy], list):
        Nlist[time][checker][engy] = [Ndat[time][pitch][engy]]

    elif isinstance(Nlist[time][checker][engy], list):
        Nlist[time][checker][engy].append(Ndat[time][pitch][engy])

def write_var_to_file(outputfile,varinfo,vardata,attributes):
    varinfo['Variable'] = attributes[0]
    varattrs = attributes[5]
    varattrs['CATDESC'] = [attributes[0],'CDF_CHAR']
    varattrs['FIELDNAM'] = [attributes[0],'CDF_CHAR']
    varattrs['UNITS'] = [attributes[1],'CDF_CHAR']
    varattrs['SCALETYP'] = [attributes[2],'CDF_CHAR']
    varattrs['VALIDMIN'] = [attributes[3],'CDF_REAL4']
    varattrs['VALIDMAX'] = [attributes[4],'CDF_REAL4']
    varattrs['LABLAXIS'] = [attributes[0],'CDF_CHAR']
    varattrs['LABL_PTR_1'] = ['LABL_PTR_1','CDF_CHAR']
    varattrs['LABL_PTR_2'] = ['LABL_PTR_2','CDF_CHAR']
    outputfile.write_var(varinfo, var_attrs=varattrs, var_data=vardata)


def write_var_to_file_mag(outputfile,varinfo,vardata,attributes):
    varinfo['Variable'] = attributes[0]
    varinfo['Dim_Sizes'] = [1]
    varattrs = attributes[5]
    varattrs['CATDESC'] = [attributes[0],'CDF_CHAR']
    varattrs['FIELDNAM'] = [attributes[0],'CDF_CHAR']
    varattrs['UNITS'] = [attributes[1],'CDF_CHAR']
    varattrs['SCALETYP'] = [attributes[2],'CDF_CHAR']
    varattrs['VALIDMIN'] = [attributes[3],'CDF_REAL4']
    varattrs['VALIDMAX'] = [attributes[4],'CDF_REAL4']
    varattrs['LABLAXIS'] = [attributes[0],'CDF_CHAR']
    # varattrs['LABL_PTR_1'] = ['LABL_PTR_1','CDF_CHAR']
    # varattrs['LABL_PTR_2'] = ['LABL_PTR_2','CDF_CHAR']
    # print('\n-----------ATTRS-----------\n')
    # thing = varattrs
    # for item in thing:
    #     print(item, thing[str(item)])
    # thing = varinfo
    # print('\n-----------INFO-----------\n')
    # for item in thing:
    #     print(item, thing[str(item)])
    outputfile.write_var(varinfo, var_attrs=varattrs, var_data=vardata)