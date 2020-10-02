# OpenCV
import cv2
import numpy as np

# OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
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

    fx = focal_len[0]
    fy = focal_len[1]

    fovy = 2*np.arctan(0.5*height/fy)*180/np.pi
    aspect = (width*fy)/(height*fx)
    gluPerspective(fovy, aspect, 0.01, 200.0)

    glMatrixMode(GL_MODELVIEW)

def idleCallback():
    glutPostRedisplay()

'''
Posiciona um objeto 3D em cima do alvo detectado na cena.
'''
def object3D(img_pts, orient, camera_matrix, dist_coef, obj):
    z =0
    world_pts = np.array([[-1, -1, z], [1, -1, z],
                          [ 1,  1, z], [-1, 1, z]], dtype="float32")


    img_pts = np.array(img_pts, dtype="float32")

    # Calculate rotation and translation vectors
    _, rot_vecs, t_vecs = cv2.solvePnP(world_pts, img_pts, camera_matrix, dist_coef)

    # Generate rotation matrix
    rot_m = cv2.Rodrigues(rot_vecs)[0]

    # Build projection matrix
    proj_matrix = np.array([[rot_m[0][0], rot_m[0][1], rot_m[0][2], t_vecs[0]],
                            [rot_m[1][0], rot_m[1][1], rot_m[1][2], t_vecs[1]],
                            [rot_m[2][0], rot_m[2][1], rot_m[2][2], t_vecs[2]],
                            [        0.0,         0.0,         0.0,      1.0]], dtype="float32")

	# Convert coordinate systems (OpenCV -> OpenGL)
    flip_yz = np.array([[1,  0,  0, 0],
		                [0, -1,  0, 0],
		                [0,  0, -1, 0],
		                [0,  0,  0, 1]])

    proj_matrix = np.dot(flip_yz, proj_matrix)
    glLoadMatrixd(np.transpose(proj_matrix))

    # Render frame
    glCallList(obj.gl_list)

    glutWireCube(2.0)

def drawBackground(frame):
    # Convert frame to OpenGL format
    background = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    background = cv2.flip(background, 0)

    height, width, channels = background.shape
    background = np.frombuffer(background.tobytes(), dtype=background.dtype, count=height * width * channels)
    background.shape = (height, width, channels)

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

    # Plane with video frame texture
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
        drawBackground(frame)

        # Detect image markers
        markers, img = detectMarkers(frame)

        # [Debug] Show marker orientation frame
        #cv2.imshow("alvos", img)
        
        # For each 
        for marker in markers:
            # Place OBJ model on top of the marker
            object3D(marker[0], marker[1], camera_matrix, dist_coef, obj)
        glutSwapBuffers()     

if __name__ == '__main__':
    # Intrinsic paremeters from camera calibration
    foc_len = (1203.33680, 1205.25410)
    pri_pt  = ( 959.50000,  539.50000)
    dist_coef = np.array([0.07433, -0.17385, -0.00486, 0.00222, 0.],dtype="float32")

    # Camera matrix
    camera_matrix = np.array([[foc_len[0],          0., pri_pt[0]],
		                      [        0.,  foc_len[1], pri_pt[1]], 
                              [        0.,          0.,      1.]],dtype="float32")

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
    initOpenGL(foc_len, dimensions)
        
    # Load Pikachu model
    obj = OBJ("Pikachu.obj", swapyz=True)

    # Background 
    background_id = glGenTextures(1)

    glutDisplayFunc(displayCallback)
    glutIdleFunc(idleCallback)

    glutMainLoop()

    vid.release()