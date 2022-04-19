from PacketModel import *
from scapy.all import *

# tshark -2 -R "iec60870_104" -r mega104-17-12-18.pcapng -w pokus2.pcapng
# editcap -c 44196 packetsOfInterest.pcapng out.pcapng

#Process file
#first argument is capture file
"""PcapFile = sys.argv[1]
result = os.system("tshark -Y iec60870_104 -r {} -w packetsOfInterest.pcapng".format(PcapFile))
if(result != 0):
   exit(1)"""

#Time window length in seconds
TIME_WINDOWS_LENGTH = 300


#specify learn file
reader = PcapReader("learn.pcapng") 

probeIP = sys.argv[2]
allPackets = []


#filter packet not containting probes IP + prepare PacketModels
for processedPacket in reader:
   if(processedPacket[IP].src != probeIP and processedPacket[IP].dst != probeIP):
      continue

   allPackets.append( PacketModel(0, determineDirection(probeIPaddr=probeIP, packet=processedPacket), processedPacket) )


#calculate deltaT for each packet + drop last packet (no deltaT)
for i in range( len(allPackets)-1 ):
   allPackets[i].deltaT = allPackets[i+1].packet.time - allPackets[i].packet.time 

allPackets.pop(-1)


#split packets into 'FROM' and 'TO' sets
TOset = []
FROMset = []
for i in range( len(allPackets) ):
   if(allPackets[i].direction == Direction.TO):
      TOset.append(allPackets[i])
   else:
      FROMset.append(allPackets[i])

spTO = BestSplitPoint(TOset,TIME_WINDOWS_LENGTH)
spFROM = BestSplitPoint(FROMset,TIME_WINDOWS_LENGTH)



#incomingPackets = capture.filter()
   


#print(capture[0])
#for packet in capture: 
#   packet.explore()

"""
if packet.haslayer(UDP) and packet.haslayer(IP) and packet.haslayer(Raw): 
   if packet.getlayer(Raw).load == sys.argv[2]: 
      start = packet.time 
   if packet.getlayer(Raw).load == sys.argv[3]: 
      end = packet.time 
      print (end - start)*1000 """