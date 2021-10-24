import queue

class config:
    log_queue_tx2 = queue.Queue(maxsize=30)
    log_queue_server = queue.Queue(maxsize=30)
    log_queue_nano = queue.Queue(maxsize=30)
    log_queue_im = queue.Queue(maxsize=30)