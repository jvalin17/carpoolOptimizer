
# coding: utf-8

# In[1]:

import datetime
from collections import OrderedDict
import math
import operator
import copy
import pandas as pd
import os


def preProcessRideData (input_file):
    
    '''Adds data to dataframe using pandas and prepocess file'''
    
    df = pd.read_csv(input_file, sep='\t', skiprows=1, header=None)
    df.columns = ['Requester', 'Trip_#', 'Depart_After', 'Arrive_Before', 'X1', 'Y1', 'X2', 'Y2']
    
    #converts column to date time
    df['Depart_After'] = pd.to_datetime(df['Depart_After'])
    df['Arrive_Before'] = pd.to_datetime(df['Arrive_Before'])
    
    #function to calculate trip distance for each row
    df['trip_dist'] = df.apply (lambda row: (math.sqrt (math.pow((row.X1-row.X2),2) + math.pow((row.Y1-row.Y2),2)))/5.0, axis=1)
    
    #trip time is same as trip distance
    df['trip_time'] = df['trip_dist']
    

    df1 = copy.deepcopy(df)

    #sort values by Depart_After and Arrive_Before 
    df1.sort_values(['Depart_After', 'Arrive_Before'], ascending=[True, True], inplace=True)
    df1['Time_Gap'] = (df1.Arrive_Before - df1.Depart_After).astype('timedelta64[m]')#df1.Timedelta(df1.Arrive_Before - df1.Depart_After).seconds / 60.0
    df1['Extra_time'] = df1['Time_Gap'] - df1['trip_time']
    return df1







