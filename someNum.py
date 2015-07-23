#
# some manipulations with numpy -- reminding myself what works
#

import cv2
import numpy as np

def get_pic():
	img = cv2.imread('pix/s_0125_c.png')
	return img

def show_pic(img):
	cv2.imshow('yup',img)
	k = cv2.waitKey(2000)
	cv2.destroyAllWindows()


def slice_sample(img):
	ball = img[180:240, 230:290]
	img[173:233, 100:160] = ball
	return img

def smaller(img):
	#s= img.shape
	#res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
	height, width = img.shape[:2]
	res = cv2.resize(img,(width/2, height/2), interpolation = cv2.INTER_CUBIC)
	return res

def grady(img):
	s = img.shape
	b = np.zeros( (s[0],s[1]) )
	w = np.ones( (s[0],s[1]) )
	gr = np.arange(0.0, 1.0, (1.0/s[1]), dtype=float)
	r = w*gr
	w = np.ones( (s[1],s[0]) )
	gr = np.arange(0.0, 1.0, (1.0/s[0]), dtype=float)
	g = w*gr
	g = np.transpose(g)
	return cv2.merge( (b,g,r) )

def wobs(img):
	"""
	use random horizontal offsets for each pixel
	"""
	s = img.shape
	cols = np.zeros((s[0],s[1]),dtype=int) + np.arange(0,s[1],dtype=int)
	rows = np.zeros((s[1],s[0]),dtype=int) + np.arange(0,s[0],dtype=int)
	rows = np.transpose(rows)
	r = np.random.randint(-8,8,size=(s[0],s[1]))
	cols = cols+r
	clipper = np.zeros((s[0],s[1]),dtype=int)
	cols = np.where(cols>clipper,cols,clipper)
	clipper = np.ones((s[0],s[1]),dtype=int)*(s[1]-1)
	cols = np.where(cols<clipper,cols,clipper)
	res = img[rows,cols]
	return res

"""
# indexing into arrays with arrays
>>> c = np.array([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
>>> rows = np.array([[0,1,0],[2,1,0],[2,2,2]])
>>> cols = np.array([[0,0,0],[1,1,1],[0,1,2]])
>>> c[rows,cols]
array([[1, 4, 1],
       [8, 5, 2],
       [7, 8, 9]])
useful?
r = np.random.random(size=(3,3))
f = np.ones()*0.5
np.where(r>f,r,f) # elementwise max
"""

i = get_pic()
i = slice_sample(i)
i = smaller(i)
i = wobs(i)
# i = grady(i)
show_pic(i)