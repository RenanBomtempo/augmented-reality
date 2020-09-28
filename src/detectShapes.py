import cv2
import numpy as np


aux = 0

# (Debug)
def log(list,n=0):
    f = open("log_"+str(n)+".txt","w")
    f.write(str(list))
    f.close()

# Calcula erro medio quadratico
def calc_rmse(predictions, targets):
    return np.sqrt(((predictions - targets) **2).mean())

# Desenha circulos em volta e enumera na imagem os vertices de um quadrilatero (Debug)
def drawOrder(img,points):
    for i in range(4):
        img = cv2.circle(img, tuple(points[i][0]), 5, (0, 100, 0), -1)
        img = cv2.putText(img,str(i), tuple(points[i][0]), cv2.FONT_HERSHEY_SIMPLEX,
                          1, (0, 255, 255), 2, cv2.LINE_AA)

# Verifica se um candidato a alvo é um alvo, e se sim, qual sua orientecao
def trackerOrient(img, alvo, points,frame):
    global aux
    threshold = 127

    palvo = np.ones(alvo.shape)
    palvoPoints = np.array([[0,0],[0,alvo.shape[1]],
                            [alvo.shape[0],alvo.shape[1]],[alvo.shape[0],0]])

    h, status = cv2.findHomography(points, palvoPoints)
    palvo = cv2.warpPerspective(img, h, (palvo.shape[0], palvo.shape[1]))

    alvo0 = cv2.cvtColor(alvo, cv2.COLOR_BGR2GRAY)
    _, alvo0 = cv2.threshold(alvo0, threshold, 255, cv2.THRESH_BINARY)

    # Criando os alvos rotacionados
    alvo1 = cv2.rotate(alvo0, cv2.ROTATE_90_CLOCKWISE)
    alvo2 = cv2.rotate(alvo1, cv2.ROTATE_90_CLOCKWISE)
    alvo3 = cv2.rotate(alvo2, cv2.ROTATE_90_CLOCKWISE)

    alvos = [alvo0,alvo1,alvo2,alvo3]

    # Verificando qual orientação produz o menor erro quadratico
    orient = -1
    minErr = 999
    for i in range(4):
        err = calc_rmse(palvo,alvos[i])
        if err<4 and err<minErr:
            minErr = err
            orient = i

    # No vetor de pontos os poontos estão em sentido anti-horario, mas enumerei
    # As possiveis rotções no sentido horario, então esse order inverte isso
    #order = [points[0][0], points[3][0], points[2][0], points[1][0]]
    orderAnti = [0,3,2,1]
    orient = orderAnti[orient]
    # Origem
    if orient>=0:
        #origem = order[orient]
        return True, orient

    return False,(0,0)
    #--------------------------------------------------------------------------
    # print("possivel alvo", aux, end='')
    # palvo = cv2.cvtColor(palvo,cv2.COLOR_GRAY2RGB)

    # order2 = [palvoPoints[0], palvoPoints[3], palvoPoints[2], palvoPoints[1]]
    # palvo = cv2.circle(palvo, tuple(order2[orient]), 40, (255,0,0), -1)

    # Marcar na imagem qual a origem estimada
    # order = [points[0][0],points[3][0],points[2][0],points[1][0]]
    # frame = cv2.circle(frame, tuple(order[orient]), 10, (255,0,0), -1)

    # cv2.imshow('Possivel Alvo' + str(aux), palvo)
    # cv2.imshow('alvo0', alvo0)
    # cv2.imshow('alvo1', alvo1)
    # cv2.imshow('alvo2', alvo2)
    # cv2.imshow('alvo3', alvo3)
    aux += 1

def detect4Polig(img,alvo):
    # Binarização
    threshold = 127

    # Área mínima para ser detectada
    ax = 100*100

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,imgBin = cv2.threshold(imgGray, threshold, 255, cv2.THRESH_BINARY)
    imgCanny = cv2.Canny(imgBin, 100, 200)

    # Dilatar as bordas
    kernel = np.ones((5, 5))
    imgCanny = cv2.dilate(imgCanny, kernel, iterations=1)

    # Encontra os contornos da imagem. RETR_EXTERNAL apenas os mais externos RETR_TREE todos
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    numTrakers = 0
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # Caso a curva tiver 4 lados, for convexa e possui uma area minima de ax pixels
        if len(approx) == 4 and cv2.isContourConvex(approx) and cv2.contourArea(approx)>ax:
            # Ordem em que os vertices foram escritos
            # drawOrder(img, approx)
            istraker, indice_origem = trackerOrient(imgBin, alvo, approx,img)

            if istraker:
                numTrakers += 1
                origem = approx[indice_origem][0]
                eixox = [origem, approx[(indice_origem+1)%4][0]]
                eixoy = [origem, approx[(indice_origem-1)%4][0]]


                cv2.drawContours(img, [approx], 0, (0, 255, 0), 1)
                img = cv2.circle(img, tuple(origem), 10, (255, 0, 0), -1)

                # Desenhar os eixos
                img = cv2.line(img, tuple(eixox[0]),tuple(eixox[1]), (255,0,0), 6)
                img = cv2.line(img, tuple(eixoy[0]), tuple(eixoy[1]), (0, 0, 255), 6)
                # Colocar nome nos alvos
                org = (approx[0][0][0]-50,approx[0][0][1]-50)
                img = cv2.putText(img, 'Alvo '+str(numTrakers-1), org, cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2, cv2.LINE_AA)

        # Desenhar todos os contornos
        #cv2.drawContours(img, [approx], 0, (0, 0, 255), 1)
    print("Detected :",numTrakers)
    return img

def MakeVideo(videoIn,alvo):
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 29.8, (1920, 1080))

    # Loop para cada frame do video
    while(videoIn.isOpened()):
        ret, frame = videoIn.read()
        if ret==True:

            frame = detect4Polig(frame,alvo)

            out.write(frame)
        else:
            break

    # Release
    out.release()

#------------------------------------------------------------------------------

# Abrindo o video e imagem alvo
videoIn = cv2.VideoCapture('tp2-icv-input.mp4')
alvo = cv2.imread('alvo.jpg')

# assumindo que o alvo é quadrado
alvo = cv2.resize(alvo,(322,322),interpolation = cv2.INTER_AREA)

ret, frame = videoIn.read()
frame = detect4Polig(frame,alvo)

MakeVideo(videoIn,alvo)

cv2.imshow("frame",frame)
videoIn.release()
cv2.waitKey(0)

