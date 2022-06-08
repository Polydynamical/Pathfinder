# Pathfinder

This directory contains the main portion of our code. This will combine the data from the Explore and Navigate directories to find a scenic path.

Generally speaking, we will likely implement an altered A\* algorithm given its versatility to changing based on tuning factors. As a sidenote, Google Maps also uses A\* for their navigation system but they also alter it to account for traffic lights, turns, traffic, etc. If we want to make this an end user product, we would also need to consider these factors since they are crucial in altering the time a route takes.
