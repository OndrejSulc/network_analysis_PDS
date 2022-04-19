from asyncio.windows_events import NULL
import enum
from enum import Enum
from operator import mod
import this
from scapy.all import *

class Direction(Enum):
  TO = 0
  FROM = 1

class TimeWindow:

  def __init__(self, id):
    self.id = id
    self.packets = []

  def addPacket(packet):
    this.packets.append(packet)
  


class PacketModel:

  def __init__(self, deltaT, direction, packet):
    self.deltaT = deltaT
    self.direction = direction
    self.packet = packet

  def insertIntoTimeWindow(time_window):
    this.time_window = time_window
    time_window.addPacket(this)
    

def BestSplitPoint( directionArray, time_windows_length ):
  deltaTarray = []
  for model in directionArray:
    deltaTarray.append(model.deltaT)

  deltaTarray.sort()


    

def determineDirection ( probeIPaddr, packet):
  if(packet[IP].src == probeIPaddr):
    return Direction.FROM
  
  else:
    return Direction.TO