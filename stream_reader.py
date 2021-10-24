import numpy as np
from six import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cv2
from six.moves.urllib.request import urlopen
from rtspstreamreaderthread import RTSPStreamCaptureThread

from Config import config
import socket

# c = ImagePreprocessingThread(name='Imagepreprocessing', image_size=(512, 512))
# c.start()
p = RTSPStreamCaptureThread(name='RTSPreader', host='http://10.128.53.170:8090/')
p.start()

while True:
    try:
        if not config.log_queue_im.empty():
            image_np = config.log_queue_im.get()
            # selected_image = im
            flip_image_horizontally = False
            convert_image_to_grayscale = False

            # image_path = IMAGES_FOR_TEST[selected_image]
            # image_np = im.reshape(1, 512, 512, 3)

            try:
                cv2.imshow("Stream reader", image_np)
                cv2.waitKey(1)
            except Exception as e:
                print(e)
            # to_send = [image_np_with_detections, result]
            #
            # # Send inference result and bounding box to screen over network socket
            # bin_buff = msgpack.packb(to_send)
            # print(len(bin_buff))
            # s.sendall(b'AA')
            # s.sendall(msgpack.packb(to_send))

    except Exception as e:
        print(e)
