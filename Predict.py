import warnings

warnings.filterwarnings("ignore")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

from keras import models
from keras import layers
from keras.utils.np_utils import to_categorical
from keras.preprocessing import image#图像z增强
from matplotlib import pyplot as plt
from keras.models import load_model #导入模型
from PIL import Image 
import numpy as np

from PIL import ImageOps,ImageFilter,ImageEnhance
from keras import regularizers
import picProcess


WIDTH = 180
HEIGHT = 60
CHANNEL = 1

dic = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25,'0':26,'1':27,'2':28,'3':29,'4':30,'5':31,'6':32,'7':33,'8':34,'9':35}


def Code(a):
    re_dic = {v: k for k, v in dic.items()}
    KEY = []
    for i in range(0,4):
        maxx = -1000.
        order = 0
        for j in range(0,36):
            if a[i*36+j]>maxx:
                maxx,order = a[i*36+j],j
        KEY.append(re_dic[order])
    return KEY

def fromProcessed(img_path):
    img = Image.open(img_path).resize((WIDTH,HEIGHT))
    img_arr = np.array(img).reshape(HEIGHT,WIDTH,CHANNEL) # 转化成numpy数组
    img_arr = np.expand_dims(img_arr,axis=0)
    img_arr = img_arr.astype('float32') / 255
    return img_arr

def fromOrigin1(img_path):

    #print(img_arr)
    img_arr = picProcess.main(img_path)
    label_t = img_path.split("/")[-1]
    label = label_t.split(".")[0]
    label = label.lower()
    print(label)
    img = Image.fromarray(img_arr.astype('uint8'))
    ImageOps.invert(img)
    img.show()
    img.save(label+".jpg")#特么玄学问题，保存之后再读和保存之前的numpy数组是不一样的....而我用的是打开图片训练的，所以需要保存之后再搞
    img_arr =  fromProcessed(label+".jpg")
    os.remove(label+".jpg")
    return img_arr

def fromOrigin2(img_path):
    
    #print(img_arr)
    img_arr = picProcess.main(img_path)
    label_t = img_path.split("/")[-1]
    label = label_t.split(".")[0]
    label = label.lower()
    print(label)
    img = Image.fromarray(img_arr.astype('uint8'))
    ImageOps.invert(img)
    img = img.filter(ImageFilter.MedianFilter)
    img = img.filter(ImageFilter.CONTOUR)
    img.show()
    img.save(label+".jpg")#特么玄学问题，保存之后再读和保存之前的numpy数组是不一样的....而我用的是打开图片训练的，所以需要保存之后再搞
    img_arr =  fromProcessed(label+".jpg")
    os.remove(label+".jpg")
    return img_arr

def LoadModel(img_path):
    model = load_model('URP.h5')
    img_arr = fromOrigin2(img_path)
    #img_arr = fromProcessed(img_path)
    a=model.predict(img_arr)
    #print(a)
    print("The KEY is: "+str(Code(a[0])))
    
    




while(1): 
    path = input("Input the image path: ")
    LoadModel(path)

