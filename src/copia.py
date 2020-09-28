import cv2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

from objloader import *
import numpy as np

def initOpenGL(cameraMatrix, dimensions):
	(width, height) = dimensions

	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

	lightAmbient = [1.0, 1.0, 1.0, 1.0]
	lightDiffuse = [1.0, 1.0, 1.0, 1.0]
	lightPosition = [1.0, 1.0, 1.0, 0.0]

	glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
	glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	fx = cameraMatrix[0,0]
	fy = cameraMatrix[1,1]
	fovy = 2*np.arctan(0.5*height/fy)*180/np.pi
	aspect = (width*fy)/(height*fx)
	gluPerspective(fovy, aspect, 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)

	obj = OBJ("Pikachu.obj", swapyz=True)
	#print('ok3')
	glEnable(GL_TEXTURE_2D)

	background_id = glGenTextures(1)

	return obj, background_id

def object3D(rect, indices, cameraMatrix, distCoeffs, obj):
	imagePoints = np.array(rect, dtype="float32")
	objectPoints = np.array([[-1, -1, 1], [ 1, -1, 1],
		                     [ 1, 1, 1], [-1, 1, 1]], dtype="float32")
	_, rvecs, tvecs = cv2.solvePnP(objectPoints[indices], imagePoints, cameraMatrix, distCoeffs)
	rotm = cv2.Rodrigues(rvecs)[0]

	m = np.array([[rotm[0][0], rotm[0][1], rotm[0][2], tvecs[0]], 
		          [rotm[1][0], rotm[1][1], rotm[1][2], tvecs[1]], 
		          [rotm[2][0], rotm[2][1], rotm[2][2], tvecs[2]],
		          [       0.0,        0.0,        0.0,      1.0]])

	##opencv coordinate system to opengl coordinate system
	flip_y_and_z_axis = np.array([[1, 0,  0, 0],
		                          [0, 1,  0, 0],
		                          [0, 0, -1, 0],
		                          [0, 0,  0, 1]])
	m = np.dot(flip_y_and_z_axis, m)

	m = np.transpose(m)
	glLoadMatrixd(m)

	##glutSolidCube(2.0)
	glCallList(obj.gl_list)

def correlation_coefficient(patch1, patch2):
	product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
	stds = patch1.std() * patch2.std()
	if stds == 0:
		return 0
	else:
		product /= stds
		return product

def findMarkers(img):
	"""
	Encontra os alvos no frame atual.
	:param img: frame a ser processado
	:return: lista dos alvos encontrados
	"""
	alvo = cv2.imread('alvo.jpg')
	alvo = cv2.cvtColor(alvo, cv2.COLOR_BGR2GRAY)
	
	ret, binaryAlvo = cv2.threshold(alvo, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	(markerSize, _) = binaryAlvo.shape

	markers = []
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	edged = cv2.Canny(gray, 50, 150)
	cnt, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

	cnt = sorted(cnt, key = cv2.contourArea, reverse = True)[:10]

	eps = (640 + 480)*0.01
	
	for c in cnt:
		isMarker = False
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, eps, True)

		if len(approx) == 4:
			min_dist = 1e6
			c_indices = None
			c_cords = None

			dst = np.array([[0, 0], [0, markerSize], [markerSize, markerSize], [markerSize, 0]], dtype="float32")
			indices = np.arange(4)

			for rotations in range(4):
				src = np.array(approx.reshape(4,2), dtype="float32")
				matrix = cv2.getPerspectiveTransform(src, dst[indices])
				warped = cv2.warpPerspective(gray, matrix, (markerSize, markerSize))

				cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)
				cv2.imshow('debug1', img)

				ret, binaryImg = cv2.threshold(warped, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
				##cv2.imshow('debug2', binaryImg)
				##cv2.waitKey(+)

				##dist = correlation_coefficient(binaryImg, binaryAlvo)
				#dist = np.sqrt(np.sum(np.square(binaryImg, binaryAlvo)))
				shape = binaryImg.shape
				dist = np.sqrt(np.sum(np.square(binaryImg, binaryAlvo[:shape[0],:shape[1]])))

				##print dist
				if dist < min_dist and dist > 80:
					min_dist = dist
					c_indices = indices
					c_cords = src

				indices = np.roll(indices, -1)
				##print dist

			if c_cords is not None:
				markers.append((c_cords, c_indices))
				##print c_cords c_indices

	return markers

def displayCallback():
	"""
	Callback do glut.
	"""
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	ret, frame = cap.read()
	if ret == True:
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

		markers = findMarkers(frame)

		for rect in markers:
			object3D(rect[0], rect[1], cameraMatrix, distCoeffs, obj)

			glutSwapBuffers()

	else:
		glutDestroyWindow(window)

def idleCallback():
	"""
	Callback do glut
	"""
	glutPostRedisplay()

if __name__ == '__main__':

	##intrinsicDict = readYAMLFile("instrinsic.vml")
	cameraMatrix = np.array([[1232.95030, 0., 932.47503],
		                     [0,  1225.84345, 505.11582], [0., 0., 1.]])##intrinsicDict["c...?"]
	distCoeffs = np.array([1.3, 7.7, 0., 0., 1.5])#intrinsicDict['distortion_coefficients']
	
	dimensions = (640, 480)#(intrinsicDict['image_width'], intrinsicDict['image_hight'])

	cap = cv2.VideoCapture('tp2-icv-input.mp4')

	if (cap.isOpened() == False):
		print("Error opening video stream or file")
	
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
	glutInitWindowSize(*dimensions)
	window = glutCreateWindow(b'Realidade Aumentada')

	obj, background_id = initOpenGL(cameraMatrix, dimensions)

	glutDisplayFunc(displayCallback)
	glutIdleFunc(idleCallback)

	glutMainLoop()

	cap.release()