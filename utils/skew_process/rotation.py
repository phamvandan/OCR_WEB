import cv2
import numpy as np

def rotateAndScale(img, angle , scaleFactor = 1.0):
    degreesCCW = angle
    (oldY,oldX) = img.shape[:2] 
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=degreesCCW, scale=scaleFactor) 
    newX,newY = oldX*scaleFactor,oldY*scaleFactor
    r = np.deg2rad(degreesCCW)
    newX,newY = (abs(np.sin(r)*newY) + abs(np.cos(r)*newX),abs(np.sin(r)*newX) + abs(np.cos(r)*newY))
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx 
    M[1,2] += ty
    rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX),int(newY)),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotatedImg

