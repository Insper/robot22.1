import cv2
import matplotlib.pyplot as plt

from numpy.linalg import norm
import numpy as np

import math

def mostra_imagem(img, title=None, ticks=False, subfig=False):
    '''
    Função para mostrar a imagem colorida ou em tons de cinza,
    removendo as escalas
    '''
    if len(img.shape) < 3:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img[:,:,::-1])
    
    if not ticks:
        plt.yticks([])
        plt.xticks([])
    
    if title is not None: plt.title(title)
    if not subfig:
        plt.show()


def acumulador_hough_retas(image, rho, theta):
    '''
    Gera a imagem do acumulador da transformada de Hough para retas
    '''
    max_rho = int( norm(image.shape) )
    min_rho = -max_rho
    max_theta = np.pi
    min_theta = 0 

    rows = int((max_rho-min_rho)/rho)
    cols = int((max_theta-min_theta)/theta)
    votes = np.zeros((rows, cols), dtype=int)
    
    # Invoca a transformada de Hough
    for v in range(100):
        lines = cv2.HoughLines(image, rho, theta, v)
        if lines is not None:
            for line in lines:
                r, t = line[0]
                votes[int((r-min_rho)/rho), int((t-min_theta)/theta)] += 1
    
    return votes


def desenha_retas(image, lines):
    '''
    Desenha as retas encontradas pela transformada de Hough
    '''
    if len(image.shape) < 3:
        imout = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        imout = image.copy()

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(imout, pt1, pt2, (0,0,255), 1, cv2.LINE_AA)
    
    return imout


def desenha_circulos(image, circles):
    '''
    Desenha as circunferências encontradas pela transformada de Hough
    As circunferências são preenchidas (círculos)
    '''
    if len(image.shape) < 3:
        imout = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        imout = image.copy()

    if circles is not None:
        for circle in circles[0]:
            cv2.circle(imout, (int(circle[0]), int(circle[1])), int(circle[2]), (0,0,255), thickness=-1 )
    
    return imout




if __name__ == "__main__":
    # Imagem com apenas um ponto
    h = 100
    w = 100
    img1 = np.zeros((h, w), dtype=np.uint8)
    img1[h//2, w//2] = 255
    img1[h-1, w-1] = 255
    img1[h//2, w-2] = 255

    linhas1 = cv2.HoughLines(img1, 1, np.pi/180, 1)
    circs1 = cv2.HoughCircles(img1, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=110, param2=4, minRadius=10, maxRadius=50)

    votes1 = acumulador_hough_retas(img1, 1, np.pi/180) 

    plt.subplot(2, 2, 1)
    mostra_imagem(img1, subfig=True)
    plt.subplot(2, 2, 2)
    mostra_imagem(votes1, subfig=True)
    plt.subplot(2, 2, 3)
    mostra_imagem(desenha_retas(img1, linhas1), subfig=True)
    plt.subplot(2, 2, 4)
    mostra_imagem(desenha_circulos(img1, circs1))
    
    

