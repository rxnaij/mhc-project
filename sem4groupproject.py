"""
3:51 PM What Richard added:
    code to add the GeoJSON layers for bike lanes
"""

## Import packages

import folium
from folium.plugins import MarkerCluster
import pandas as pd
import csv
import matplotlib.pyplot as plt
from collections import Counter

## Functions that collect and list MISCELLANEOUS STATISTICS.

# Returns the top streets where accidents occurred

def worstStreets():
    streets = {}
    file = open("MVC.csv")
    reader = csv.DictReader(file)
    for row in reader:
        on_street = row["ON STREET NAME"]
        streets[on_street] = streets.get(on_street, 0) + 1
    file.close()
    
    worst = sorted(streets, key = streets.__getitem__, reverse=True)
    worstStreetsFile = open('listWorstStreets.txt', "w+")
    for i in range(len(worst)):
        fileStr = str(str(worst[i]) + str(" was the offending vehicle in ") + str(streets[worst[i]]) + str(" accidents.\n"))
        worstStreetsFile.write(fileStr)
        
    worstStreetsFile.close()
    return worst


# Retrives the top factors leading to accidents
#   if vehicle == 1: returns factors for non-bicycle vehicles
#   if vehicle == 2: returns factors for bicyclists

def worstCauses(vehicle):
    if vehicle == 1:
        contribFactor = "CONTRIBUTING FACTOR VEHICLE 1"
    elif vehicle == 2:
        contribFactor = "CONTRIBUTING FACTOR VEHICLE 2"
    causes = {}
    file = open("MVC.csv")
    reader = csv.DictReader(file)
    for row in reader:
        causeType = row[contribFactor]
        causes[causeType] = causes.get(causeType, 0) + 1
    file.close()
    
    worst = sorted(causes, key = causes.__getitem__, reverse=True)
    
    if vehicle==1:
        worstCausesFile = open('listWorstVehicleCauses.txt', "w+")
    elif vehicle==2:
        worstCausesFile = open('listWorstBicycleCauses.txt', 'w+')
        
    if vehicle==1:
        worstCausesFile.write("For non-bicycle vehicles:")
    elif vehicle==2:
        worstCausesFile.write("For bicyclists:")
    for i in range(len(worst)):
        fileStr = str(str(worst[i]) + str(" was the cause for ") + str(causes[worst[i]]) + str(" accidents.\n"))
        worstCausesFile.write(fileStr)
        
    worstCausesFile.close()
    return worst


# Retrives the types of vehicles that collided into bicyclists the most

def worstVehicles():
    vehicles = {}
    file = open("MVC.csv")
    reader = csv.DictReader(file)
    for row in reader:
        vehicleType = row["VEHICLE TYPE CODE 1"]
        vehicles[vehicleType] = vehicles.get(vehicleType, 0) + 1
    file.close()
    
    worst = sorted(vehicles, key = vehicles.__getitem__, reverse=True)
    worstVehiclesFile = open('worstStreets.txt', "w+")
    for i in range(len(worst)):
        fileStr = str(str(worst[i]) + str(" was the offending vehicle in ") + str(vehicles[worst[i]]) + str(" accidents.\n"))
        worstVehiclesFile.write(fileStr)
        
    worstVehiclesFile.close()
    return worst

# Retrives the types of vehicles that collided into bicyclists the most
# Data does not come with a column for SURFACE TYPE.
# DataFrame with SURFACE TYPE column must be provided in parameter.

def worstSurfaces(data):
    surfaces = {}
    for index, row in data.iterrows():
        surfaceType = row["SURFACE TYPE"]
        surfaces[surfaceType] = surfaces.get(surfaceType, 0) + 1
    worst = sorted(surfaces, key = surfaces.__getitem__, reverse=True)
    worstSurfacesFile = open('listWorstSurfaces.txt', "w+")
    for i in range(len(worst)):
        fileStr = str(str(worst[i]) + str(" was the surface on which an accident occurred in ") + str(surfaces[worst[i]]) + str(" accidents.\n"))
        worstSurfacesFile.write(fileStr)
        
    worstSurfacesFile.close()
    return worstSurfaces

## code to show time of accident and frequency.

def timeGraph():
    #Using the dictionary reader to access by column names
    f = open("MVC.csv")
    reader = csv.DictReader(f)
    accidentTime = [row['TIME'] for row in reader]
    f.close()
    print(accidentTime)

    accidentHour = []
    for i in range(0,len(accidentTime)-4):
        accidentHour.append(int(accidentTime[i][:accidentTime[i].find(":")]))
        
    accidentHourCount = Counter(accidentHour)
    hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    counts = []
        
    for i in range(len(hours)):
        counts.append(accidentHourCount[hours[i]])
    
    #Make a plot
    plt.plot(hours,counts,color='r',label="Number of accidents")
    plt.title("Bike Accident Frequency by Time")
    plt.xlabel('Time (In Hours)')
    plt.ylabel('Accident Frequency')
    plt.show()
    #plt.title("NYC Number of Accidents on February 10,2016 by Hour")
    #plt.xlabel("Counts")
    #plt.ylabel("Accidents")
    #plt.legend(loc = 2,fontsize = 'x-small')  #Make a legend in upper left corner


