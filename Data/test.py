import json

out = open("testest.txt", "a")

gsvjson = json.loads(open("san_mateo_county_GSV.json").read())

for x in gsvjson:
    out.write(f"{x[1]}\n")

