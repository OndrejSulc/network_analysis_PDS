from statistics import mode
import matplotlib.pyplot as plt
 
def plot_total_packets_count(dmodel, profile, direction):

  count = len(dmodel.time_windows)
  
  # lowerBound 
  xLowerB = []
  yLowerB = []
  for i in range(count):
    xLowerB.append(i)
    yLowerB.append(profile.total_number_of_packets_lower_bound)
  
  plt.plot(xLowerB, yLowerB, label = "profile lower bound")

  # upperBound 
  xUpperB = []
  yUpperB = []
  for i in range(count):
    xUpperB.append(i)
    yUpperB.append(profile.total_number_of_packets_upper_bound)
  
  plt.plot(xUpperB, yUpperB, label = "profile upper bound")

  # data
  xData = []
  yData = []
  for i in range(count):
    xData.append(i)
    yData.append(dmodel.time_windows[i].total_packets_count)

  plt.plot(xData, yData, label = "packets count in time window")
  
  # naming the x axis
  plt.xlabel('time windows')
  # naming the y axis
  plt.ylabel('packets count')
  # giving a title to my graph
  plt.title('Total packets count in time windows MODEL:'+ direction)
  # show a legend on the plot
  plt.legend()
  # function to show the plot
  plt.show()



def plot_lower_region_count(dmodel, profile, direction):

  count = len(dmodel.time_windows)
  
  # lowerBound 
  xLowerB = []
  yLowerB = []
  for i in range(count):
    xLowerB.append(i)
    yLowerB.append(profile.lower_region_lower_bound)
  
  plt.plot(xLowerB, yLowerB, label = "profile lower bound")

  # upperBound 
  xUpperB = []
  yUpperB = []
  for i in range(count):
    xUpperB.append(i)
    yUpperB.append(profile.lower_region_upper_bound)
  
  plt.plot(xUpperB, yUpperB, label = "profile upper bound")

  # data
  xData = []
  yData = []
  for i in range(count):
    xData.append(i)
    yData.append(dmodel.time_windows[i].lower_region_count)

  plt.plot(xData, yData, label = "packets count in time window")
  
  # naming the x axis
  plt.xlabel('time windows')
  # naming the y axis
  plt.ylabel('packets count')
  # giving a title to my graph
  plt.title('Lower region packets count in time windows MODEL:'+ direction)
  # show a legend on the plot
  plt.legend()
  # function to show the plot
  plt.show()


def plot_upper_region_count(dmodel, profile, direction):

  count = len(dmodel.time_windows)
  
  # lowerBound 
  xLowerB = []
  yLowerB = []
  for i in range(count):
    xLowerB.append(i)
    yLowerB.append(profile.upper_region_lower_bound)
  
  plt.plot(xLowerB, yLowerB, label = "profile lower bound")

  # upperBound 
  xUpperB = []
  yUpperB = []
  for i in range(count):
    xUpperB.append(i)
    yUpperB.append(profile.upper_region_upper_bound)
  
  plt.plot(xUpperB, yUpperB, label = "profile upper bound")

  # data
  xData = []
  yData = []
  for i in range(count):
    xData.append(i)
    yData.append(dmodel.time_windows[i].upper_region_count)

  plt.plot(xData, yData, label = "packets count in time window")
  
  # naming the x axis
  plt.xlabel('time windows')
  # naming the y axis
  plt.ylabel('packets count')
  # giving a title to my graph
  plt.title('Upper region packets count in time windows MODEL:'+ direction)
  # show a legend on the plot
  plt.legend()
  # function to show the plot
  plt.show()