class car:
    def __init__ (self, start_x, start_y):
        ''' Initalizes car object wth certain properties'''
        
        #maximum 3 passengers are allowed at a time
        self.limit = 3
        
        #keeps track of number of passengers in car
        self.capacity = 0
        
        #dictionary to hold passenger name and their respective destinations in the order they come
        self.passenger = OrderedDict()
        
        #the time when car is at a particular location
        self.current_location_time = 0
        
        #last passenger dropped time
        self.last_drop_time = 0
        
        #time when car started its journey
        self.earliest_start_time = 0
        
        #passenger start location
        self.passenger_start_location = {}
        
        #keeps track of estimated drop time of each passenger present in car
        self.passenger_drop_time = {}
        
        #keeps track of start time of each passenger present in car
        self.passenger_start_time = {}
        
        #keeps track of extra time each passenger has 
        self.passenger_gap = {}
        
        #keeps track of estimated trip time of each passenger
        self.passenger_trip_rec = {}
        
        #keeps track of arrive before limit of each passenger present in car
        self.passenger_arrive_before = {}
    
        #x co-ordinate of car's location
        self.x_loc = start_x
        
        #y co-ordinate of car's location
        self.y_loc = start_y
        
        #speed of car
        self.speed = 60.0
        
        #overall extra time car has
        self.extratime = 0
        
        
    
    def isAvailable (self):
        '''checks if there is space in car or not'''
        if self.capacity < self.limit:
            return True
        return False
        
    
    def addPassenger (self, passenger_name, passenger_trip_num, arrive_before, pass_loc_x, pass_loc_y, destination_x, destination_y, time_gap, start_time, drop_time):
        '''Adds new passenger in car'''
        
        #creating uniquekey
        passenger_id = passenger_name+str(passenger_trip_num)
        
        #update passenger start location
        self.passenger_start_location[passenger_name] = [pass_loc_x,pass_loc_y]
        
        #update destination
        self.passenger[passenger_name] = [destination_x, destination_y]
        
        #note start time for passenger
        self.passenger_start_time [passenger_name] = start_time
        
        #update trip number
        self.passenger_trip_rec [passenger_name]  = passenger_trip_num
        
        #moving car to new passenger start point
        self.x_loc ,self.y_loc = pass_loc_x, pass_loc_y
        
        #adding new passenger time gap 
        self.passenger_gap [passenger_name] = time_gap
        
        #estimated drop time
        self.passenger_drop_time [passenger_name] = drop_time
        
        #arrive before time
        self.passenger_arrive_before [passenger_name] = arrive_before
        
        #increamenting passenger count in car
        self.capacity += 1 
        
        #update time
        self.current_location_time = start_time
        
        #update last drop time
        self.last_drop_time = drop_time
        
        #update last location
        self.last_location = [destination_x, destination_y]
        
        if len(self.passenger_start_time) > 0:
            self.earliest_start_time = min(self.passenger_start_time.items(), key=lambda x: x[1])[1]
        else:
            self.earliest_start_time = start_time
        
    
    def dropPassenger (self, passenger_name):
        '''drops a paasenger in car'''
        
        #updates location of car before dropping passenger
        self.x_loc , self.y_loc = self.passenger[passenger_name]
        
        #self.last_drop_time = self.passenger_drop_time[passenger_name]
        self.current_location_time = self.passenger_drop_time[passenger_name]
        
        #removes passenger from all records
        del self.passenger_drop_time[passenger_name]
        del self.passenger_start_time[passenger_name]
        del self.passenger_gap[passenger_name]
        del self.passenger[passenger_name]
        del self.passenger_trip_rec [passenger_name]
        
        #updates earliest start time of car
        if len(self.passenger_start_time) > 0:
            self.earliest_start_time = min(self.passenger_start_time.items(), key=lambda x: x[1]) 
        
        #reduce the count of people present in car
        self.capacity -= 1
        
        
        #if we are dropping last person in car, it updates the current location time of car
        if self.capacity == 0:
            self.earliest_start_time = self.current_location_time
            
            
    
    def calDistance (self, dest_x, dest_y):
        '''calculates distance from current location of car to destination'''
    
        dist = (math.sqrt((self.x_loc - dest_x)**2 + (self.y_loc - dest_y)**2))/5.0
        return dist

    
    def calTime (self, dest_x, dest_y):
        '''calculates time from current location of car to destination'''
        dist_to_destination = self.calDistance (dest_x, dest_y)
        time_to_destination = dist_to_destination
        return time_to_destination
    
    
    def calPickUpTime (self, dist):
        '''calculates pick up time of new passenger'''
        time_to_pickup = dist
        return time_to_pickup
 
    
    def print_status (self):
        '''used for printing car status'''
        
        print "Car ID %s" % id(self)
        
        print "Capacity: %s " % self.capacity 
        print "PAssenger Status: " 
        print self.passenger
        
        print "Current Location Time: %s " % self.current_location_time
        print "Last Drop Time: %s " % self.last_drop_time
        print "Last Location: %s " % self.last_location
        
        print "Earliest Start Time: %s " % self.earliest_start_time
        print "Drop Time %s: " % self.passenger_drop_time 
        print "PAssengers Start time: "
        print self.passenger_start_time
        
        print "PAssengers Gap time: "
        print self.passenger_gap
        
        print "PAssengers Trip time: "
        print self.passenger_trip_rec
        
        print "PAssengers Arrive Before time: "
        print self.passenger_arrive_before
    
        print "Current Location X: %s" %self.x_loc
        print "Current Location Y: %s" %self.y_loc
        print "Current Car Speed: %s" %self.speed
        print "Car Extra Time: %s \n" %self.extratime
        



def calDistanceTime (curr_x, curr_y, dest_x, dest_y):
    '''calculates time taken from one point to another'''
    dist = (math.sqrt((curr_x - dest_x)**2 + (curr_y - dest_y)**2))/5.0
    time_to_destination = (dist)
    
    return time_to_destination


