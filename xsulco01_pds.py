from Models import *
from Plotting import *
from scapy.all import *
import json

def filter_communication():
   inFile = sys.argv[2]
   outFile = sys.argv[3]

   result = os.system("tshark -Y iec60870_104 -r {} -w {}".format(inFile, outFile))
   if(result != 0):
      print("Chyba při využití programu tshark.")
      exit(1)
   else:
      print("Soubor {} vytvořen.".format(outFile))



def test_communication_profile():
   profilesFile = open(sys.argv[2],"r")
   profiles = json.load(profilesFile)

   FROM_profile = Profile(**profiles[0])
   TO_profile = Profile(**profiles[1])

   reader = PcapReader(sys.argv[3]) 
   probeIP = sys.argv[4]

   allPackets = PacketModel.CreatePacketModels(reader,probeIP)

   if(len(allPackets) == 0):
      print("Seznam packetů po filtrování probeIP je prázdný.")
      return

   #split packets into 'FROM' and 'TO' sets
   Direction_Models = DirectionModel.CreateDirectionModels(allPackets,probeIP)

   for tw in Direction_Models[0].time_windows:
        tw.gatherCharacteristics(FROM_profile.split_point)
   
   for tw in Direction_Models[1].time_windows:
        tw.gatherCharacteristics(TO_profile.split_point)

   print(FROM_profile.direction, Direction_Models[0].direction)
   detect_anomallies(sys.argv[1], Direction_Models[0], FROM_profile)

   print(TO_profile.direction, Direction_Models[1].direction)
   detect_anomallies(sys.argv[1], Direction_Models[1], TO_profile)

   if( len(sys.argv) == 6 and sys.argv[5] == "-g"):
      plot_number_of_packets_in_time_windows(Direction_Models[0], FROM_profile.direction)
      plot_number_of_packets_in_time_windows(Direction_Models[1],TO_profile.direction)

      plot_total_packets_count(Direction_Models[0], FROM_profile, FROM_profile.direction)
      plot_total_packets_count(Direction_Models[1], TO_profile, TO_profile.direction)

      plot_lower_region_count(Direction_Models[0], FROM_profile, FROM_profile.direction)
      plot_lower_region_count(Direction_Models[1], TO_profile, TO_profile.direction)

      plot_upper_region_count(Direction_Models[0], FROM_profile, FROM_profile.direction)
      plot_upper_region_count(Direction_Models[1], TO_profile, TO_profile.direction)



def create_profile_of_communication():

   #specify learn file and parameters
   reader = PcapReader(sys.argv[2]) 
   probeIP = sys.argv[3]

   allPackets = PacketModel.CreatePacketModels(reader,probeIP)

   if(len(allPackets) == 0):
      print("Seznam packetů po filtrování probeIP je prázdný.")
      return

   #split packets into 'FROM' and 'TO' sets
   Direction_Models = DirectionModel.CreateDirectionModels(allPackets,probeIP)

   #create profiles for each direction
   Direction_Models[0].createProfile() #FROM
   Direction_Models[1].createProfile() #TO

   ModelsJSON = json.dumps( [ Direction_Models[0].profile.__dict__, Direction_Models[1].profile.__dict__] )

   print(ModelsJSON)



if __name__ == "__main__":
   if( sys.argv[1] == "-p"):
      create_profile_of_communication()

   elif( sys.argv[1] == "-t" or sys.argv[1] == "-t3" ):
      test_communication_profile()
   
   elif( sys.argv[1] == "-f"):
      filter_communication()
   
   else:
      if(sys.argv[1] != "-h"):
         print("unknown parameter ",sys.argv[1])

      print("""Help:
-p  <learn.pcapng> <probeIP>                         Na standardní výstup vypíše JSON s profily komunikace v daném souboru. Pomocí probeIP určuje směr.

-t  <profile.json> <soubor.pcapng> <probeIP> [-g]    Provede test zda komunikace v souboru odpovídá profilu. Test provadí pro každé okno samostatně. (-g zobrazení grafů)

-t3 <profile.json> <soubor.pcapng> <probeIP> [-g]    Provede test zda komunikace v souboru odpovídá profilu. Test provadí pro sekvence 3 oken. (-g zobrazení grafů)

-f  <soubor.pcapng> <out.pcapng>                     Ze souboru vyfiltruje IEC komunikaci a uloží ji do výstupního souboru.

-h                                                   Vypíše tento text
""")


