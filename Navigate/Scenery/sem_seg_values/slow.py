import matplotlib.image as img
seg_dict = {}

gsv = img.imread('000000_0.png', format="JPG")
for i in range(512):
    for j in range(512):
        tmp = str(gsv[i][j])
        if tmp in seg_dict.keys():
            seg_dict[tmp] += 1
            pass
        else:
            seg_dict[tmp] = 1

print(dict(sorted(seg_dict.items(), key=lambda item: item[1])))

# print(gsv[511][0])
