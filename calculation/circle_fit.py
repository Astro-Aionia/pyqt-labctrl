import numpy as np
import cv2

def get_binary(filename, threshold=96):
    img = cv2.imread(filename)
    ret, binary = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)
    lap = cv2.Laplacian(np.uint8(binary),cv2.CV_8U)
    lap = np.int64(np.absolute(lap))
    return np.sum(lap,axis=2)/3/255
def get_border(data):
    dim = data.shape
    border = []
    for i in range(dim[0]):
        for j in range(dim[1]):
            if data[i,j] != 0:
                border.append([i,j])
    return border
def avg(border,m,n):
    N = len(border)
    avg = 0
    for i in range(N):
        avg = avg + (border[i][0]**m)*(border[i][1]**n)
    avg = avg/N
    return avg
def circle_fit(border):
    y0 = 0.5*((avg(border,2,0)*avg(border,1,0)+avg(border,1,0)*avg(border,0,2)-avg(border,3,0)-avg(border,1,2))*(avg(border,0,1)**2-avg(border,0,2))-(avg(border,2,0)*avg(border,0,1)+avg(border,0,1)*avg(border,0,2)-avg(border,2,1)-avg(border,0,3))*(avg(border,1,0)*avg(border,0,1)-avg(border,1,1)))/((avg(border,1,0)**2-avg(border,2,0))*(avg(border,0,1)**2-avg(border,0,2))-(avg(border,1,0)*avg(border,0,1)-avg(border,1,1))**2)
    x0 = 0.5*((avg(border,2,0)*avg(border,0,1)+avg(border,0,1)*avg(border,0,2)-avg(border,0,3)-avg(border,2,1))*(avg(border,1,0)**2-avg(border,2,0))-(avg(border,2,0)*avg(border,1,0)+avg(border,1,0)*avg(border,0,2)-avg(border,1,2)-avg(border,3,0))*(avg(border,1,0)*avg(border,0,1)-avg(border,1,1)))/((avg(border,1,0)**2-avg(border,2,0))*(avg(border,0,1)**2-avg(border,0,2))-(avg(border,1,0)*avg(border,0,1)-avg(border,1,1))**2)
    return [x0, y0]