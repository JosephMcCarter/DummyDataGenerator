import pandas as pd
import random
import datetime
import numpy as np
import math
from apscheduler.schedulers.blocking import BlockingScheduler


#Input start time in DD-MM-YYYY HH:MM:SS.ms format
#Input boxID
#Input mean
#Input standard deviation
StartTime = datetime.datetime.strptime(raw_input('Race start time (DD-MM-YYYY HH:MM:SS.ms format): '), "%d-%m-%Y %H:%M:%S.%f")
boxID = raw_input('Enter BoxID: ')
mean = int(raw_input('Enter mean for offset: '))
std = int(raw_input('Enter standard deviation for offset: '))


def uniformFloat(lo, hi):
    """
    Return a number chosen uniformly from the range [lo, hi).
    """
    return random.uniform(lo, hi)

def gaussian(mean=0.0, stddev=1.0):
    """
    Return a float according to a standard Gaussian distribution
    with the given mean (mean) and standard deviation (stddev).
    """
    # Approach 2: Use the polar form of the Box-Muller transform.
    x = uniformFloat(-1.0, 1.0)
    y = uniformFloat(-1.0, 1.0)
    r = x*x + y*y
    while (r >= 1) or (r == 0):
        x = uniformFloat(-1.0, 1.0)
        y = uniformFloat(-1.0, 1.0)
        r = x*x + y*y
    g = x * math.sqrt(-2 * math.log(r) / r)
    # Remark:  x * math.sqrt(-2 * math.log(r) / r)
    # is an independent random gaussian
    global offset
    offset = mean + stddev * g
    return offset


def Triangle1():
    """
    Model 1 - Long rise/short fall.
    """

    print "Using Triangle1"
    Tri1Trise = np.arange(-100, -30, random.randint(1,11)).tolist()
    Tri1Tfall = np.arange(-100, max(Tri1Trise), random.randint(1,2))[::-1].tolist()
    global TriangelOffset
    TriangleReturn = (Tri1Trise + Tri1Tfall)
    gaussian(mean, std)
    TriangelOffset = [x+offset for x in TriangleReturn]

    return TriangelOffset


def Triangle2():
    """
    Model 2 - short rise/long fall.
    """

    print "Using Triangle2"
    Tri2Trise = np.arange(-100, -30, random.randint(1,2)).tolist()
    Tri2Tfall = np.arange(-100, max(Tri2Trise), random.randint(1,11))[::-1].tolist()
    global TriangelOffset
    TriangleReturn = (Tri2Trise + Tri2Tfall)
    gaussian(mean, std)
    TriangelOffset = [x + offset for x in TriangleReturn]

    return TriangelOffset


def Triangle3():
    """
    Model 3 - even rise/even fall.
    """

    print "Using Triangle3"
    Tri3Trise = np.arange(-100, -30, random.randint(1,5)).tolist()
    Tri3Tfall = np.arange(-100, max(Tri3Trise), random.randint(1,5))[::-1].tolist()
    global TriangelOffset
    TriangleReturn = (Tri3Trise + Tri3Tfall)
    gaussian(mean, std)
    TriangelOffset = [x + offset for x in TriangleReturn]

    return TriangelOffset


def BoxStack():
    """
    Return boxID from input.
    """

    global boxID
    return boxID

def AntennaStack():
    """
    Return Antenna number from 4 choices.
    """

    ants = ['Ant1', 'Ant2', 'Ant3', 'Ant4']
    antennas = random.choice(ants)
    return antennas

def ChipIDStack():

    """
    Return chipID from in the format of 8 digits filled with zeros.
    ChipID numbers are ranged between 1-300
    """

    global ChipID
    ChipID = format(random.randint(1, 300), '08')
    return ChipID

def FunctionStack():
    """
    Return model at random - Triangle 1 or 2 or 3.
    """

    FuncList = [Triangle1, Triangle2, Triangle3]
    random.choice(FuncList)()


TransactionPlus = StartTime

def TimeGenerator():
    global TransactionPlus
    global StartTime

    Trans1 = datetime.timedelta(milliseconds=random.randint(10, 20))

    Trans2 = datetime.timedelta(milliseconds=random.randint(20, 30))

    Trans3 = datetime.timedelta(milliseconds=random.randint(30, 40))

    Trans4 = datetime.timedelta(milliseconds=random.randint(35, 37))

    Trans5 = datetime.timedelta(milliseconds=random.randint(42, 56))

    Trans6 = datetime.timedelta(milliseconds=random.randint(15, 35))

    TransactionTimeList = [Trans1, Trans2, Trans3, Trans4, Trans5, Trans6]

    Trans = random.choice(TransactionTimeList)

    TransactionPlus += Trans
    return TransactionPlus


df = pd.DataFrame()
def DataFrameStacker():
    """
    Dataframe stacker - generates dataframe using other previoulsy defined functions
    Dataframe is generated using python lists then zipped together using zip()
    """

    global df
    FunctionStack()
    ChipIDStack()
    TimeGenerator()
    TimeStacker = [TimeGenerator() for i in range(len(TriangelOffset))]
    ChipIDStacker = [ChipID for i in range(len(TriangelOffset))]
    AntennaStacker = [AntennaStack() for i in range(len(ChipIDStacker))]
    BoxStacker = [boxID for i in range(len(AntennaStacker))]
    f = zip(TimeStacker,ChipIDStacker, AntennaStacker, TriangelOffset, BoxStacker)
    df = df.append(f, ignore_index=True)
    print df

# Scheduler with starts runs functions at random intervals
scheduler = BlockingScheduler()
scheduler.add_job(DataFrameStacker, 'interval', seconds=random.randint(0,10))
scheduler.start()



