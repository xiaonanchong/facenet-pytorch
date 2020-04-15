import random
import os

def vgg_test_list(n):

  path = '/home/ubuntu/data/vggface2/test/'
  c = 0
  t = 0
  with open("ms1m_face_test_list.txt",'w',encoding = 'utf-8') as f:
    for folder in os.listdir(path):
      c+=1
      if c <=n:
        for filename in os.listdir(path+folder)[:1]:
          #print(path+folder+'/'+filename+ '	' +folder)
          f.write(path+folder+'/'+filename+ '	' +folder +'\n')
      elif c<=2*n:
        for filename in os.listdir(path+folder)[:1]:
          #print(path+folder+'/'+filename+ '	' +'unknown')
          f.write(path+folder+'/'+filename+ '	' +'unknown' +'\n')
      else:
        print('read',c-1,'folders to test list!')
        break
    print('warning: not enough faces: only',c,'collected!')


  with open("ms1m_face_regis_list.txt",'w',encoding = 'utf-8') as f:
    for folder in os.listdir(path):
      t+=1
      if t <=n:
        for filename in os.listdir(path+folder)[1:2]:
          #print(path+folder+'/'+filename+ '	' +folder)
          f.write(path+folder+'/'+filename+ '	' +folder +'\n')
      else:
        print('read',t-1, 'folders to regist list!')
        break




def casia_test_list(n):
  path="/home/ubuntu/data/500_casia_face_v5/"
  p1 = "CASIA-FaceV5 (000-099)/"
  p2 = "CASIA-FaceV5 (100-199)/"
  p3 = "CASIA-FaceV5 (200-299)/"
  p4 = "CASIA-FaceV5 (300-399)/"
  p5 = "CASIA-FaceV5 (400-499)/" 
  p = [p1,p2,p3,p4,p5]
  
  with open("casia_face_regis_list.txt",'w',encoding = 'utf-8') as f:
    for i in range(n):
      p_=p[i//100]
      f.write(path+p_+str(i).zfill(3)+"/"+str(i).zfill(3)+"_"+str(0)+".bmp	"+str(i).zfill(3)+"\n")

  with open("casia_face_test_list.txt",'w',encoding = 'utf-8') as f:
    for i in range(n):
      p_=p[i//100]
      f.write(path+p_+str(i).zfill(3)+"/"+str(i).zfill(3)+"_"+str(random.randint(1,4))+".bmp	"+str(i).zfill(3)+"\n")
    for i in range(n):
      i=i%100
      r = random.randint(n//100,4)
      f.write(path+p[r]+str(i+100*r).zfill(3)+"/"+str(i+100*r).zfill(3)+"_"+str(random.randint(1,4))+".bmp	"+"unknown"+"\n")

  print('test list built!')

#casia_test_list(400)
vgg_test_list(100)

'''
with open("casia_face_regis_list.txt",'w',encoding = 'utf-8') as f:
  for i in range(100):
   f.write("/home/anjie/500_casia_face_v5/CASIA-FaceV5 (000-099)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+str(i).zfill(3)+"\n")


with open("casia_face_test_list.txt",'w',encoding = 'utf-8') as f:
  for i in range(50):
    f.write("/home/anjie/500_casia_face_v5/CASIA-FaceV5 (000-099)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_1.bmp	"+str(i).zfill(3)+"\n")
  for i in range(100,150):
    f.write("/home/anjie/500_casia_face_v5/CASIA-FaceV5 (100-199)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+"unknown"+"\n")
'''
	
'''
with open("casia_face_regis_list.txt",'w',encoding = 'utf-8') as f:
  for i in range(100):
   f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (000-099)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+str(i).zfill(3)+"\n")
  for i in range(100,200):
   f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (100-199)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+str(i).zfill(3)+"\n")


with open("casia_face_test_list.txt",'w',encoding = 'utf-8') as f:
  for i in range(50):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (000-099)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_1.bmp	"+str(i).zfill(3)+"\n")
  for i in range(100,150):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (100-199)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_1.bmp	"+str(i).zfill(3)+"\n")

  for i in range(200,300):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (200-299)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+"unknown"+"\n")
'''

'''

with open("casia_face_regis_list.txt",'w',encoding = 'utf-8') as f:
  for i in range(100):
   f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (000-099)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+str(i).zfill(3)+"\n")
  for i in range(100,200):
   f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (100-199)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+str(i).zfill(3)+"\n")
  for i in range(200,300):
   f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (200-299)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+str(i).zfill(3)+"\n")



with open("casia_face_test_list.txt",'w',encoding = 'utf-8') as f:
  for i in range(50):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (000-099)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_1.bmp	"+str(i).zfill(3)+"\n")
  for i in range(100,150):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (100-199)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_1.bmp	"+str(i).zfill(3)+"\n")
  for i in range(200,250):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (200-299)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_1.bmp	"+str(i).zfill(3)+"\n")

  for i in range(300,400):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (300-399)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+"unknown"+"\n")
  for i in range(400,450):
    f.write("/home/ubuntu/500_casia_face_v5/CASIA-FaceV5 (400-499)/"+str(i).zfill(3)+"/"+str(i).zfill(3)+"_0.bmp	"+"unknown"+"\n")
'''
