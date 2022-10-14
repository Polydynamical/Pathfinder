locations = open("locations.txt").readlines()

out = []

for i, line in enumerate(locations):
    line = line.split("\n")[0]
    if line == "[":
        out.append("[")
        continue

    if line == "]":
        out.append("]")
        continue

    out.append(line.split()[1] + "," + line.split()[0])


outfile = open("locations2.txt", "a")

for x in out:
    outfile.write(x + "\n")
    
