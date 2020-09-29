# OpenCV
import cv2
import numpy as np

# OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from collections import deque
from marker import *

from objloader import *

'''
Inicialização dos parâmetros da OpenGL.
'''
def initOpenGL(focal_len, dimensions):
    (width, height) = dimensions
     
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fx = camera_matrix[0,0]
    fy = camera_matrix[1,1]
    fovy = 2*np.arctan(0.5*height/fy)*180/np.pi
    aspect = (width*fy)/(height*fx)
    gluPerspective(fovy, aspect, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

def idleCallback():
    glutPostRedisplay()

'''
Posiciona um objeto 3D em cima do alvo detectado na cena.
'''
def object3D(img_pts, orient, camera_matrix, dist_coef, obj):
    world_pts = np.array([[-1, -1, 1], [ 1, -1, 1],
                          [1,  1, 1], [-1,  1, 1]], dtype="float32")

    world_pts = np.roll(world_pts, -orient)
    #img_pts = np.array([img_pts[0][0], img_pts[1][0], img_pts[2][0], img_pts[3][0]], dtype="float32")
    img_pts = np.array(img_pts, dtype="float32")
    print(world_pts, img_pts)

    # Calcular matrix de projeção
    _, rot_vecs, t_vecs = cv2.solvePnP(world_pts, img_pts, camera_matrix, dist_coef)
    rot_m = cv2.Rodrigues(rot_vecs)[0]

    proj_matrix = np.array([[rot_m[0][0], rot_m[0][1], rot_m[0][2], t_vecs[0]], 
                            [rot_m[1][0], rot_m[1][1], rot_m[1][2], t_vecs[1]], 
                            [rot_m[2][0], rot_m[2][1], rot_m[2][2], t_vecs[2]],
                            [        0.0,         0.0,         0.0,      1.0]])

	# Mudança de sistema de coordenadas (OpenCV -> OpenGL)
    flip_yz = np.array([[1,  0,  0, 0],
		                [0, -1,  0, 0],
		                [0,  0, -1, 0],
		                [0,  0,  0, 1]])

    proj_matrix = np.dot(flip_yz, proj_matrix)
    glLoadMatrixd(np.transpose(proj_matrix))

    # Renderiza o modelo do Pikachu
    glCallList(obj.gl_list)
    glutWireCube(2.0)

'''
Loop de renderização
'''
def displayCallback():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # habilita o uso de texturas (o Pikachu tem textura)
    glEnable(GL_TEXTURE_2D)

    read, frame = vid.read()

    if read:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        background = cv2.flip(background, 0)

        height, width, channels = background.shape
        background = np.frombuffer(background.tostring(), dtype=background.dtype, count=height * width * channels)
        background.shape = (height, width, channels)

        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, background_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, background)

        glDepthMask(GL_FALSE)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)

        glMatrixMode(GL_MODELVIEW)

        glBindTexture(GL_TEXTURE_2D, background_id)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, background)

        glPushMatrix()
        glBegin(GL_QUADS)
        glTexCoord2i(0, 0); glVertex2i(0, 0)
        glTexCoord2i(1, 0); glVertex2i(width, 0)
        glTexCoord2i(1, 1); glVertex2i(width, height)
        glTexCoord2i(0, 1); glVertex2i(0, height)
        glEnd()

        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        glDepthMask(GL_TRUE)
        glDisable(GL_TEXTURE_2D)

        alvos, img = detect_markers(frame)

        cv2.imshow("alvos", img)

        for alvo in alvos:
            # Posiciona o modelo 3D em cima do alvo
            object3D(alvo[0], alvo[1], camera_matrix, dist_coef, obj) 
        glutSwapBuffers()     

if __name__ == '__main__':
    # Intrinsic paremeters from camera calibration
    focal_len = (1295.66495, 1280.53452)
    princ_pt  = ( 915.60124,  478.74546)
    dist_coef = np.array([0.06646, 0.27952, -0.00221, -0.00802, 0.00000])

    # Camera matrix
    camera_matrix = np.array([[focal_len[0], 0., princ_pt[0]],
		                      [0.,  focal_len[1], princ_pt[1]], 
                              [0., 0., 1.]])

    # Open input video
    vid = cv2.VideoCapture('tp2-icv-input.mp4')

    # Viewport dimensions
    dimensions = (1920, 1080)

    # GLUT configuration
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
    glutInitWindowSize(*dimensions)
    window = glutCreateWindow(b'Realidade Aumentada')

    # OpenGL intialization
    initOpenGL(focal_len, dimensions)

    obj = OBJ("Pikachu.obj", swapyz=True)   
    # Background
    background_id = glGenTextures(1)

    glutDisplayFunc(displayCallback)
    glutIdleFunc(idleCallback)

    glutMainLoop()

    vid.release()