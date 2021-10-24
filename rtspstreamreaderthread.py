# 192.168.137.151:81
# host = "http://192.168.1.191:8080"
# host = "rtsp://192.168.1.191:554/11"

import threading
import time
import logging
import numpy as np
import struct
import logging
from Config import config
from NonBufferedCapture import VideoCapture


class RTSPStreamCaptureThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, host='rtsp://192.168.137.153',
                 args=(), kwargs=None, verbose=None):
        super(RTSPStreamCaptureThread, self).__init__()
        self.target = target
        self.name = name
        self.host = host

        return

    def run(self):
        images = []
        try:
            cap = VideoCapture(self.host)  # non buffered video capture with read method overridden

        except Exception as e:
            print(e)
            return

        while True:
            try:
                img = cap.read()

                if not config.log_queue_im.full():
                    config.log_queue_im.put(img)

                # im.show()
                # time.sleep(config.approx_update_rate)

            except Exception as e:
                logging.debug(str(e))


        return
