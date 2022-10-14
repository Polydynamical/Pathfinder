# Pathfinder

Created: May 17, 2022 10:29 PM

Status: In Progress

## Goals

- Navigate: Provide people a way to enjoy their routes through customizing their scenery. (point A to point B customization)
- Explore:  Provide people a way to enjoy their city through an automatic route generator. (point A back to point A auto-generated)

<!-- ## Defintions TODO (6/8/2022) -->

## Justification

Taking on a project such as this is relatively nontrivial and requires extensive planning and coordination. The following analysis will attempt to understand the rationale behind this project and similar work that has been done.

### Travel Industry

First and foremost, it is important to note that Pathfinder will primarily **not** target the average person. Most people in their day-to-day lives don't really care about looking at a nice route but rather want to get from point A to point B (i.e. home to work) as fast as possible. Although it is possible some people will use it as a daily app, there is great opportunity in targeting the travel industry.

The travel industry is one of the most important aspects of the US economy. In 2019, international visitors alone spent ~$230 billion and supports 10 million American jobs accounting for 3% of the US GDP. This tells us that there are a lot of people willing to spend money and invest their time in enjoying the United States. More specifically, our goal is to target the epxloration of cities and taking nice scenic routes to destinations. In the United States, approximately 60% of millenials go on road trips and about 45% of American drivers take road trips during the summer.

These statistics clearly demonstrate that there is an market for our app. 

A potential idea is to also expand/merge this project with another company to implement into a navigation app. That way, rather than creating a competing navigation app, we simply add the feature to an already existing app.

### Related Work

There are four major papers that specifically relate to our project. These all are all related to creating the best scenic route. These papers are also listed in chronological order which helps us understand the progression of research.

