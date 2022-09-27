import os
import tqdm

image_links = open("unique_image_links.txt").readlines()
counter = 0

filelist = sorted(os.listdir("Images/"))
for i in tqdm.tqdm(range(0, 257402, 2)):
    if str(format((i) // 2, '06')) + "_0.png" == filelist[0]:
        del(filelist[0])
    else:
        print(filelist[0])
        print(str(format((i) // 2, '06')) + "_0.png")

    if str(format((i) // 2, '06')) + "_1.png" == filelist[0]:
        del(filelist[0])
    else:
        print(filelist[0])
        print(str(format((i) // 2, '06')) + "_1.png")
    """
        response = requests.get(image_links[], timeout=10)
        open(f"Images/{format(i//2, '06')}_0.png", "wb").write(response.content)
        """
