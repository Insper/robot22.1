import cv2


def pontos_fuga(img_bgr):
    """
    Cria e retorna uma nova imagem BGR com os
    pontos de fuga desenhados.

    Entrada:
    - img_bgr: imagem original no formato BGR

    Saída:
    - resultado: imagem BGR com os pontos de fuga desenhados 
    """


    resultado = img_bgr.copy()

    return resultado


if __name__ == "__main__":
    bgr = cv2.imread('figura_q1.png')
    resultado = pontos_fuga(bgr)

    cv2.imwrite("figura_q1_resultado.png", resultado)

    cv2.imshow('Original', bgr)
    cv2.imshow('Pontos de fuga', resultado)
    cv2.waitKey()
    cv2.destroyAllWindows()
