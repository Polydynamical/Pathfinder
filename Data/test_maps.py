locations = open("locations.txt").readlines()
a = ""
b = []

for i in range(0, len(locations), len(locations)//23):
    b.append(locations[i].replace("\n", "").replace("[", "").replace("]", ""))
    a = "/".join(b)

print(a)

