from mmseg.apis import inference_segmentor, init_segmentor
from mmseg.core.evaluation import get_palette
import tqdm
import os

config_file = "../bdd100k-models/sem_seg/configs/sem_seg/upernet_convnext-t_fp16_512x1024_80k_sem_seg_bdd100k.py"
checkpoint_file = "upernet_convnext-t_fp16_512x1024_80k_sem_seg_bdd100k.pth"
my_palette = [                                                                                                                                                                                                              
    [128, 64, 128],
    [244, 35, 232],
    [70, 70, 70],
    [102, 102, 156],
    [190, 153, 153],
    [153, 153, 153],
    [250, 170, 30],
    [220, 220, 0],
    [107, 142, 35],
    [152, 251, 152],
    [70, 130, 180],
    [220, 20, 60],
    [255, 0, 0],
    [0, 0, 142],
    [0, 0, 70],
    [0, 60, 100],
    [0, 80, 100],
    [0, 0, 230],
    [119, 11, 32],
]

# build the model from a config file and a checkpoint file
model = init_segmentor(config_file, checkpoint_file, device='cuda')

filelist = sorted(os.listdir("../../../../Data/Images/img/"))
filelist2 = sorted(os.listdir("../../../../Data/Images/masks/"))

notinlist = []
for i in range(1, len(filelist), 10):
    if i % 10000 == 0:
        print(i)
    if filelist[i] in filelist2:
        continue
    notinlist.append(filelist[i])

for myfile in tqdm.tqdm(notinlist):
    result = inference_segmentor(model, f"../../../../Data/Images/img/{myfile}")

    model.show_result(f"../../../../Data/Images/img/{myfile}", result, my_palette, show=False, out_file=f"../../../../Data/Images/masks/{myfile}", opacity=1.0)
