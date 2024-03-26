import matplotlib.pyplot as plt 
import numpy as np
import geopandas
from shapely.geometry import Point
import seaborn as sb
import math

class Candidate:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.total_votes = 0

    def __str__(self):
        return f'Name: {self.name}\t\tXY: {(self.x,self.y)}\tTotal Votes:{self.total_votes}'
    
    def get_name(self): return self.name    
    
    def get_position(self): return (self.x,self.y)

    def get_votes(self): return self.total_votes

    def increase_votes(self, factor=1): self.total_votes += factor

    def update_position(self, new_position): self.x, self.y = new_position

    def display(self): print(str(self))

    def reset_votes(self): self.total_votes = 0
    
class Voter:
    def __init__(self, id, x, y, preferences):
        self.id = id
        self.x = x
        self.y = y
        self.preferences = preferences
    
    def __str__(self):
        return f'ID: {self.id}\t\tXY: {(self.x,self.y)}\tPreferences:{self.preferences}'
    
    def get_id(self): return self.id

    def get_position(self): return (self.x,self.y)

    def get_preferences(self): return self.preferences

    def update_preferences(self, new_preferences): self.total_votes = new_preferences

    def remove_candidate(self, candidate): 
        if candidate in self.preferences: self.preferences.remove(candidate)

    def update_position(self, new_position): self.x, self.y = new_position

    def display(self): print(str(self))

def read_votes_from_file(filename):
    file = open(filename,"r")
    votes = [x.strip().split(',') for x in file] 
    return votes

def create_candidates(filename):
    zip_dictionary = populate_zipcode_dictionary("datasets/us_zipcodes.csv")
    candidates = []
    with open(filename, "r") as file:
        lines = [x.strip().split(',') for x in file]
        for name,zipcode in lines:
            if zipcode in zip_dictionary:
                x, y = zip_dictionary[zipcode]
                candidates.append(Candidate(name, x, y))
            else: print(f"No coordinates found for zipcode: {zipcode}")
    return candidates

def create_voters(votes):
    voters = []
    index = 0
    for v in votes:
        voters.append(Voter(index, 0,0, v))
        index += 1

    return voters

def sort_candidates(candidates):
    result = []
    for candidate in candidates:
        result.append((candidate.get_name(), candidate.get_votes()))
    return sorted(result, key=lambda x:x[1], reverse=True)

def filter_losers(candidates):
    result = []
    max_score = candidates[0][1]
    for candidate in candidates:
        if candidate[1] == max_score:
            result.append(candidate)
    return result

def remove_candidate(candidates, removed):
    for c in candidates:
        if c.get_name() == removed:
            candidates.remove(c)
    return candidates

def populate_zipcode_dictionary(filename):
    zip_dictionary = {}
    with open(filename, "r") as zipcodes:
        for line in zipcodes:
            zipcode, latitude, longitude = line.strip().split(',')
            zip_dictionary[zipcode] = (float(latitude), float(longitude))
    return zip_dictionary

def populate_population_dictionary(filename):
    pop_dictionary = {}
    with open(filename, "r") as zipcodes:
        for line in zipcodes:
            #print(line)
            #print(line.strip().split(','))
            city, stadium, pop_size, zip = line.strip().split(',')
            pop_dictionary[zip] = int(pop_size)
    return pop_dictionary 

def create_graph(candidates, voters):

    candidates_locations = []
    voter_locations = []
    long =[]
    lat =[]

    # Adding labels for each data point
    for c in candidates:
        name = c.get_name()
        x,y = c.get_position()
        candidates_locations.append([x,y])
        long.append(x)
        lat.append(y)
    
    for v in voters:
        x,y = v.get_position()
        voter_locations.append([x,y])


    us_map = geopandas.read_file('maps/usa-states-census-2014.shp')

    fig,ax = plt.subplots(figsize = (15,15))
    us_map = us_map.to_crs("EPSG:4326")

    us_map.boundary.plot(ax = ax)

    geometry = [Point(xy) for xy in zip(lat,long)]
    geo_df = geopandas.GeoDataFrame(geometry = geometry)
    print(geo_df)
    g = geo_df.plot(ax = ax, markersize = 30, color = 'red', marker='*', label = 'Stadiums')
    
    #voter_locations = np.array([v.get_position() for v in voters])
    print(len(voter_locations))
    #hm = sb.heatmap(data=voter_locations, annot=True)
    for c in candidates:
        name = c.get_name()
        x,y = c.get_position()
        ax.text(y, x, name, fontsize=7, ha='right', va='bottom', fontweight='bold')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Stadium Locations on US Map')
    plt.legend()
    plt.show()

def populate_voters(filename, zip_dictionary, candidates):
    pop_dictionary = populate_population_dictionary(filename)
    voters = []
    #print(pop_dictionary)
    i = 0
    for location in pop_dictionary:
        #print(location)
        zip = location
        for person in range(pop_dictionary[location]):
            if zip in zip_dictionary: 
                x,y = zip_dictionary[zip]
                voters.append(Voter(f"Voter{i}", x, y, populate_preferences(x,y, candidates)))
                i += 1
            else: print(f"No coordinates found for zipcode: {zip}")
    #print(f"HERE: {i}")
    return voters

def populate_preferences(x,y, candidates):
    distances = []
    preferences = []
    for cand in candidates:
        d = euclidean_preference((x,y), (cand.get_position()[0], cand.get_position()[1]))
        distances.append((d, cand.get_name()))
    
    distances.sort(key=lambda a: a[0]) # sorting based on the distance, not candidate name
    for d in distances:
        preferences.append(d[1])

    return preferences

def euclidean_preference(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2

    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

def print_results(results, save_to):
    with open(save_to, 'w'):
        print(results, file=save_to)