#config_file = 'casia_face_regis_list.txt'
#test_file = 'casia_face_test_list.txt'
config_file = 'ms1m_face_regis_list.txt'
test_file = 'ms1m_face_test_list.txt'

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os


def embedding(file_name):
  import PIL.Image as Image
  from models.mtcnn import MTCNN
  from models.inception_resnet_v1 import InceptionResnetV1
  workers = 10
  #device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
  device = torch.device('cpu')
  mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20,
  thresholds=[0.6,0.7,0.7], factor=0.709, post_process=True, device=device)
  resnet = InceptionResnetV1(pretrained='casia_webface').eval().to(device)

  crop_imgs = []
  labels = []
  with open (file_name, 'rt') as file:
    for line in file:
      l = line.strip('\n').split('	')
      path = l[0]
      labels.append(l[1])
      x = Image.open(path)
      x_aligned, prob = mtcnn(x, return_prob=True)
      crop_imgs.append(x_aligned)

  print('total', len(crop_imgs),'images read!')

  embeddings = []

  if len(crop_imgs)%100==0 and len(crop_imgs)>=100:
    for i in range(len(crop_imgs)//100):  
      em = resnet(torch.stack(crop_imgs[i*100:100*(i+1)]).to(device)).detach().cpu()
      embeddings+=em

  else:
    for i in range(len(crop_imgs)):  
      em = resnet(torch.stack(crop_imgs).to(device)).detach().cpu()
      embeddings+=em

  return embeddings, labels

def identify(e1,l1,e2, cutting_edge):
  #print('length of e1,l1 and e2:',len(e1), len(l1), len(e2))
  y = []
  for f2 in e2:
    dist = 10000
    iden = ''
    for i in range(len(l1)):
      dist_ = (f2-e1[i]).norm().item()
      if dist_ < dist:
        iden = l1[i]
        dist = dist_
    if dist > cutting_edge:
      iden = 'unknown'
      #print('++', dist)
    #else:
      #print('--', dist)
    y.append(iden)
  return y

def accuracy(y,l2):
  print(y) 
  print(l2)
  total = len(y)
  tp, tn, fp, fn = 0,0,0,0
  mismatch = 0
  right = 0
  for i in range(total):
    if y[i]==l2[i]:
      right+=1
      if l2[i] == 'unknown': tn+=1
      else: tp+=1
    else:
      if l2[i] == 'unknown': fp+=1
      elif y[i] == 'unknown': fn+=1
      else: mismatch+=1
  print('tested on total: '+str(total)+' faces')
  print('recognition rate = ', float(right)/total)

  print('true positive rate = ', float(tp)/(total/2))
  print('true negative rate = ', float(tn)/(total/2))
  print('false positive rate = ', float(fp)/(total/2))
  print('false negative rate = ', float(fn)/(total/2))
  return float(right)/total, float(tp)/(total/2), float(tn)/(total/2), float(fp)/(total/2), float(fn)/(total/2), mismatch


def accuracy2(y,l2):
  if len(y) != len(l2):
    print("warning: total number of prediction is different from total number of test cases!")
  total = len(y)
  tp, tn, fp, fn, right, mismatch = 0,0,0,0,0,0
  p,n=0,0
  for i in range(total):
    if l2[i]==y[i]: right+=1
    if l2[i]!='unknown':#正样本
      p+=1
      if y[i]!='unknown': 
        tp+=1
        if y[i]!=l2[i]: mismatch+=1
      else: fn+=1
    else:#负样本
      n+=1
      if y[i]=='unknown': tn+=1
      else: fp+=1
  return total, p, n, right, tp, tn, fp, fn, mismatch
	      
def test(ce):
  e1,l1 = embedding(config_file)
  e2,l2 = embedding(test_file)
  y = identify(e1,l1,e2, ce)
  #a,b,c,d,e,m = accuracy(y,l2)
  total, p, n, right, tp, tn, fp, fn, mismatch = accuracy2(y,l2)
  if p !=(tp+fn):print('warning: p not equql to tp+fn!')
  if n !=(tn+fp):print('warning: n not equal to tn+fp!')
  p=float(p)
  n=float(n)

  if n!=0:
    tnr = tn/n
    fpr = fp/n
  else: tpr, fpr = -1,-1
  tpr = tp/p  
  fnr = fn/p
  
  mr = mismatch/float(tp)
  rr = right/float(total)


  with open("result.txt",'a',encoding = 'utf-8') as f:

    for i in [ce,tpr,tnr,fnr,fpr,mr,rr]:
      i = float('%.2f' %i)
      f.write(str(i)+'	')
    f.write('\n')

#'''
with open("result.txt",'a',encoding = 'utf-8') as f:
  for i in ['ce','tpr','tnr','fnr','fpr', 'mr', 'rr']:
    f.write(i+'	')
  f.write('\n')
  f.write('----------')
  f.write('\n')
for i in range(10):
  test(0.95 + i*0.01)

#'''

