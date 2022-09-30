# Pathfinder

This directory contains the main portion of our code. This will combine the data from the Explore and Navigate directories to find a scenic path.

Generally speaking, we will likely implement an altered A\* algorithm given its versatility to changing based on tuning factors. As a sidenote, Google Maps also uses A\* for their navigation system but they also alter it to account for traffic lights, turns, traffic, etc. If we want to make this an end user product, we would also need to consider these factors since they are crucial in altering the time a route takes.

We should:
- LImit the search space for the algorithm based on heuristics
	- I.e. we calculate the distance to the end of each point in the graph (we could do the same for the search) and we should simply remove points that are outside of a certain user-defined radius. (also maybe convert to time of route based on mileage)
