# vrp
vehicle routing problem

### strategy
Be greedy!  
A driver starting at the depot will drive to the nearest unclaimed load. They will drive the load to the endpoint.  
Upon reaching the load's endpoint, the driver will scout the nearest unclaimed load's starting point.  
If the driver can handle that load and make it back to the depot while staying within the 12 hour max drive time, it will accept the load. Otherwise, they will drive back to the depot.  
And so on and so forth.  

Why use this strategy?  
Greedy algorithms usually work reasonably well (e.g. Dijkstra's).  So using a greedy nearest neighbors approach seems like a good tradeoff between algorithm complexity and performance.  
Also, the cost function penalizes the number of drivers in a big way (500 multiplier) so it makes sense to maximize the distance each driver drives.

### how to use
This program was built using python 3.12.1 but it should work with any recent version of python3.  
`python3 vrp_runner.py "input_file.txt"`
