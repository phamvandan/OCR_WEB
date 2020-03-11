from utils.deskew import Deskew
import imutils

def skewImage(image):
	d = Deskew(image)
	image,angle = d.run()
	return image