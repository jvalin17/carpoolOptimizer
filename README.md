# Shared Ride Optimizer

#### Objective is to create a schedule for commercial vehicles to satisfy all of their passengers' trips, using as few vehicles as possible. All trips can be shared rides, that is, multiple trips can be serviced by the same vehicle at the same time. Each vehicle can seat up to three passengers at once. 

### Problem Details  

##### Input is provided in a csv format. 

##### All trips have a specified Depart After and Arrive Before time (inclusive) that indicate the earliest time that the person can leave their origin and the latest time that they can reach their destination, respectively.

##### Origin and destination locations are specified as coordinates on a simple 2-dimensional plane. The X1 and Y1 pair represents origin location, the X2 and Y2 pair represents destination location. Assume that the cars travel in a straight line at constant speed.

### Constraints Example  

##### The depart-after time and arrive-before time specify a window within which the trip can take place. For example, for Homer’s trip #1, if he were picked up at 9:30, then there would still be time to drive to his destination before 11:03. So, someone with a 9:20am depart-after requirement could be picked up before Homer’s 9:00am depart-after requirement.   

### Solution  

#### Language: Python 2.7  

#### Algorithm:

###### 1.It follows concept of queue that is FIFO. A passenger that enters car first is dropped first.  
###### 2.Tries to fit more requester in minimum cars mainly based on reusability. Assigns car to incoming requester from previously used cars.  

##### Object:  
###### Class Car (car object with certain properties and Functionalities)  
###### Initialize with starting location  

##### Properties:  
###### Limit – Maximum 3 passengers can be taken at a time  
###### Capacity – Current number of passengers in car  
###### Passenger Destination dictionary – Added Passengers destination is maintained in the order they enter car  
###### Current Location Time – Time where car is currently located  
###### Last Drop Time – drop time of last passenger  
###### Earliest Start Time – start time when picked up first passenger  
###### Passenger Gap time dictionary – How much extra time each passenger has when they are picked up  
###### Passenger Start Location Dictionary – Location from which each passenger is picked up  
###### Passenger Trip Dictionary – Trip time for each passenger  
###### Passenger Arrive before Dictionary – The time before which each passenger should reach is maintained  
###### Car location x –coordinate,  Car location y-coordinate  
###### Car Speed  

#### Functionalities:  
###### isAvailable  -checks if car has space   
###### addPassenger – Adds all details of a passenger  
###### dropPassenger –Updates details of Passenger  
###### calDistance – calculates distance of given location from car  
###### calTime – calculates time to reach given location from car  
###### calPickuptime – calculates pick up time for a passenger  
###### print_status – can be used to get details of car at any location  
	

##### Algorithm Pseudo Code:
read data -> data frame && sort users by ‘Depart After’ and ‘Arrive Before’ 

For each request -> table:

	x,y -> location of ride requester

	If any active cars

If time of car to drop last passenger < current requester time
	Car <- drop all passengers
	Update records
	
	Calculate time (Car <- new Request)
If time to pick up and drop requester < drop time limit for requester
	Assign Car <- Requester
	Picked_up <- True
	
	If not picked_up

Try to find nearest car from all active cars
			If there are passengers in car
It checks if all passengers can reach on time or not by adding Requester

If all passengers can reach on time
	Cars time, location <- Requester Pick Up Time, Location
	Update all passengers drop timings
		Requester is added to car
		Assign Car -> Requester
		Picked_up -> True	
	
	If not picked up
		Assign new car to requester


