from models.mtcnn import MTCNN
from models.inception_resnet_v1 import InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os

workers = 7

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('device:', device)

mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20,
thresholds=[0.6,0.7,0.7], factor=0.709, post_process=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)


def collate_fn(x):
  return x[0]

image_bank = datasets.ImageFolder('/home/ubuntu/data/500_casia_face_v5')
image_bank.idx_to_class = {i:c for c,i in image_bank.class_to_idx.items()}
loader = DataLoader(image_bank, collate_fn=collate_fn, num_workers=workers)

aligned = []
names = []
for x,y in loader:
  x_aligned, prob = mtcnn(x, return_prob=True) #x_aligned:tenser[3,160,160]
  print(y, image_bank.idx_to_class[y], prob)
  aligned.append(x_aligned)
  names.append(image_bank.idx_to_class[y])

aligned = torch.stack(aligned).to(device)
embeddings = resnet(aligned).detach().cpu()#tensor[_,512]

print(embeddings)




                              


