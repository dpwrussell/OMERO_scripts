from omero_basics import OMEROConnectionManager
import cv2
import numpy

# Assemble with ffmpeg, e.g.
# ffmpeg -framerate 1 -i color_img_%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p -r 60 test.mp4

conn_manager = OMEROConnectionManager()
conn = conn_manager.connect()

conn.SERVICE_OPTS.setOmeroGroup('-1')
image = conn.getObject('Image', 477168)
pixels = image.getPrimaryPixels()
sizeX = image.getSizeX()
sizeY = image.getSizeY()
sizeZ = image.getSizeZ()
sizeC = image.getSizeC()
sizeT = image.getSizeT()

font = cv2.FONT_HERSHEY_SIMPLEX
# zct_list = [(0, 0, 0, (0, 0, sizeX, sizeY))]
#
# z = 0
# t = 0

# plane = getPlane(rendering_engine, z, t)
# plane = next(pixels.getTiles(zct_list))
for z in xrange(sizeZ):
    rendered_image = image.renderImage(z, 0)
    # plane = numpy.array(rendered_image, dtype='uint32')
    plane = numpy.array(rendered_image)
    print plane.shape
    # plane = plane.byteswap()
    # print plane.shape
    # exit(1)
    # plane = plane.reshape(sizeX, sizeY)
    RGB_plane = cv2.cvtColor(plane, cv2.COLOR_BGR2RGB)
    cv2.putText(RGB_plane, 'Test1!', (0, 35), font, 1, (0, 0, 255),
                2, cv2.LINE_AA)
    cv2.putText(RGB_plane, 'Test2!', (0, 70), font, 1, (0, 255, 0),
                2, cv2.LINE_AA)
    cv2.putText(RGB_plane, 'Test3!', (0, 105), font, 1, (255, 0, 0),
                2, cv2.LINE_AA)
    cv2.putText(RGB_plane, 'Test4!', (0, 140), font, 1, (255, 255, 255),
                2, cv2.LINE_AA)
    cv2.imwrite('color_img_{}.jpg'.format(z), RGB_plane)

# exit(1)
# planeImage = plane
# planeImage = numpy.array(plane, dtype='uint32')
# planeImage = planeImage.byteswap()
# planeImage = planeImage.reshape(sizeX, sizeY)
# i = Image.frombuffer('RGBA', (sizeX, sizeY), planeImage.data, 'raw', 'ARGB', 0,
#                      1)

# fourcc = VideoWriter_fourcc(*'XVID')
# video = VideoWriter('movie.avi', fourcc, 3.0, (image.getSizeX(),
#                     image.getSizeY()), True)
# for i in xrange(10):
#     video.write(plane)
# video.release()


# ffmpeg -framerate 1 -i color_img_%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p -r 60 test.mp4
