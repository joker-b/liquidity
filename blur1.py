import cv2
import numpy as np
#cap = cv2.VideoCapture("vids/drip.avi") # b&w droplet
cap = cv2.VideoCapture("vids/IMG_0766_4sec.MOV") # See See small
# cap = cv2.VideoCapture("vids/DSCF4481.MOV") # See See tea
# cap = cv2.VideoCapture("vids/20131208_142558_707_muni10.mp4") # subway station

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

n = 0
while(1):
    ret, frame2 = cap.read()
    nextF = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    # cv2.calcOpticalFlowFarneback(prev, next, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags[, flow]) 
    flow = cv2.calcOpticalFlowFarneback(prvs,nextF, 0.5, 3, 15, 3, 5, 1.2, 0) # vers 2
    flow = flow * 4
    v,u = cv2.split(flow)
    s = nextF.shape
    cols = np.zeros((s[0],s[1]),dtype=int) + np.arange(0,s[1],dtype=int)
    cols = cols + u
    rows = np.zeros((s[1],s[0]),dtype=int) + np.arange(0,s[0],dtype=int)
    rows = np.transpose(rows)
    rows = rows + v
    cols = np.asarray(cols,int)
    rows = np.asarray(rows,int)
    
    clipper = np.zeros((s[0],s[1]),dtype=int)
    cols = np.where(cols>clipper,cols,clipper)
    rows = np.where(rows>clipper,rows,clipper)
    clipper = np.ones((s[0],s[1]),dtype=int)*(s[1]-1)
    cols = np.where(cols<clipper,cols,clipper)
    clipper = np.ones((s[0],s[1]),dtype=int)*(s[0]-1)
    rows = np.where(rows<clipper,rows,clipper)
    res = frame2[rows,cols]

    #cv2.imshow('frame2',rgb)
    cv2.imshow('res',res)

    k = cv2.waitKey(3000) & 0xff
    if k == 27:
        # print 'bye'
        break
    elif k == ord('s'):
        # print 'hi %d'%(n)
        cv2.imwrite('pix/s_%04d_f.png'%(n),newi)
        cv2.imwrite('pix/s_%04d_c.png'%(n),frame2)
    prvs = nextF
    n = n + 1
    # print n

cap.release()
cv2.destroyAllWindows()