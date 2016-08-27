import cv,cv2
import numpy as np
import os
#clip = "drip.avi" # b&w droplet
clip = "IMG_0766_4sec.MOV" # See See small
# clip = "DSCF4481.MOV" # See See tea
outN = "small"
# clip = "20131208_142558_707_muni10.mp4" # subway station

src = "vids"
dest = "pix/%s" % (outN)
# dest = os.path.join("/Users/kevinbjorke/Google Drive",'kbImport','Cg','subway')

cap = cv2.VideoCapture(os.path.join(src,clip)) # subway station

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
s = frame1.shape
fourcc = cv.FOURCC('m','p','4','v')
out = cv2.VideoWriter()
out.open(os.path.join(dest,('output_%s.mov'%(outN))),fourcc, 30.0, (s[1],s[0]),True)
# out = cv2.VideoWriter('output.avi',fourcc, 30.0, (s[1],s[0]))
res2 = np.zeros(frame1.shape,float)
res8 = np.zeros(frame1.shape,float)
n = 0
while(1):
    try:
        ret, frame2 = cap.read()
        nextF = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    except:
        break
    # cv2.calcOpticalFlowFarneback(prev, next, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags[, flow]) 
    pyr_scale = 0.5
    levels = 3
    winsize = 15
    iterations = 3
    poly_n = 5
    poly_sigma = 1.2
    flags = 0
    flow = cv2.calcOpticalFlowFarneback(prvs,nextF, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags) # vers 2
    #flow = cv2.calcOpticalFlowFarneback(prvs,nextF, 0.5, 3, 15, 3, 5, 1.2, 0) # vers 2
    s = nextF.shape
    cols = np.zeros((s[0],s[1]),dtype=int) + np.arange(0,s[1],dtype=int)
    rows = np.zeros((s[1],s[0]),dtype=int) + np.arange(0,s[0],dtype=int)
    rows = np.transpose(rows)
    res = np.zeros(frame2.shape,float)
    rg = np.arange(-1.,2.,0.1)
    for m in rg:
        v,u = cv2.split(flow*m)
        cols = cols + u
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
        res = res + frame2[rows,cols]
    res = res / len(rg)
    res2 = res2 + res
    res8 = res8 + res
    #img = np.res(res,int)
    clipper = np.ones(res.shape,dtype=float)*255
    res = np.where(res<clipper,res,clipper)
    rx = np.asarray(res,np.dtype('uint8'))
    cv2.imshow('frame2',rx)
    # Scv2.imwrite('pix/rx_%04d.png'%(n),rx)
    out.write(rx)
    #cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        # print 'bye'
        break
    elif k == ord('s'):
        # print 'hi %d'%(n)
        cv2.imwrite('pix/b_%04d_f.png'%(n),res)
        # cv2.imwrite('pix/b_%04d_c.png'%(n),frame2)
    prvs = nextF
    n = n + 1
    if (n%8)==0:
        res8 = res8 / 8
        res8 = np.where(res8<clipper,res8,clipper)
        rx = np.asarray(res8,np.dtype('uint8'))
        cv2.imwrite(os.path.join(dest,'%s8_%04d.jpg'%(outN,n)),rx)
        res8 = np.zeros(frame1.shape,float)
       

res2 = res2 / n
clipper = np.ones(res2.shape,dtype=float)*255
res2 = np.where(res2<clipper,res2,clipper)
rx = np.asarray(res2,np.dtype('uint8'))
cv2.imshow('FINAL',rx)
k = cv2.waitKey(5000) & 0xff
cv2.imwrite(os.path.join(dest,('%s_final.jpg'%(outN))),rx)
 

cap.release()
out.release()
cv2.destroyAllWindows()