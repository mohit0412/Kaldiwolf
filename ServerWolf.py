"""
Author: humblewolf
Description: This implements the websocket server
"""

import argparse
import logging
import threading
from gevent import monkey; monkey.patch_all()
from ws4py.server.geventserver import WebSocketWSGIApplication, WebSocketWSGIHandler, WSGIServer
from ws4py.websocket import EchoWebSocket
from multiprocessing import Process, Queue
from RedisQueueWolf import PySimpleQueue
from ConstantsWolf import ConstantsWolf as cw
import VadWolf as VW

logging.basicConfig(filename=cw.srv_log_loc, level=logging.DEBUG, format= '%(asctime)s %(levelname)s %(message)s')


class BroadcastWebSocket(EchoWebSocket):

    def check_tcptqueue(self):
        while True:
            try:
                msg = self.tcptQueue.get(self.tcpt_queue_uuid)
                if msg:
                    self.send_message(msg)
            except:
                pass

    def send_message(self, msg):
        with self.lock:
            self.send(msg)#this can be problematic

    def opened(self):
        base_key = PySimpleQueue.get_true_base_uuid()
        self.aud_queue_uuid = base_key+"_in"
        self.tcpt_queue_uuid = base_key+"_out"
        self.audQueue = PySimpleQueue()
        self.tcptQueue = PySimpleQueue()
        self.lock = threading.RLock()

        # spawn a process to do vad and pass data to the queue.....
        self.p = Process(name="ServerWolf_vad_proc", target=VW.vadetectwork, args=(self.aud_queue_uuid, self.tcpt_queue_uuid, base_key))
        self.p.start()
        print("New process spawned for vad")

        # spawn a thread to check o/p data from tcptQueue.......
        self.t = threading.Thread(name="ServerWolf_op_queue_chk_thr", target=self.check_tcptqueue)
        self.t.start()
        print("New thread spawned for o/p checking")


    def received_message(self, m):
        self.audQueue.put(self.aud_queue_uuid, m.data)
        #print("msg recv and placed on queue")


class EchoWebSocketApplication(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ws = WebSocketWSGIApplication(handler_cls=BroadcastWebSocket)

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'] == '/ws':
            environ['ws4py.app'] = self
            return self.ws(environ, start_response)

        return None


if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()

    parser = argparse.ArgumentParser(description="Kaldiwolf's Server")
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    app = EchoWebSocketApplication(args.host, args.port)
    server = WSGIServer((args.host, args.port), app)
    logging.info("Going to start kaldiwolf's websocket server")
    server.serve_forever()