def getNearestAvailableCar (requester, location_x, location_y, destination_x, destination_y, time_gap, drop_before_time, active_cars, req_start_time):
    
    '''greedy search for nearest car available that fulfils all requirements of passengers'''
    
    #stop flag to stop search
    stop_flag = 0
    
    #initialize nearest car distance = infinite
    nearest_car_distance = float('inf')
    
    #no nearest car present
    nearest_car = 0
    
    #values for nearest car, distance from nearest car, start time of journey and travel time
    nearest_car, nearest_car_distance, start_time, time_to_dest = 0, float('inf'), 0, 0
    
    
    #check distance from all for active cars 
    for cars in active_cars:
        
        #distance 
        distance_from_car = cars.calDistance (location_x,location_y)
        
        #time to reach requester in minutes
        pick_up_time = cars.calTime(location_x,location_y)
        
        #if pick up passenger time is less than extra time that passenger has
        if pick_up_time < time_gap:
            
            
            #check if car has space
            if cars.isAvailable() :
                
                
                #difference of time in earliest start time
                #start_time_diff = (req_start_time - cars.current_location_time).total_seconds() /60.0
                
                
                #assign start point as new passenger location
                curr_x = location_x
                curr_y = location_y
                    
                #start time of requester
                req_trip_start_time = cars.current_location_time + datetime.timedelta(minutes = pick_up_time)
                
                
                #add passenger pick up time to tot time
                tot_time = 0
                
                #record new drop timings
                updated_drop_timings = {}
                
                #current start time
                current_start_time = req_trip_start_time
                
                
                
                
                #for all passengers in cars check if we can fulfil their requirement of reaching time
                for passenger,destination in cars.passenger.items():
                        
                    dest_x = destination[0]
                    dest_y = destination[1]
                        
                    #get time to reach destination
                    current_loc_to_dest_time = calDistanceTime (curr_x,curr_y,dest_x,dest_y)
                    
                    #estimated drop time if we pick up new passenger
                    estimated_drop_time = current_start_time + datetime.timedelta(minutes = current_loc_to_dest_time)

                    #id estimated time is less than arrive before time of a particular passenger already in car
                    if estimated_drop_time <= cars.passenger_arrive_before[passenger]:
                        
                        #update drop times of all passengers in cars
                        updated_drop_timings[passenger] = estimated_drop_time 
                        
                        #shifting time for next destination
                        current_start_time = estimated_drop_time
                        
                        #updating location for next destination
                        curr_x = dest_x
                        curr_y = dest_y
                        
                            
                    else:
                        #stop and return
                        stop_flag = 1
                        break
                
                    
                if stop_flag != 1:
                        
                        
                        
                    #calculate time taken for added passenger to reach new passenger's destination
                    last_dest_x = destination_x
                    last_dest_y = destination_y
                    
                    drop_time_of_new_passenger = current_start_time + datetime.timedelta(minutes = calDistanceTime (curr_x, curr_y, last_dest_x, last_dest_y))
                    
                    
                    #updating earliest start time 
                    cars.last_drop_time = drop_time_of_new_passenger 
                    
                    if drop_time_of_new_passenger < drop_before_time:
                        
                        if distance_from_car < nearest_car_distance:
                            
                            nearest_car = cars
                            nearest_car_distance = distance_from_car
                            
                            #update drop time of all passengers
                            for k,v in nearest_car.passenger_drop_time.items():
                        
                                nearest_car.passenger_drop_time [k] = updated_drop_timings[k]
                                
                            
                            #start time
                            start_time = req_trip_start_time
                            
                            #drop time
                            time_to_dest = drop_time_of_new_passenger 
                            
                            #update to new last drop time
                            nearest_car.last_drop_time = drop_time_of_new_passenger 
    
    #return nearest car 
    return nearest_car, nearest_car_distance, start_time, time_to_dest
    

def addReccord (car_object, passenger):
    '''adds results to dictionary'''
    
    if id(car_object) not in cars_schedule:
        cars_schedule[id(cars)] = []
                
    
    cars_schedule[id(cars)].append([passenger, cars.passenger_trip_rec[passenger],cars.passenger_start_time[passenger], cars.passenger_drop_time[passenger],cars.passenger_start_location[passenger],cars.passenger[passenger]])
                    

        
        
def printResults ():
    '''Formating results '''
    
    from datetime import datetime

    lst = []


    for k,v in cars_schedule.items():
        for i in v:
            
            start_data = [k,i[0],i[1],i[2].time(),'Start',i[4]]
            drop_data =[k,i[0],i[1],i[3].time(),'Drop',i[5]]
        
            
            lst.append(start_data)
            lst.append(drop_data)
        
        


    cols = ['Car_Id','Passenger_Name','Trip_Num','Time_','Action','Location']
    df4 = pd.DataFrame(lst, columns=cols)
    df4.sort_values(['Time_'] ,ascending=[True], inplace=True)
    
    
    cars_itenary = {}
    
    for index, row in df4.iterrows():
        
        #car identifier
        car_id = row['Car_Id']
        
        if row['Action'] == 'Start':
            
            result_format = "Picked Up %s for Trip %s from %s at %s" % (row['Passenger_Name'],row['Trip_Num'], row['Location'],row['Time_'])
        
        elif row['Action'] == 'Drop':
            
            result_format = "Dropped %s for Trip %s from %s at %s" % (row['Passenger_Name'],row['Trip_Num'] ,row['Location'],row['Time_'])
            
        if car_id not in cars_itenary:
            cars_itenary[car_id] =[]
            
        cars_itenary[car_id].append(result_format)
        
    for k,v in cars_itenary.items():
        print "Car Id - %s Schedule: \n" % (k)
        
        for items in v:
            print items
        
        print '\n'
        