[Zheng, Y.-T., Yan, S., Zha, Z.-J., Li, Y., Zhou, X., Chua, T.-S., & Jain, R. (2013). GPSView. ACM Transactions on Multimedia Computing, Communications, and Applications, 9(1), 1–18. doi:10.1145/2422956.2422959](https://sci-hub.se/https://doi.org/10.1145/2422956.2422959)
- This paper uses an attention based model based on the number of GPS-tagged photos on the Internet based on the number of photos in each location. In other words, thoey rank the scenic route based on the Points of Interest given by the number of photos taken at the specific location. They scrape these photos from sites such as Flickr. They also specifically account for how visible the "scenic thing" is from your car and take that into account for determining the "scenicness" of the road. An important point that would be incorporated into our project is having a precise defintion of a scenic roadway. This paper defines it as "... a thoroughfare that passes by a series of landscapes and sights and affords vistas of notablke aesthetic, geological, historical, cultural, and touristic qualities alongs it roadside". The defintion is a good start at tackling the problem of creating a scenic route and although does not take into account urban districts, it simplfies the goal. The formula they used for discriminating geospatial distribution is based on a logarithmic scale which allows for a discrete graph. 
- There are several shortcomings of this paper given that it was written in 2013, well before many improvements in machine learning models. Therefore, GPSView is blind to several factors that limit its overall ability. First, scraping photos from online sources fails to factor into relatively unexplored locations. For example, some rural areas in the middle of Missouri might not be places that people take many photos but still contain substantial scenery. Secondly, this paper assumes that photos contain geospecific data in images. Although this was largely available in 2013, now in 2022, most websites strip geospecific data from uploaded images. For example, all images posted on Facebook or sent through Discord automatically remove this type of information to enhance privacy. These privacy concerns limit our ability to accurately represent the number of photos at a specific location. Thirdly, GPSview does not take into account specific aspects of scenery that a user might enjoy. GPSView bases "scenicness" based on how popular locations are rather than specific aspects of the road. For example, if a user wanted to explore residential districts rather than ones in nature, that would be impossible with the methods described in the paper. Finally, GPSview is not available to the public and therefore has no potential benefit to the public.

[Alivand, M., Hochmair, H., & Srinivasan, S. (2015). Analyzing how travelers choose scenic routes using route choice models. Computers, Environment and Urban Systems, 50, 41–52. doi:10.1016/j.compenvurbsys.2014.10.004](https://sci-hub.se/https://doi.org/10.1016/j.compenvurbsys.2014.10.004)
- This paper is certainly a paper worth reading for our project beacuse it analyzes the factors that people consider when deciding the "scenicness" of a route. They hypothesized and tested 3 different models in determing how scenic and they concluded that "an increased presence of water bodies, mountains, forests, and parks along routes increases the probability for a route to be chosen as scenic route, wheras the presence of urban areas along a route decreases that probability." Although this clearly does not take into consideration that some people may consider an urban area as scenic, the metholodiges described in determing such a conclusion can be used in Pathfinder. They did this by mapping out certain characteristics of the roads and comparing them to the number of geo-tagged images at the location. Specifically, they took into account travel time, length of the route, curviness, road time, number of right and left turns, number of road changes, path size, presence of amusement parks, bridges, convention centers, forests, golf courses, mountains, parks, gardens, rocks, sand, skylines, stadiums, water body, etc and related them to the number of photos found on Panoramio, a website with geo-tagged images. However, another aspect that Pathfinder can adapt is generating the specific navigation route. This paper uses a non-parametric Wilcoxon signed rank test for balancing the scenic and fastest route to avoid creating a 3 hour trip for a 15 minute drive. 
- First, it is worth noting that Panoramio is not longer active due to privacy condcerns and was merged into Google Maps/Earth. Although this paper does not specifically work to generate a scenic route, it mainly serves as evaluating which factors influence a classification of such a route. However, it still uses the same idea of comparing the number of geo-tagged images to ranking how scenic a route is. While this is a good model for popularity, our goal with Pathfinder is to allow the user to decide whether they would like to see nature as scenery or other urban and residential districts. Another shortcoming of this project is the entire study was based on routes in California and is not a general approach. With machine learning, Pathfinder aims to generalize the concept of scenicness regardless of images found online. As mentioned before, some places do not contain images uploaded online but would still be considered scenic based on the criteria listed in this paper. Similar to GPSView, this paper lists no publicly available implementation of ranking the scenicness of a route.

[Runge, N., Samsonov, P., Degraen, D., & Schöning, J. (2016). No more Autobahn! Proceedings of the 21st International Conference on Intelligent User Interfaces - IUI  ’16. doi:10.1145/2856767.2856804](https://sci-hub.se/https://doi.org/10.1145/2856767.2856804)
-  First and foremost, this project, titled "Autobahn", improves upon the previous two papers by eliminating volunteered geographic information (VGI) or images with geo-tagging. The authors of the paper recognize unequal distributions of images and tourist attraction bias. In other words, given the large amount of images at a certain location, it propmts more people to visit those locations leading to a nonuniform distrubution of images compared to its "scenicness". Rather, this paper takes a direct approach from scraping Google Street View images and classifying them with deep learning. With this classification, it decides the "scenicness" of a route in an algorithm to create a final navigation route. In this final algorithm, it takes into consideration the region of interest (ROI) and sets a maximum time limit for the route. With these factors, Autobahn uses the Graph/opper API for navigation in the United States and the OpenRouteService API for Europe. Notably, they claim to provide a demonstration of the system at the [Autobahn Project Website](http://autobahn.edm.uhasselt.be/) however the website fails to provide a valid connection. Even the link in the [WIRED article about the Autobahn project](https://www.wired.co.uk/article/scenic-sat-nav-autobahn-research) fails to load a valid page. Even the snapshots from the Wayback machine fail to properly load the page. This gives us a hint that this project was relatively exciting in the beginning but ultimately failed.
- This project is the most similar to the goals and general idea of Pathfinder in the sense that it classifies images agnostic of location and uses it to evaluate the best route given the conditions. It is able to identify "5 high-level scenic categories, namely sightseeing (e.g. viaduct, temple, amusement park), nature and woods (e.g. valley, alley, garden), fields (e.g. wheat field, corn field), water (e.g. ocean, harbor, coast) and mountain (e.g. butte, snowy mountain, volcano). The sixth category contained all non-scenic tags (e.g. street, industry and building)." Notice the last phrase when it labels street, industry, and building as non-scenic. Our goal with Pathfinder is to create a more generalized approach to scenic routes by allowing the user to specify the type of scenery. In addition to the categories of nature that Autobahn includes, we aim to allow for the user to explore residential and urban areas. Another shortcoming is the classification of the Google Street View images. Even though the model was pretrained on the notorious ImageNet dataset with one of the most popular mahcine learning models, Caffee Deep Learning Framework, there have been many advances in machine learning in the past 6 years in convolutional neural networks. The accuracy for the pretrained model was approximately 50%, which is quite good but still lacks major improvements. Another shortcoming includes the classification of the scenicness of an area into 1 km segments. The model takes identifies the most prevalent class in these segments and corresponds to about 3200 feet. Now, although this is generally not a bad idea, it lacks some detail. For a better mapping of the scenery of an area, it would be necessary to shrink the size for more specific scenery. For example, residential districts turn into business districts and vice versa quite quickly and the lack of detail would diminish the quality of the route. Finally, the classification of the Autobahn project coresponds to only about 7.5% the size of California. Pathfinder should aim to include more area eventually. The initial goal will start small but the speed of the model should be extensible to much larger regions.

[Gavalas, D., Kasapakis, V., Konstantopoulos, C., Pantziou, G., & Vathis, N. (2016). Scenic route planning for tourists. Personal and Ubiquitous Computing, 21(1), 137–155. doi:10.1007/s00779-016-0971-3 ](https://sci-hub.se/https://doi.org/10.1007/s00779-016-0971-3)


### Similar Apps

There are a couple of apps in the App Store which have some similarity to the goals of Pathfinder. For understanding the exact number of downloads per day of each app, the paper [Garg, Rajiv and Telang, Rahul, Inferring App Demand from Publicly Available Data (May 2, 2012). MIS Quarterly, Forthcoming, Available at SSRN: https://ssrn.com/abstract=1924044 or http://dx.doi.org/10.2139/ssrn.1924044](https://deliverypdf.ssrn.com/delivery.php?ID=275072007020105075125030081127122018035086055082012031067096022088069002113025010127101122106111029121027004092093026123100118109039073020059068111075107080001064026081012027015091097087022085093024065064116080025085089121113084008118120072113002081&EXT=pdf&INDEX=TRUE) list a general formula as $78423 \cdot (\text{rank})^{-0.944}$.

- **Roadtrippers**: Using the above formula, we can reasonably assume that over the past 4 years, the app has received approximately 2 million downloads. This is largely consistent with the self-proclaimed 25 million trips covering 17 billion miles. Now, this app is essentially the "Explore" feature of Pathfinder in that it lists out the various scenic areas in a city and after the user chooses their locations, will provide a navigation route through them. For example, if I wanted to drive from San Carlos to San Jose, I would be given a list of various attractions such as Great America, Palo Alto Junior Museum, Discovery Museum, Levi's Stadium, Stafford Park, Alice's Restaurant, San Pedro Square Market, San Jose Museum of Quilts and Textiles, etc, and I would choose which I find interesting. Then it would create a route from point A to point B including those attractions. At its essence, this app takes away the pain of finding tourist attractions and simply lists them out for you. Then it adopts a navigation route similar to Google Maps and includes the attractions as stops. This is fairly straightforward to implement: find the attractions and use the Google Maps API to include them as stops. However, this app fails to automatically generate a route based on preferences. The user must discern from thousands of different attractions and at times can be overwhelming. Furthermore, some of the attractions are not really considered attractions. For example, "Levi's Stadium" is an option but it has no real value if there are no players on the field. Finally, this app does not take into consideration the visual appearance of the routes taken and solely focuses on the destinations and sights to see. In other words, this app is more a guide to curate a travel itinerary rather than including the experience of driving as well. Pathfinder can improve upon this to implement a visual approach to navigation.

- **Scenic Motorcycle Navigation**: Using the above formula, we can reasonably infer the app has received approximnately 900K downloads in the past 4 years. This app is closer the goals of creating an app that has visual appeal to the driver. Based on geographic maps, this app is able to decide the "windiness" of a route and provides a navigation system for motorcyclists. This provides a route that is somewhat scenic as winding roads tend to be accompanied with forests and nature. However, this app falls short in that it only factors the windiness of the app rather than specific visual features of the road. For example, Pathfinder aims to appeal to those wanting to see the local community by driving through residential districts. In addition, this app creates routes based on users' experiences and their opinion of a scenic route. According to their app description, "Scenic has a vast database of thousands of beautiful routes, shared and rated by local Scenic users worldwide. Select an area, tap 'Search' and see what comes up.' Similar to the VGI problems that Runge et al outlines, this app bases its routes on subjective public opinion rather than objective analysis. This app also lacks the features from Roadtrippers that would be useful in discerning a potential scenic route.


<!-- ### Conclusion -->

## General Approach

- Create an app with two features: Explore and Navigate.
    - **Explore:** Get a tour of the city of elsewhere. Start and end destination is your current location so it’s basically an auto-guided tour.
    	- Input: latitute, longitude, time constraint.
	- Output: One single path between nodes (road intersections).
    - **Navigate:** Get from point A to point B along a route customized to your preferneces. You can choose to see a residential district, nature, etc.
    	- Input: latitude, longitude, time constraint, end latitude, end longitude, type of scenery (nature, residential, etc (still need to finalize this))
	- Output: One single path between nodes (road intersections).
        
### 3 Major Steps

1. **Create an algorithm for ranking/enumerating scenic locations (museums, forests, state parks etc)**
	1. Find a data source with all such scenic locations.
	2. Label these data points on our node/edge file.
2. **Create an algorithm for ranking the scenicness feature in our desired locations.** (done)
	1. Identify the presence of trees, lakes, etc (done).
		- Can be done with a model trained on ImageNet with Google Street View images, like Autobahn does in Runge et al.
		- We would need to identify trees, plants, bodies of water, gardens, fields, mountains, etc.
		- Then we would take panoramic images from Google Street View and label them with our machine learning model.
		- This geospatial map (maybe in geojson format?) would include weights between road interesections.
		- We can use [this](https://docs.fast.ai/examples/camvid.html) example pretrained model which has been used in [this](https://doi.org/10.1109/ACCESS.2020.3006493) paper.
		- 10/13/22: After further work, I decided to use Facebook's upernet convnext model pretrained on the bdd100k dataset and made ~250K inferences in Google Colab.
	2. Identify the type of surrounding buildings. (TODO)
		- Data can be scraped and mapped from zoning districts (by hand or algorithmically)
	3. Label our data. (done)
		- Add the percentage of each feature to each edge (road) in our data. We would basically expand our .csv file to include extra data for each edge.
3. **Create a working navigation system.** (done)
    1. Get a network of roads in the respective area from US government TIGER files for each county. (done)
    2. Create a shortest/fastest route method with a simple A\* algorithm. (done)
    3. For Explore, use the A\* algorithm to find the shortest route between the "checkpoints" throughout the route. (done)
		- This could also be done with the GraphHopper API or Google Street View (GSV) API.
    4. For Navigate, use the weights and ranking of the scenicness and factor that into the weights of the edges between nodes in the algorithm. Essentially, we would be using the scenicness value to subtract from the total $f$-value of the node.
    	- This will require extensive tuning to ensure that all the constraints of time are met while providing an optimal scenic route.
	- UPDATE: 10/13/22: The problem with simply using the scenicness as the heuristic is that A* is built around finding the shortest path. I.e. it will start at its current node and just incrementally edge closer to the goal node. 
	- For a scenic pathfinding algorithm, we need an omniscient view of the map to find the optimal path. One idea for this is using Percolation theory. Check out the Pathfinder/Percolation directory (will merge into parent directory if it works. 
	- The basic concept of percolation theory is that if we have a 2-dimensional set of nodes on a graph with randomly generated weights on edges, there exists a maximum critical parameter, p, at which all the nodes would be fully connected. In a scenario with edge values randomly generated between 0 and 1, the p-value is 0.5 This means that if the p-value is exactly 0.5, there will always be a path between two nodes. If the p-value is above 0.5, this is not necessarily true. 
	- The idea is to treat our road graph with scenic edges and find the highest possible critical parameter. this would be achieved by removing all connections with a weight too low and find the best possible connection between scenic paths. 
	- [Here](https://web.mit.edu/ceder/publications/Percolation.pdf) is an excellent introduction to the basics of Percolation theory.
	- Note that this is simply an idea and I plan on exploring other aspects of graph theory and thinking critically (no pun intended) about incorporating interdisplinary methods into optimizing this project.
	  

- Book on navigation algorithms "Route Planning Algorithm for Car Navigation" by Flinsenberg, Ingrid C.M. [https://brainmaster.com/software/pubs/brain/Flinsenberg Route Planning.pdf](https://brainmaster.com/software/pubs/brain/Flinsenberg%20Route%20Planning.pdf)

### Notes
- In the end we might combine the Navigate feature with the Explore one for a more personalized experience; however, that would cause a lot more overhead in terms of effort.
- We are planning on starting with San Mateo County then extending to Bay Area -> California -> United States etc.
- We'll write the initial project in **Python 3.9** given its versatility. After the proof of concept, we can migrate it down to Rust or C++.
- Implementing a system for managing millions of nodes is seriously nontrivial. Thankfully, a team at stanford [has worked on this problem](https://snap.stanford.edu/index.html). They also have a published paper [J. Leskovec, K. Lang, A. Dasgupta, M. Mahoney. Community Structure in Large Networks: Natural Cluster Sizes and the Absence of Large Well-Defined Clusters. Internet Mathematics 6(1) 29--123, 2009.](https://arxiv.org/pdf/0810.1355.pdf).
- SNAP also provides the dataset [California Road Network](https://snap.stanford.edu/data/roadNet-CA.html) (roadNet) which represents the road network in terms of nodes and edges. This is extremely useful in simplying the navigation problem. Furthermore, this dataset has been used in various applications such as [visualizing California's roads](https://studentwork.prattsi.org/infovis/labs/california-road-network/) or 
- Google Maps also uses A\* for their navigation system but they also alter it to account for traffic lights, turns, traffic, etc. If we want to make this an end user product, we would also need to consider these factors since they are crucial in altering the time a route takes.
- To view the road map data for San Mateo County, you can open the .xhtml file in your browser. The .csv contains the raw data which needs to be parsed in our programs. You can also open the .shp file with SolidWorks or FreeCad.


## Questions

- The entire navigation system might end up being quite computationally intensive. How can we can simplify our model and how would we improve performance if we end up deciding to create a public user demonstration? (10/13/22: just be more patient or use Google colab/cloud)
- How do we want to structure this app? (Should we consider other options instead of the Explore/Navigate method?)
- Should we open source this project on Github and would that negatively impact our performance on the App Store?
- <del>Is everyone really committed to this project, or is it "just for college applications"? (This project will fail if it's built on building self-worth).</del> It's just me now :)
- <del>Will this app actually be useful to people?</del> (answered above in [Justification](#Justification))

## If we have time
- Implement the above algorithms into an iOS app.
	- iOS has some of the best potential with Apple's new MapKit API announced at Apple's World Wide Developer Conference 2022 (WWDC 2022)
	- Programming language would be Swift.
