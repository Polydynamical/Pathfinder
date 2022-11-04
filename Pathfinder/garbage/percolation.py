
#    point_to_start = distance(tuple_to_str(cluster_avg[i]), start)



    # midpoint_to_point = distance(endpoints_midpoint, tuple_to_str(cluster_avg[i]))


#    if distance(tuple_to_str(cluster_avg[i]), endpoints_midpoint) + distance(tuple_to_str(cluster_avg[i]), start) <= total_distance / 2:


#    theta = acos(( cos(point_to_start) - cos(start_to_midpoint) * cos(midpoint_to_point) ) / ( sin(start_to_midpoint) * sin(midpoint_to_point) ))
#    radius = (total_distance / 2) * ( 1 - e ** 2 )  /  ( 1 + e * cos(theta) )
 
#     radius = a * b / sqrt( (a * b * cos(theta)) ** 2  + (a * sin(theta)) ** 2)

#    alpha = pi/2 # angle of line with respect to poles
#    theta = lat1 - pi/2
#    center = tuple([3958.8 * x for x in (sin(theta) * cos(lon1), sin(theta) * sin(lon1), cos(theta))])
#    g = sqrt(a ** 2 - b ** 2)
#    f1 = tuple([3958.8 * x for x in (cos(alpha) * sin(g) * cos(lon1) * cos(theta) - sin(alpha) * sin(g) * sin(lon1) + cos(g) * cos(lat1) * sin(theta), cos(alpha) * sin(g) * sin(lon1) * cos(theta) + sin(alpha) * sin(g) * cos(lon1) + cos(g) * sin(lon1) * sin(theta), cos(g) * cos(theta) - cos(alpha) * sin(g) * sin(theta))])
#    f2 = tuple([3958.8 * x for x in (-cos(alpha) * sin(g) * cos(lon1) * cos(theta) + sin(alpha) * sin(g) * sin(lon1) + cos(g) * cos(lat1) * sin(theta), - cos(alpha) * sin(g) * sin(lon1) * cos(theta) - sin(alpha) * sin(g) * cos(lon1) + cos(g) * sin(lon1) * sin(theta), cos(g) * cos(theta) + cos(alpha) * sin(g) * sin(theta))])
#
#    f1_lat = atan2(f1[2], sqrt(f1[0] ** 2 + f1[1] ** 2))
#    f1_lng = atan2(f1[1], f1[0])
#    f2_lat = atan2(f2[2], sqrt(f2[0] ** 2 + f2[1] ** 2))
#    f2_lng = atan2(f2[1], f2[0])
#    print(f1_lat, f1_lng)
#    print(f2_lat, f2_lng)
#    print(center)

