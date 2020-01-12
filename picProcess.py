#coding:utf-8
import sys,os
from PIL import Image,ImageDraw
from PIL import ImageOps,ImageFilter,ImageEnhance
import numpy as np
import warnings
warnings.filterwarnings("ignore")
 
#二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
#该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False
 
    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1
 
    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None
 
# 降噪 
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点 
# G: Integer 图像二值化阀值 
# N: Integer 降噪率 0 <N <8 
# Z: Integer 降噪次数 
# 输出 
#  0：降噪成功 
#  1：降噪失败 
def clearNoise(image,G,N,Z):
    draw = ImageDraw.Draw(image)
 
    for i in range(0,Z):
        for x in range(1,image.size[0] - 1):
            for y in range(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    draw.point((x,y),color)
 
#测试代码

train_porn_num = 7000
test_porn_num = 1000

porn_team = []#读取图片列表中包括子目录的所有图片

def getPornFile(path, type):
    global porn_team
    for root,dirname,filename in os.walk(path):
        if (dirname or filename):
            for i in filename:
                if os.path.splitext(i)[1] == "."+type:
                    porn_team.append(root+"/"+i)
                    
            for i in dirname:
                getPornFile(path+"/"+i, type)


def generateImg():
    
    print("Processing...")
    getPornFile(r'labeled_img','jpg')#获得所有jpg路径
    i = 1 
    j = 1
    '''
    注意这里的图片有可能是灰度GREY 有可能是RGB 一定要在输入的时候保持统一！！！！！
    '''

    for img_path in porn_team:

        
        label_t = img_path.split("/")[-1]
        label = label_t.split(".")[0]
        label = label.lower()
        if (os.path.exists("imgProcessed1/"+label+".jpg")):
            continue
        #img = Image.open(img_path).resize((WIDTH,HEIGHT)) # 用PIL中的Image.open打开图像
        #img_arr = np.array(img) # 转化成numpy数组

        #降噪
        img_arr = main(img_path)

        label_t = img_path.split("/")[-1]
        label = label_t.split(".")[0]
        label = label.lower()
        print(label)
        img = Image.fromarray(img_arr.astype('uint8'))
        ImageOps.invert(img)
        img.save("imgProcessed2/"+label+".jpg")
        
     

def newCase(path):

    image = Image.open(path)

    om = image.filter(ImageFilter.CONTOUR)

    Image._show(om)

    om = image.filter(ImageFilter.FIND_EDGES)
    Image._show(om)
    om = image.filter(ImageFilter.MedianFilter)
    Image._show(om)

    img_arr = np.array(image)

    img_arr = img_arr[:,:,0]-img_arr[:,:,1]

    count=np.zeros((60,180),dtype=int)

    for i in range(60):
        for j in range (180):
            if img_arr[i][j]<30 or img_arr[i][j]>200:
                img_arr[i][j]=255

def main(path):
    import warnings

    warnings.filterwarnings("ignore")

    #打开图片
    image = Image.open(path)
    iamge = image.filter(ImageFilter.MedianFilter)
    #将图片转换成灰度图片
    #image = image.convert("L")
    
    img_arr = np.array(image)

    img_arr = img_arr[:,:,0]-img_arr[:,:,1]

    count=np.zeros((60,180),dtype=int)

    for i in range(60):
        for j in range (180):
            if img_arr[i][j]<30 or img_arr[i][j]>200:
                img_arr[i][j]=255
    '''
            elif(i>=1 and i<59) and (j>=1 and j<179):
                count[i][j]+=1
                count[i-1][j]+=1
                count[i][j-1]+=1
                count[i-1][j-1]+=1
                count[i+1][j]+=1
                count[i][j+1]+=1
                count[i+1][j+1]+=1
                count[i-1][j+1]+=1
                count[i+1][j-1]+=1
   
    #降噪完成

    for i in range(60):
        for j in range (180):
            if (count[i][j]>=7):
                img_arr[i][j] = 0
            else :
                img_arr[i][j] = 255
    '''

    return img_arr
  
 
if __name__ == '__main__':
    generateImg()
    #path = input("in path:")
    #newCase(path)