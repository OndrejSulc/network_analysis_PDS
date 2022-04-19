import enum
import numpy as np
from enum import Enum
from operator import mod
from scapy.all import *


#Time window length in seconds
TIME_WINDOWS_LENGTH = 120

#########################################
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
class Profile:

  def __init__(self, split_point,
                     total_number_of_packets_lower_bound,
                     total_number_of_packets_upper_bound,
                     lower_region_lower_bound,
                     lower_region_upper_bound,
                     upper_region_lower_bound,
                     upper_region_upper_bound):
    self.split_point = split_point
    self.total_number_of_packets_lower_bound = total_number_of_packets_lower_bound
    self.total_number_of_packets_upper_bound = total_number_of_packets_upper_bound
    self.lower_region_lower_bound = lower_region_lower_bound
    self.lower_region_upper_bound = lower_region_upper_bound
    self.upper_region_lower_bound = upper_region_lower_bound
    self.upper_region_upper_bound = upper_region_upper_bound

  def check_time_window(self, tw):
    tw.gatherCharacteristics(self.split_point)

    if( not (self.total_number_of_packets_lower_bound < tw.total_packets_count and tw.total_packets_count < self.total_number_of_packets_upper_bound)):
      return False
    
    elif( not( self.lower_region_lower_bound < tw.lower_region_count and tw.lower_region_count < self.lower_region_upper_bound)):
      return False
    
    elif( not( self.upper_region_lower_bound < tw.upper_region_count and tw.upper_region_count < self.upper_region_upper_bound)):
      return False

    else:
      return True
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
    self.time_windows = None
    self.split_point = None
    self.profile = None


  def createProfile(self):
    self.time_windows = TimeWindow.CreateTimeWindows(self.packets)

    self.split_point = self.calcBestSplitPoint()

    for tw in self.time_windows:
        tw.gatherCharacteristics(self.split_point)

    TP_array = []
    LR_array = []
    UR_array = []
    for tw in self.time_windows:
      TP_array.append(tw.total_packets_count)
      LR_array.append(tw.lower_region_count)
      UR_array.append(tw.upper_region_count)

    std_TP = np.std(TP_array)
    mean_TP = np.mean(TP_array)

    std_LR = np.std(LR_array)
    mean_LR = np.mean(LR_array)

    std_UR = np.std(UR_array)
    mean_UR = np.std(UR_array)

    self.profile = Profile(self.split_point,
                           (mean_TP - 3*std_TP),
                           (mean_TP + 3*std_TP),
                           (mean_LR - 3*std_LR),
                           (mean_LR + 3*std_LR),
                           (mean_UR - 3*std_UR),
                           (mean_UR + 3*std_LR))


  def calcBestSplitPoint(self):
    deltaTarray = []
    for pm in self.packets:
      deltaTarray.append(pm.deltaT)

    deltaTarray.sort()
    Q1 = np.quantile(deltaTarray,0.25)
    Q2 = np.quantile(deltaTarray,0.5)
    Mean = np.mean(deltaTarray)
    Q3 = np.quantile(deltaTarray,0.75)

    candidates = [Q1,Q2,Mean,Q3]

    #get minStd and best split-point
    bestSplitPoint = None
    minStd = None
    for c in candidates:
      for tw in self.time_windows:
        tw.gatherCharacteristics(c)
    
      (meanC, stdC) = self.get_better_std(self.time_windows)
      if(stdC != 0):
        if(minStd == None or minStd > stdC):
          minStd = stdC
          bestSplitPoint = c

    return bestSplitPoint


  def get_better_std(self, time_windows):
    LR_array = []
    UR_array = []
    for tw in time_windows:
      LR_array.append(tw.lower_region_count)
      UR_array.append(tw.upper_region_count)

    std_LR = np.std(LR_array)
    mean_LR = np.mean(LR_array)
    condition_LR = (mean_LR - 3*std_LR > 0)

    std_UR = np.std(UR_array)
    mean_UR = np.mean(UR_array)
    condition_UR = (mean_UR - 3*std_UR > 0)

    if(condition_LR and condition_UR):
      if(std_LR < std_UR):
        return mean_LR, std_LR
      else:
        return mean_UR, std_UR
    
    elif(condition_LR and not(condition_UR)):
      return mean_LR, std_LR

    elif(not condition_LR and condition_UR):
      return mean_UR, std_UR
    
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