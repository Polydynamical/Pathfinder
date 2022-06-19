import requests
import tqdm
import sys
import os

# failed = open("failed2.txt", "a")

image_links = open("unique_image_links.txt").readlines()

notinlist = os.listdir("Images/")

for i in tqdm.tqdm(range(0, 257402, 2)):

    if f"{format(i//2, '06')}_0.png" not in notinlist:
        try:
            response = requests.get(image_links[i], timeout=10)
            open(f"Images/{format(i//2, '06')}_0.png", "wb").write(response.content)
        except:
            pass
#            failed.write(f"0: {i} - {link}\n")
#            failed.flush()
    else:
        pass

    if f"{format(i//2, '06')}_1.png" not in notinlist:
        try:
            response2 = requests.get(image_links[i + 1], timeout=10)
            open(f"Images/{format(i//2, '06')}_1.png", "wb").write(response2.content)
        except:
            pass
#            failed.write(f"1: {i//2 + 1} - {image_links[i//2 + 1]}\n")
#            failed.flush()
    else:
        pass

