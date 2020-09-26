import cv2
import numpy as np


def detect4Polig(img):
    # Binarização
    threshold = 127
    # Área mínima para ser detectada
    ax = 200

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,imgBin = cv2.threshold(imgGray, threshold, 255, cv2.THRESH_BINARY)
    imgCanny = cv2.Canny(imgBin, 100, 200)

    # Dilatar as bordas
    kernel = np.ones((5, 5))
    imgCanny = cv2.dilate(imgCanny, kernel, iterations=1)
    # Encontra os contornos da imagem. RETR_EXTERNAL apenas os mais externos RETR_TREE todos
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 1)
        #x = approx.ravel()[0]
        #y = approx.ravel()[1]

        # Caso a curva tiver 4 lados, for convexa e possui uma area minima de ax pixels
        if len(approx) == 4 and cv2.isContourConvex(approx) and cv2.contourArea(approx)>ax:
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
            # RENAN é aqui que tem que verificar os treco de homografia

    return img

def MakeVideo(videoIn):
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 29.8, (1920, 1080))

    # Loop para cada frame do video
    while(videoIn.isOpened()):
        threshold = 127
        ret, frame = videoIn.read()
        if ret==True:

            frame = detect4Polig(frame)

            out.write(frame)
        else:
            break

    # Release
    out.release()

#------------------------------------------------------------------------------

# Abrindo o video e imagem alvo
videoIn = cv2.VideoCapture('tp2-icv-input.mp4')
targetImg = cv2.imread('alvo.jpg')

ret, frame = videoIn.read()
frame = detect4Polig(frame)

MakeVideo(videoIn)


cv2.imshow("frame",frame)
cv2.waitKey(0)
videoIn.release()


