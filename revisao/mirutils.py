# -*- coding:utf-8 -*-


import cv2
import numpy as np
import matplotlib

def morpho_limpa(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
    mask = cv2.morphologyEx( mask, cv2.MORPH_OPEN, kernel )
    mask = cv2.morphologyEx( mask, cv2.MORPH_CLOSE, kernel )    
    return mask


def multiplot(imgs, legenda="No sub", plt=matplotlib.pyplot):
    """ Função que plota várias imagens - só funciona em Juputer (e lab)
    """
    fig, axes = plt.subplots(1,len(imgs), figsize=(24,8))    
    fig.suptitle(legenda)
    if len(imgs)==1: # Peculiaridade do subplot. Não é relevante para a questão
        ax = axes
        ax.imshow(cv2.cvtColor(imgs[0], cv2.COLOR_BGR2RGB))
        return
    for i in range(len(imgs)):
        axes[i].imshow(cv2.cvtColor(imgs[i], cv2.COLOR_BGR2RGB))
        
def multiplot_gray(imgs, legenda, plt=matplotlib.pyplot):
    """ Função que plota n imagens grayscale em linha
         só funciona em Juputer (e lab)
    """
    fig, axes = plt.subplots(1,len(imgs), figsize=(26,8))    
    fig.suptitle(legenda)
    if len(imgs)==1: # Peculiaridade do subplot. Não é relevante para a questão
        ax = axes
        ax.imshow(imgs[0],  vmin=0, vmax=255, cmap="Greys_r")
        return
    for i in range(len(imgs)):
        axes[i].imshow(imgs[i], vmin=0, vmax=255, cmap="Greys_r")
        
        
# Função centro de massa baseada na aula 02  https://github.com/Insper/robot202/blob/master/aula02/aula02_Exemplos_Adicionais.ipynb
# Esta função calcula centro de massa de máscara binária 0-255 também, não só de contorno
def center_of_mass(mask):
    """ Retorna uma tupla (cx, cy) que desenha o centro do contorno"""
    M = cv2.moments(mask)
    # Usando a expressão do centróide definida em: https://en.wikipedia.org/wiki/Image_moment
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return [int(cX), int(cY)]

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,3)
    cv2.line(img,(x,y - size),(x, y + size),color,3)
    
    
def hsv_hists(img, plt):
    """
        Plota o histograma de cada um dos canais HSV
        img - imagem HSV
        plt - objeto matplotlib
        só funciona em Juputer (e lab)
    """
    plt.figure(figsize=(20,10)); 
    img_h = img[:,:,0]
    img_s = img[:,:,1]
    img_v = img[:,:,2]
    histo_plot(img_h, "r","H", plt);
    histo_plot(img_s, "g","S", plt);
    histo_plot(img_v, "b","V", plt);

def make_hist(img_255, c, label, plt):
    """ img_255 - uma imagem com 3 canais de 0 até 255
        c a cor do plot
        label - o label do gráfico
        plt - matplotlib.pyplot
    """
    hist,bins = np.histogram(img_255.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()

    # plt.plot(cdf_normalized, color = c)
    plt.hist(img_255.flatten(),256,[0,256], color = c)
    plt.xlim([0,256])
    plt.legend(label, loc = 'upper left')
    plt.plot()

def histo_plot(img, cor, label, plt):
    """
        img - imagem
        cor - cor  no formato do matplotlib
        plt - matplotlib.pyplot object
         - só funciona em Juputer (e lab)

    """
    plt.figure(figsize=(10,5))
    make_hist(img, cor, label, plt)
    plt.show()
    plt.figure(figsize=(10,5))
    plt.imshow(img, cmap="Greys_r")#, vmin=0, vmax=255)    
    plt.title(label)

    
    
def center_of_contour(contorno):
    """ Retorna uma tupla (cx, cy) que desenha o centro do contorno"""
    M = cv2.moments(contorno)
    # Usando a expressão do centróide definida em: https://en.wikipedia.org/wiki/Image_moment
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (int(cX), int(cY))
    
def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,5)
    cv2.line(img,(x,y - size),(x, y + size),color,5)
    
font = cv2.FONT_HERSHEY_SIMPLEX

def texto(img, a, p):
    """Escreve na img RGB dada a string a na posição definida pela tupla p"""
    cv2.putText(img, str(a), p, font,1,(0,50,100),2,cv2.LINE_AA)
    
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


## Fonte: https://github.com/mirwox/prova1_2020/blob/solution/q2/Solucao_Q2.ipynb


def find_m_h(segmento):
    a = segmento[0]
    b = segmento[1]
    m = (b[1] - a[1])/(b[0] - a[0])
    h = a[1] - m*a[0]
    return m,h

def intersect_segs(seg1, seg2):
    m1,h1 = find_m_h(seg1)
    m2,h2 = find_m_h(seg2)
    x_i = (h2 - h1)/(m1-m2)
    y_i = m1*x_i + h1
    return x_i, y_i

def intersection(lista1, lista2):
    seg1 = random.choice(lista1)
    seg2 = random.choice(lista2)
    pt = intersect_segs(seg1, seg2)
    return (int(pt[0]), int(pt[1]))
