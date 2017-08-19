from omero_basics import OMEROConnectionManager
import cv2

conn_manager = OMEROConnectionManager()
conn = conn_manager.connect()

image = conn.getObject("Image", 870)
z, t, c = 0, 0, 0                     # first plane of the image
pixels = image.getPrimaryPixels()
plane = pixels.getPlane(z, c, t)      # get a numpy array.

ret, thresh1 = cv2.threshold(plane, 10, 255, cv2.THRESH_BINARY)

cv2.imwrite('color_img.jpg', thresh1)
