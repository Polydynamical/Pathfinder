import tqdm

geolocations = open("san_mateo_county_geolocations.txt").readlines()
google_links = open("links.txt").readlines()
out = open("out.json", "a")

for i, link in tqdm.tqdm(enumerate(google_links)):
    if r"data=!3m3!1e1!3m1!2e0" in link:
        continue
    elif "data=!3m6!1e1!3m4!1sAF" in link:
        continue
    elif r"data=!3m6!1e1!3m4!1s" in link:
        out.write(f"[\"{geolocations[i].split('cbll=')[1].split(r'&cbp=')[0]}\", \"{link.split(r'data=!3m6!1e1!3m4!1s')[1].split('!')[0]}\"],\n")
    else:
        continue

