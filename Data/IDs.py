import json
import tqdm

outfile = open("unique_image_links.txt", "a")
IDs = json.loads(open("san_mateo_county_GSV.json").read())
out = []

for i, ele in tqdm.tqdm(enumerate(IDs)):
    if i == 0:
        out.append(ele[1])
        continue
    if ele[1] == IDs[i-1][1]:
        continue
    out.append(ele[1])

for j in out:
    outfile.write(f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={j}&x=0&y=0&zoom=1\n")
    outfile.write(f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={j}&x=1&y=0&zoom=1\n")
