from PacketModel import *
from scapy.all import *
import json

# tshark -2 -R "iec60870_104" -r mega104-17-12-18.pcapng -w pokus2.pcapng
# editcap -c 44196 packetsOfInterest.pcapng out.pcapng

#Process file
#first argument is capture file
"""PcapFile = sys.argv[1]
result = os.system("tshark -Y iec60870_104 -r {} -w packetsOfInterest.pcapng".format(PcapFile))
if(result != 0):
   exit(1)"""



#specify learn file and parameters
reader = PcapReader("learn.pcapng") 
probeIP = sys.argv[2]


#filter packet not containting probes IP + prepare PacketModels
allPackets = []
for processedPacket in reader:
   if(processedPacket[IP].src != probeIP and processedPacket[IP].dst != probeIP):
      continue

   allPackets.append( PacketModel(0, processedPacket) ) #determineDirection(probeIPaddr=probeIP, packet=processedPacket)


#calculate deltaT for each packet, assignTimeWindow + drop last packet (no deltaT)
for i in range( len(allPackets)-1 ):
   allPackets[i].deltaT = allPackets[i+1].packet.time - allPackets[i].packet.time 

allPackets.pop(-1)


#split packets into 'FROM' and 'TO' sets
Direction_Models = DirectionModel.CreateDirectionModels(allPackets,probeIP)

#create profiles for each direction
Direction_Models[0].createProfile() #FROM
Direction_Models[1].createProfile() #TO

FROM_ModelJsonStr = json.dumps(Direction_Models[0].profile.__dict__)
TO_ModelJsonStr = json.dumps(Direction_Models[1].profile.__dict__)

print(FROM_ModelJsonStr)
print(TO_ModelJsonStr)


#print(len(Direction_Models[0].packets))
#print(len(Direction_Models[1].packets))


