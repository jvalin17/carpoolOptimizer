# Shared Ride Optimizer

#### Objective is to create a schedule for commercial vehicles to satisfy all of their passengers' trips, using as few vehicles as possible. All trips can be shared rides, that is, multiple trips can be serviced by the same vehicle at the same time. Each vehicle can seat up to three passengers at once. 

### Problem Details  

##### Input is provided in a csv format. 

##### All trips have a specified Depart After and Arrive Before time (inclusive) that indicate the earliest time that the person can leave their origin and the latest time that they can reach their destination, respectively.

##### Origin and destination locations are specified as coordinates on a simple 2-dimensional plane. The X1 and Y1 pair represents origin location, the X2 and Y2 pair represents destination location. Assume that the cars travel in a straight line at constant speed.

### Constraints Example  

##### The depart-after time and arrive-before time specify a window within which the trip can take place. For example, for Homer’s trip #1, if he were picked up at 9:30, then there would still be time to drive to his destination before 11:03. So, someone with a 9:20am depart-after requirement could be picked up before Homer’s 9:00am depart-after requirement. 