if __name__ == '__main__': 
    
    #schedules of cars  
    cars_schedule = {}
    
    #list of all active cars
    active_cars = []


    #change filename for a different filename
    filename = 'Rides.txt'
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    filepath = dir_path + '/' + filename

    processed_data = preProcessRideData(filepath)

    #iterates over all rows of processed data
    for index, row in processed_data.iterrows():
    
        #current start location
        curr_loc_x, curr_loc_y = row['X1'], row['Y1']
    
        #current end location
        dest_loc_x, dest_loc_y = row['X2'], row['Y2']
    
        #requester
        requester = row['Requester']
    
        #flag to know if passenger is picked up or not
        picked_up = 0
    
        #checks all active cars, updates their timings and assigns new passengers
        if len(active_cars) > 0:
        
        
            for cars in active_cars:
            
                #if the last drop time is running behnd depart after
                if cars.last_drop_time < row['Depart_After']:
                
                
                    #drop all passengers
                    all_passengers = cars.passenger.keys()
                
                    #checks time from current location of car to next passenger that is 
                    for passenger in all_passengers:
                    
                        #adds record in cars schedule
                        addReccord (cars, passenger)
                    
                        #drops each passenger
                        cars.dropPassenger(passenger)
                   
                
                    #calculates time taken to reach next passenger 
                    time_to_next_passenger = cars.calTime(curr_loc_x, curr_loc_y)
                
                
                    #time difference in cars time and current passenger
                    time_diff = row['Depart_After'] - cars.current_location_time 
                    timeDiff = time_diff.total_seconds() / 60
                
                    #if time to reach next passenger is less than the time difference between car and passenger's real time
                    #it picks up that passenger 
                    if time_to_next_passenger < timeDiff:
                    
                        picked_up = 1
                    
                        nearest_car = cars
                    
                        dist = cars.calDistance(curr_loc_x, curr_loc_y)
                        start_time = row['Depart_After']
                        drop_time = row['Depart_After'] + datetime.timedelta(minutes = row['trip_time'])
                            
                        nearest_car.addPassenger (requester, row['Trip_#'], row['Arrive_Before'] ,curr_loc_x, curr_loc_y, dest_loc_x, dest_loc_y, row['Time_Gap'],start_time, drop_time)
                        break
        
            #looks for other active cars if passenger is not picked up
            for cars in active_cars:
        
                if not picked_up:
            
                    nearest_car, dist, start_time, drop_time = getNearestAvailableCar (requester, curr_loc_x, curr_loc_y, dest_loc_x, dest_loc_y, row['Time_Gap'], row['Arrive_Before'],active_cars, row['Depart_After']) 
        
        
                    if nearest_car and dist:
                        picked_up = 1
            
                        nearest_car.addPassenger (requester, row['Trip_#'], row['Arrive_Before'] ,curr_loc_x, curr_loc_y, dest_loc_x, dest_loc_y, row['Time_Gap'],start_time, drop_time)
                        break
        
        # if no active car meets requirement of passenger, a new car is assigned
        if not picked_up:
        
            new_car = car(curr_loc_x, curr_loc_y)
        
        
            start_time = row['Depart_After']
        
        
            drop_time = row['Depart_After'] + datetime.timedelta(minutes = row['trip_time'])
        
        
            new_car.addPassenger (requester, row['Trip_#'], row['Arrive_Before'], curr_loc_x, curr_loc_y, dest_loc_x, dest_loc_y, row['Time_Gap'],start_time, drop_time)
            new_car.extratime = row['Extra_time']
            active_cars.append(new_car)
        

    #dropping last group of people in all cars
    for cars in active_cars:
        if cars.capacity > 0:

            all_passengers = cars.passenger.keys()
            for passenger in all_passengers:
                addReccord (cars, passenger)
                cars.dropPassenger(passenger)
    
    #prints schedules
    printResults()


# In[ ]:



