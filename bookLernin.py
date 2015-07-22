import cv2
import numpy as np
#cap = cv2.VideoCapture("vids/drip.avi")
#cap = cv2.VideoCapture("vids/IMG_0766_4sec.MOV")
# cap = cv2.VideoCapture("vids/DSCF4481.MOV")
cap = cv2.VideoCapture("vids/20131208_142558_707_muni10.mp4")

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

n = 0
while(1):
    ret, frame2 = cap.read()
    nextF = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    # cv2.calcOpticalFlowFarneback(prev, next, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags[, flow]) 
    # flow = cv2.calcOpticalFlowFarneback(prvs,nextF, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow = cv2.calcOpticalFlowFarneback(prvs,nextF, 0.5, 3, 15, 3, 5, 1.2, 0) # vers 2

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    #cv2.imshow('frame2',rgb)
    s = flow.shape
    fakeb = np.zeros((s[0],s[1]))
    ns = (s[0],s[1],s[2]+1)
    flowbgr = np.dstack((flow,fakeb))
    # flowbgr = np.append(flow,fakeb)
    #cv2.imshow('frame2',flowbgr)
    horz = cv2.normalize(flow[...,0], None, 0, 255, cv2.NORM_MINMAX)
    print horz.dtype
    horz.astype('uint8')
    vert = cv2.normalize(flow[...,1], None, 0, 255, cv2.NORM_MINMAX)
    vert.astype('uint8')

    cv2.imshow('frame2',rgb)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',rgb)
    prvs = nextF
    n = n + 1
    # print n

cap.release()
cv2.destroyAllWindows()