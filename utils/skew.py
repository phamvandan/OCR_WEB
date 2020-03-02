from utils.deskew import Deskew

def skewImage(image):
	d = Deskew(image)
	image,angle = d.run()
	return image