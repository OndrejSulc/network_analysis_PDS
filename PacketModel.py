import enum
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
    this.time_window = time_window
    time_window.addPacket(this)
#########################################


#########################################
class TimeWindow:
  def __init__(self):
    self.total_packets_count = 0
    self.lower_region_count = 0
    self.upper_region_count = 0

    self.packets = []


  def addPacket(self, packet):
    this.packets.append(packet)


  def CreateTimeWindows(packets_array, time_window_length):
    TimeWindows = [TimeWindow()]
    elapsedTime = 0
    
    for i in range( len(packets_array)-1 ):
      elapsedTime += packets_array[i].deltaT
      if(elapsedTime > time_window_length):
          TimeWindows.append( TimeWindow() )
          elapsedTime -= time_window_length

      packets_array[i].insertIntoTimeWindow( TimeWindows[-1] )
    
    return TimeWindows
#########################################
   

#########################################
class DirectionModel:

  def __init__(self, direction,packets):
    self.direction = direction
    self.packets = packets


  def createProfile(self):
    pass


  def bestSplitPoint(self, directionArray, time_windows_length ):
    deltaTarray = []
    for model in directionArray:
      deltaTarray.append(model.deltaT)

    deltaTarray.sort()


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