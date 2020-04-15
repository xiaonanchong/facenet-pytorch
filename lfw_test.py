# test facenet(pytorch) with LFW recommended test pairs
# need meta file --- pairsDevTest.txt
# LFW data source: http://vis-www.cs.umass.edu/lfw/#views

import argparse
import os

pair_file = '/home/ubuntu/data/pairsDevTest.txt'
data_folder = '/home/ubuntu/data/5749_lfw/'

cutting_edge = 1.05687

import torchvision
from PIL import Image 

from models.mtcnn import MTCNN
from models.inception_resnet_v1 import InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os

workers = 3
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20,
thresholds=[0.6,0.7,0.7], factor=0.709, post_process=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)


def embedding(img_path):
  x = Image.open(img_path)
  x_aligned, prob = mtcnn(x, return_prob=True)
  e = resnet(torch.stack([x_aligned]).to(device)).detach().cpu()
  return e

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

tp = 0
tn = 0
fp = 0
fn = 0
total = 0.0
positive = 0
negative = 0
d = []
max_in_pos=0.0
min_in_neg=1.0

with open (pair_file, 'rt') as file:
  for line in file:
    total += 1

    if RepresentsInt(line):
      print('start testing on', int(line), 'random pairs')
      

    else:
      e = line[:-1].split('	')
      p1 = data_folder + e[0] + os.sep + e[0] + '_' + e[1].zfill(4) + '.jpg'

      if len(e)<4:
        positive += 1
        p2 = data_folder + e[0] + os.sep+ e[0] + '_' + e[2].zfill(4) + '.jpg'
        tag = True
      else:
        negative += 1
        p2 = data_folder + e[2] + os.sep+ e[2] + '_' + e[3].zfill(4) + '.jpg'
        tag = False

      feature1 = embedding(p1)
      feature2 = embedding(p2)

      dist = (feature1-feature2).norm().item()
      print(dist)
      d.append(dist)

      if tag:
        max_in_pos=max(dist, max_in_pos)
        if dist<cutting_edge: tp+=1
        else: fn+=1
      else:
        min_in_neg=min(dist, min_in_neg)
        if dist<cutting_edge: fp+=1
        else: tn+=1

print(positive, 'positive pairs ---', negative, 'negative pairs')
print('max distance in positive pairs:', max_in_pos)
print('min distance in negative pairs:', min_in_neg)

for i in [['tp',tp], ['tn',tn], ['fp',fp], ['fn',fn]]:
  print(i[0], ':', i[1], 'rate:', float(i[1])/float(positive))


with open('distfile.txt', 'w') as filehandle:
    for listitem in d:
        filehandle.write('%s\n' % listitem)
print('complete testing and write distances to : distfile.txt')
      