accident = pd.read_csv('MVC.csv')

## code to add bike lane data to the accident dataframe

# Create column in accident DataFrame denoting bike lane type
accident["SURFACE TYPE"] = ''

# Remove extra whitespace from accident location columns
accident['ON STREET NAME'] = accident['ON STREET NAME'].str.strip()
accident['CROSS STREET NAME'] = accident['CROSS STREET NAME'].str.strip()

# Classify groups of streets which are entirely covered in a certain type of lane
protectedLanes = ['1 AVENUE', '2 AVENUE', 'LAFAYETTE STREET']
normalLanes = ['5 AVENUE', 'EAST 1 STREET', 'EAST 2 STREET', 'EAST 9 STREET', 'EAST 10 STREET', '5 AVENUE']

# For each entry, identify an accident location as either located on :
#   a street classified as entirely covered by a bike lane in the lists above OR 
#   a street only partially covered by a bike lane
for index,row in accident.iterrows():
    on_street = row["ON STREET NAME"]
    cross_street = row["CROSS STREET NAME"]
    if (on_street in protectedLanes) or (on_street == 'BROADWAY' and cross_street in ["EAST 17 STREET", "EAST 18 STREET", "EAST 19 STREET", "EAST 20 STREET"]) or (on_street == "EAST 17 STREET" and cross_street in ["BROADWAY","PARK AVENUE SOUTH", "UNION SQUARE EAST"]) or (on_street == "4 AVENUE" and cross_street in ["EAST 9 STREET", "WANAMAKER PLACE", "EAST 10 STREET", "EAST 11 STREET", "EAST 12 STREET"]):
        # Protected lanes
        accident.set_value(index, 'SURFACE TYPE', 'protected')
    elif (on_street in normalLanes) or (on_street == 'EAST 20 STREET' and cross_street not in ['2 AVENUE', '3 AVENUE']):
        # Normal lanes
        accident.set_value(index, 'SURFACE TYPE', 'normal')
    elif (on_street == 'BOWERY' and cross_street in ['EAST 1 STREET', 'EAST 2 STREET']) or (on_street == 'WASHINGTON SQUARE NORTH' and cross_street in ["UNIVERSITY PLACE", "5 AVENUE"]) or (on_street in ['EAST 15 STREET', 'EAST 16 STREET'] and cross_street == "5 AVENUE") or (on_street == "UNION SQUARE EAST" and cross_street in ["EAST 14 STREET", "EAST 15 STREET"]) or (on_street == "EAST 20 STREET" and cross_street in ["3 AVENUE", "2 AVENUE"]):
        # Shared lanes
        accident.set_value(index, 'SURFACE TYPE', 'shared')
    else:
        # Street (no bike lanes)
        accident.set_value(index, 'SURFACE TYPE', 'street')

## code to sort and produce miscellaneous data in text files

timeGraph()
worstVehicles()
worstStreets()
worstCauses(1)
worstCauses(2)
worstSurfaces(accident)

## code to create map

# Create map
mapaccident = folium.Map(location=[40.715441,-73.804684], zoom_start=10) 

coords = []
popups = []
icons = []
for index,row in accident.iterrows():
    lat = row["LATITUDE"]
    long = row["LONGITUDE"]
    name = row["DATE"]
    on_street = row["ON STREET NAME"]
    cross_street = row["CROSS STREET NAME"]
    surface = row['SURFACE TYPE']
    descr = str(name) + '\n' + str(on_street) + ", " + str(cross_street) + '\n' + str(surface)
    coords.append([lat,long])
    popups.append(descr)

mapaccident.add_children(MarkerCluster(locations=coords, popups = popups))

# Add GeoJSON layers of bike lanes
mapaccident.choropleth(geo_path='union_square-map.geojson',
               fill_color='yellow',
               fill_opacity=0.2,
               line_color='black',
               line_weight=1,
               legend_name='Union Square, 10003'
              )
mapaccident.choropleth(geo_path='protected-map.geojson',
               line_color='green',
               line_weight=5,
               legend_name='Protected bike lane'
              )
mapaccident.choropleth(geo_path='normal-map.geojson',
               line_color='cyan',
               line_weight=5,
               legend_name='Normal bike lane'
              )
mapaccident.choropleth(geo_path='shared-map.geojson',
               line_color='magenta',
               line_weight=5,
               legend_name='Shared bike lane'
              )
folium.LayerControl().add_to(mapaccident)

#Save map
mapaccident.save(outfile='bikeaccidentLocations.html')