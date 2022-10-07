# Nodes and stuff

- We should precompute a value for scenicness for each node
	- We should make a directory for things people want.
	- I.e. maximum vegetation implies scenic value is (everything - road - ?sky) - vegetation

User Presets:
- how much vegetation
	eq: scenicness = (everything) - vegetation
- how much residential
	eq: TBD!!
- how much urban city
	eq: TBD!!

Notes:
- We want to minimize the scenicness value to minimize the cost between two nodes.
- For example, if we are trying to find the shortest route between two nodes, we precompute the cost (distance) between two nodes. If the cost is very low (like 0), we will continue exploring from that node. If the cost if very high (like inf), the model will avoid the route and look for better options

- For the user set limit, we must first find the shortest (maybe fastest too) route between two locations and have the user limit be added to the shortest path.
- I.e. if it takes 30 miles to get from A to B and the user doesn't want to exceed 10 miles extra distance, Pathfinder will set the 

TODO:
- decide whether the sky is a consideration in scenicness
- Todo: change path cost based on speed limit and stop signs etc
- Precompute scenicness of all edges (between any two nodes)
	- store all these adjacency lists into a directory adjancecy\_lists/
		+ i.e. 100veg where is only cares about vegetation
		+ i.e. 100resid where it only cares about residential environments
		+ i.e. 80veg20resid where it mostly wants vegetation but also cares about residential areas
	- scenicness factor = (percent 1) * (eq/factor 1) + (percent 2) * (eq/factor 2) + ... + (percent n) * (eq/factor n)
		+ i.e. 100veg = (100%) * (veg eq from above) for all edges -> adjacency\_lists/100veg.txt
		+ i.e. 100resid = (100%) * (resid eq from above) for all edges -> adjacency\_lists/100resid.txt
		+ i.e. 80veg20resid = (80%) * (veg eq from above) + (20%) * (resid eq from above) for all edges -> adjacency\_lists/80veg20resid.txt
