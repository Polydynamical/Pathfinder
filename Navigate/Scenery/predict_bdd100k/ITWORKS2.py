import mmcv
import multiprocessing as mult
import torch
from mmseg.apis import inference_segmentor, init_segmentor
from mmcv.parallel import collate
from mmseg.datasets.pipelines import Compose
import tqdm
import os
import numpy as np
import cv2
from datetime import datetime

class LoadImage:
    def __call__(self, results):
        if isinstance(results['img'], str):
            results['filename'] = results['img']
            results['ori_filename'] = results['img']
        else:
            results['filename'] = None
            results['ori_filename'] = None
        img = mmcv.imread(results['img'])
        results['img'] = img
        results['img_shape'] = img.shape
        results['ori_shape'] = img.shape
        return results

config_file = "bdd100k-models/sem_seg/configs/sem_seg/upernet_convnext-t_fp16_512x1024_80k_sem_seg_bdd100k.py"
checkpoint_file = "upernet_convnext-t_fp16_512x1024_80k_sem_seg_bdd100k.pth"
my_palette = {
        0: [128, 64, 128],
        1: [244, 35, 232],
        2: [70, 70, 70],
        3: [102, 102, 156],
        4: [190, 153, 153],
        5: [153, 153, 153],
        6: [250, 170, 30],
        7: [220, 220, 0],
        8: [107, 142, 35],
        9: [152, 251, 152],
        10: [70, 130, 180],
        11: [220, 20, 60],
        12: [255, 0, 0],
        13: [0, 0, 142],
        14: [0, 0, 70],
        15: [0, 60, 100],
        16: [0, 80, 100],
        17: [0, 0, 230],
        18: [119, 11, 32],
    }

filelist = sorted(os.listdir("../../../Data/Images/img/"))
filelist2 = sorted(os.listdir("../../../Data/Images/masks/"))

notinlist = []
for i in range(0, len(filelist)):
    if i % 10000 == 0:
        print(i)
    if filelist[i] not in filelist2:
        notinlist.append(f"../../../Data/Images/img/{filelist[i]}")

# notinlist = ["../../../Data/Images/img/043431_1.png"]

# build the model from a config file and a checkpoint file
device = "cpu"
model = init_segmentor(config_file, checkpoint_file, device=device)
cfg = model.cfg
test_pipeline = [LoadImage()] + cfg.data.test.pipeline[1:]
test_pipeline = Compose(test_pipeline)

# array to append all image data
out = np.empty((512, 512, 3))
result = 0

# notinlist = ["../../../Data/Images/img/043431_1.png"]

def finish(result, out, img):
    for i, x in enumerate(result[0]):
        for j, ele in enumerate(x):
            out[i][j] = my_palette[ele]

    out = np.flip(out, axis=2)
    cv2.imwrite(f"../../../Data/Images/masks/{img.split('img/')[1]}", out)

for img in tqdm.tqdm(notinlist):
    data = []
    img_data = dict(img=img)
    img_data = test_pipeline(img_data)
    data.append(img_data)

    data = collate(data, samples_per_gpu=1)
    data['img_metas'] = [i.data[0] for i in data['img_metas']]

    with torch.no_grad():
        result = model(return_loss=False, rescale=True, **data)

    mult.Process(target=finish, args=(result, out, img,)).start()


"""
    cv2.imwrite(f"../../../Data/Images/masks/{img.split('img/')[1]}", out)
#for myfile in tqdm.tqdm(notinlist):
#out = np.empty((512, 512, 3))

result = inference_segmentor(model, f"{myfile}")


for i, x in enumerate(result[0]):
    for j, ele in enumerate(x):
        out[i][j] = my_palette[ele]

out = np.flip(out, axis=2)
cv2.imwrite(f"./{myfile}", out)

#    end = datetime.now()
#    cv2.imwrite(f"../../../Data/Images/masks/{myfile}", result)

#    model.show_result(f"../../../Data/Images/img/{myfile}", result, my_palette, show=False, out_file=f"../../../Data/Images/masks/{myfile}", opacity=1.0)
"""
