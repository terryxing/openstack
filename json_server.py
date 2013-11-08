"""
This is a json server that communication with other process, provided by murphy to be added into the POX lib
"""

from pox.core import core
from pox.lib.ioworker.workers import *
from pox.lib.ioworker import *
from pox.lib.revent import *

import json


# IOLoop for our IO workers
_ioloop = None

# Log
log = None


class JSONEvent (Event):
  """
  Event fired whenever a JSON message is received
  """
  def __init__ (self, worker, msg):
    super(JSONEvent,self).__init__()
    self.worker = worker
    self.msg = msg

  def __str__ (self):
    return "<%s: %s>" % (self.worker, self.msg)


class JSONDestreamer (object):
  """
  Destreams JSON

  That is, it handles the "framing" of JSON messages in a stream.
  """
  #TODO: Put this somewhere in pox.lib
  decoder = json.JSONDecoder()

  def __init__ (self, callback = None):
    self._buf = ''
    self.callback = callback if callback else self.rx

  def rx (self, msg):
    print(msg)

  def push (self, data):
    if len(self._buf) == 0:
      data = data.lstrip()
    self._buf += data
    try:
      while len(self._buf) > 0:
        r,off = self.decoder.raw_decode(self._buf)

        self._buf = self._buf[off:].lstrip()
        self.callback(r)
    except ValueError:
      pass


class ServerWorker (TCPServerWorker, RecocoIOWorker):
  """
  Worker to accept connections
  """
  pass


class JSONWorker (RecocoIOWorker):
  """
  Worker to receive JSON message
  """
  def __init__ (self, *args, **kw):
    super(JSONWorker, self).__init__(*args, **kw)
    self._connecting = True
    self.destreamer = JSONDestreamer(callback = self._rx_msg)

  def _handle_close (self):
    log.info("Client disconnect")
    super(JSONWorker, self)._handle_close()
    #clients.discard(self)

  def _handle_connect (self):
    log.info("Client connect")
    super(JSONWorker, self)._handle_connect()
    #clients.add(self)

  def _handle_rx (self):
    try:
      self.destreamer.push(self.read())
    except:
      log.exception("Failed to destream JSON")
      self.close()

  def _rx_msg (self, msg):
    """
    Handle complete JSON messages

    Called by the JSON destreamer
    """
    e = JSONEvent(self, msg)
    core.JSONServer.raiseEventNoErrors(e)


class JSONServer (EventMixin):
  """
  Listens on a TCP socket for JSON messages

  For each message, JSONEvent is fired.
  """
  _eventMixin_events = set([JSONEvent])

  def __init__ (self, port = 8987):
    w = ServerWorker(child_worker_type=JSONWorker, port = port)
    self.server_worker = w
    _ioloop.register_worker(w)


def launch (port = 8987):
  # Set up logging
  global log
  log = core.getLogger()

  # Set up IO loop
  global _ioloop
  _ioloop = RecocoIOLoop()
  #_ioloop.more_debugging = True
  _ioloop.start()

  # Register our little JSON core as a component
  core.registerNew(JSONServer, port=int(port))
