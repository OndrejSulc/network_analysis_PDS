import enum
import numpy as np
from enum import Enum
from operator import mod
from scapy.all import *


#Time window length in seconds
TIME_WINDOWS_LENGTH = 300


class Direction(Enum):
  TO = 0
  FROM = 1

#########################################
class PacketModel:

  def __init__(self, deltaT, packet):
    self.deltaT = deltaT
    self.packet = packet

  def insertIntoTimeWindow(self, time_window):
    self.time_window = time_window
    time_window.addPacket(self)
#########################################


#########################################
class TimeWindow:
  def __init__(self):
    self.total_packets_count = None
    self.lower_region_count = None
    self.upper_region_count = None

    self.packets = []

  def addPacket(self, packet):
    self.packets.append(packet)


  def gatherCharacteristics(self, split_point):
    self.total_packets_count = 0
    self.lower_region_count = 0
    self.upper_region_count = 0

    for p in self.packets:
      self.total_packets_count += 1
      if(p.deltaT < split_point):
        self.lower_region_count += 1
      else:
        self.upper_region_count += 1
    

  # STATIC ------------
  def CreateTimeWindows(packets_array):
    TimeWindows = [TimeWindow()]
    elapsedTime = 0
    
    for i in range( len(packets_array)-1 ):
      elapsedTime += packets_array[i].deltaT
      if(elapsedTime > TIME_WINDOWS_LENGTH):
          TimeWindows.append( TimeWindow() )
          elapsedTime -= TIME_WINDOWS_LENGTH

      packets_array[i].insertIntoTimeWindow( TimeWindows[-1] )
    
    return TimeWindows
#########################################
   

#########################################
class DirectionModel:

  def __init__(self, direction,packets):
    self.direction = direction
    self.packets = packets
    self.split_point = None


  def createProfile(self):
    deltaTs = []
    for pm in self.packets:
        deltaTs.append(pm.deltaT)

    deltaTs.sort()

    self.split_point = self.bestSplitPoint()
    print(self.split_point)
    pass


  def bestSplitPoint(self):
    deltaTarray = []
    for pm in self.packets:
      deltaTarray.append(pm.deltaT)

    deltaTarray.sort()
    Q1 = np.quantile(deltaTarray,0.25)
    Q2 = np.quantile(deltaTarray,0.5)
    Q3 = np.quantile(deltaTarray,0.75)
    Mean = np.mean(deltaTarray)
    TimeWindows = TimeWindow.CreateTimeWindows(self.packets)

    print(Q1,Q2,Mean,Q3)

    minStd = None

    #Q1
    for tw in TimeWindows:
      tw.gatherCharacteristics(Q1)
  
    stdQ1 = self.get_best_std(TimeWindows)
    if(stdQ1 != 0):
      if(minStd == None or minStd > stdQ1):
        minStd = stdQ1

    #Q2
    for tw in TimeWindows:
      tw.gatherCharacteristics(Q2)
  
    stdQ2 = self.get_best_std(TimeWindows)
  
    if(stdQ2 != 0):
      if(minStd == None or minStd > stdQ2):
        minStd = stdQ2

    #Q3
    for tw in TimeWindows:
      tw.gatherCharacteristics(Q3)
  
    stdQ3 = self.get_best_std(TimeWindows)
  
    if(stdQ3 != 0):
      if(minStd == None or minStd > stdQ3):
        minStd = stdQ3

    #Mean
    for tw in TimeWindows:
      tw.gatherCharacteristics(Mean)
  
    stdMean = self.get_best_std(TimeWindows)
  
    if(stdMean != 0):
      if(minStd == None or minStd > stdMean):
        minStd = stdMean

    return minStd


  def get_best_std(self, time_windows):
    LR_array = []
    UR_array = []
    for tw in time_windows:
      LR_array.append(tw.lower_region_count)
      UR_array.append(tw.upper_region_count)

    std_LR = np.std(LR_array)
    mean_LR = np.mean(LR_array)
    condition_LR = (mean_LR - 3*std_LR > 0)

    std_UR = np.std(UR_array)
    mean_UR = np.std(UR_array)
    condition_UR = (mean_UR - 3*std_UR > 0)

    if(condition_LR and condition_UR):
      if(std_LR < std_UR):
        return std_LR
      else:
        return std_UR
    
    elif(condition_LR and not condition_UR):
      return std_LR

    elif(not condition_LR and condition_UR):
      return std_UR
    
    else:
      return 0


  # STATIC ------------
  def CreateDirectionModels(allPackets, probeIPaddr):
    TOset = []
    FROMset = []
    for i in range( len(allPackets) ):
      direction = DirectionModel.DetermineDirection(probeIPaddr, allPackets[i]) 
      if( direction == Direction.TO):
          TOset.append(allPackets[i])
      else:
          FROMset.append(allPackets[i])

    dir_models_array = [DirectionModel(Direction.FROM, FROMset), DirectionModel(Direction.TO, TOset)]
    return dir_models_array


  def DetermineDirection ( probeIPaddr, packet):
    if(packet.packet[IP].src == probeIPaddr):
      return Direction.FROM
    
    else:
      return Direction.TO