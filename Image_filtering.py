from skimage import io, color
import numpy as np
from matplotlib import pyplot as plt
import math
import os
from skimage.transform import resize, rescale
import copy
######Citirea bazei de date si colectarea imaginilor######
curent_dir = os.getcwd() 
img_dir = r"/content/drive/MyDrive/baza_date_paic"

lista_imagini = []

os.chdir(img_dir)

for img in os.listdir(img_dir):
  a = io.imread(img)
  resized = resize(a, (256,256))
  resized = resized*255
  lista_imagini.append(resized)


######Functie pentru adaugarea zgomotului Gaussian######
def addGauss(img, medie = 0, dispersie = 10):
    nr_linii, nr_coloane, nr_canale = img.shape
    zg = np.random.normal(medie, dispersie, [nr_linii,nr_coloane,nr_canale])
    img_zg = img + zg
    img_zg[img_zg > 255] = 255
    img_zg[img_zg < 0] = 0
    return img_zg


###Lista de imagini cu zgomot gaussian cu dispersie 10#####
imagini_zg_g = []
for i in range(len(lista_imagini)-2):
  b = addGauss(lista_imagini[i],dispersie = 10).astype(np.uint8)
  imagini_zg_g.append(b)
  #plt.figure(),plt.imshow(b)


###########Functie pentru adaugarea zgomotului impulsiv#######
def addImpulse(img_orig, ratio = 0.1):
    img = img_orig.copy()
    l, c, ch = img.shape
    length = int(l * c * ratio)
    lin = np.random.randint(0, l, [length])
    col = np.random.randint(0, c, [length])
    up_down = np.random.randint(0, 2, [length])
    for i in range(length):
        img[lin[i], col[i], np.random.randint(0, 3)] = 255 * up_down[i]
    return img

#####Lista de imagini cu zgomot impulsiv pe 10% din ele#########
imagini_zg_i = []
for i in range(len(lista_imagini)-2):
  c = addImpulse(lista_imagini[i],ratio = 0.1).astype(np.uint8)
  imagini_zg_i.append(c)
  #plt.figure(),plt.imshow(c)


imagini_zg_g_diferit = []
imagini_zg_i_diferit = []

for i in range(5,len(lista_imagini)):
  b1 = addGauss(lista_imagini[i],dispersie = 25).astype(np.uint8)
  b2 = addGauss(lista_imagini[i],dispersie = 50).astype(np.uint8)
  b3 = addGauss(lista_imagini[i],dispersie = 100).astype(np.uint8)
  imagini_zg_g_diferit.append(b1)
  imagini_zg_g_diferit.append(b2)
  imagini_zg_g_diferit.append(b3)

  c1 = addImpulse(lista_imagini[i],ratio = 0.07).astype(np.uint8)
  c2 = addImpulse(lista_imagini[i],ratio = 0.25).astype(np.uint8)
  c3= addImpulse(lista_imagini[i],ratio = 0.5).astype(np.uint8)
  imagini_zg_i_diferit.append(c1)
  imagini_zg_i_diferit.append(c2)
  imagini_zg_i_diferit.append(c3)



#for i in range(len(imagini_zg_g_diferit)):
#  plt.figure(),plt.imshow(imagini_zg_g_diferit[i])
  

#for i in range(len(imagini_zg_i_diferit)):
  #plt.figure(), plt.imshow(imagini_zg_i_diferit[i])


mask = np.array([[1/9, 1/9, 1/9],
                 [1/9, 1/9, 1/9],
                 [1/9, 1/9, 1/9]])

######Filtru de mediere aritmetica#######
def avg_filter(img_orig, mask):
    img_out = img_orig.copy()
    
    l, c, ch = img_out.shape
    for i in range(1, l - 2):
        for j in range(1, c - 2):
            for k in range(ch):
                img_out[i, j, k] = np.sum((img_orig[i-1:i+2, j-1:j+2, k] * mask).flatten())
    return img_out.astype(np.uint8)

imagini_filtrate_aritmetica_g = []
for i in range (len(imagini_zg_g)):
  a = avg_filter(imagini_zg_g[i],mask).astype(np.uint8)
  #plt.figure(),plt.imshow(a)
  imagini_filtrate_aritmetica_g.append(a)


imagini_filtrate_aritmetica_i = []
for i in range(len(imagini_zg_i)):
  b = avg_filter(imagini_zg_i[i],mask).astype(np.uint8)
  #plt.figure(),plt.imshow(b)
  imagini_filtrate_aritmetica_i.append(b)

imagini_i_aritmetica = []
imagini_g_aritmetica = []
for i in range(len(imagini_zg_i_diferit)):
  a = avg_filter(imagini_zg_i_diferit[i],mask).astype(np.uint8)
  b = avg_filter(imagini_zg_g_diferit[i],mask).astype(np.uint8)
  #plt.figure(),plt.imshow(a)
  #plt.figure(),plt.imshow(b)
  imagini_i_aritmetica.append(a)
  imagini_g_aritmetica.append(b)



########Filtru median########

def median(img):
    img_out = img.copy()
    l, c, p = img.shape

    for i in range(1, l - 1):
        for j in range(1, c - 1):
            for k in range(3):
                img_out[i, j, k] = np.sort(img[i - 1:i + 2, j - 1:j + 2, k], axis=None)[4]

    return img_out.astype(np.uint8)


imagini_filtrate_median_g = []
for i in range (len(imagini_zg_g)):
    a = median(imagini_zg_g[i])
    plt.figure(),plt.imshow(a)
    imagini_filtrate_median_g.append(a)


imagini_filtrate_median_i = []
for i in range(len(imagini_zg_i)):
    b = median(imagini_zg_i[i])
    plt.figure(),plt.imshow(b)
    imagini_filtrate_median_i.append(b)

imagini_i_median = []
imagini_g_median = []
for i in range(len(imagini_zg_i_diferit)):
    a = median(imagini_zg_i_diferit[i])
    b = median(imagini_zg_g_diferit[i])
    plt.figure(),plt.imshow(a)
    plt.figure(),plt.imshow(b)
    imagini_i_median.append(a)
    imagini_g_median.append(b)


######Filtrare Fuzzy Peer########
