#!/usr/bin/python2
from genericore import Configurable
import pystache,cherrypy
import logging, sys
from datetime import datetime
import modules
import os
from os import path


log = logging.getLogger('shiny')

TEMPLATE_DIR=path.join(path.dirname(sys.argv[0]) + "/../template/" )
MODULE_DIR=path.join(path.dirname(sys.argv[0]) + "/modules" )

DEFAULT_CONFIG = { "http" : {
          "socket_port" : 8080,
          "socket_host" : "0.0.0.0"
          }
}

class Shiny(Configurable):  #TODO pull out the HTTP server Component
  stats = {}
  avail = [] # available modules (will be written automagically
  templates = {}

  def __init__(self,MODULE_NAME,conf=None):
    self.NAME = MODULE_NAME
    newConf = {MODULE_NAME : DEFAULT_CONFIG}
    Configurable.__init__(self,newConf)
    self.load_conf(conf)
    self.init_modules()
    cherrypy.server.__dict__.update(self.config[MODULE_NAME]["http"])

  def process(self,stats):
    log.debug("Received Stats: " + str(stats))
    self.stats[stats['type']] = stats['data']
    self.stats[stats['type']]['timestamp'] = datetime.now().ctime()

  def create_connection(self):
    cherrypy.tree.mount(self)
    cherrypy.server.quickstart()
    cherrypy.engine.start()

  def get_modules(self):
    extension = ".py"
    list_of_files = [file for file in os.listdir(MODULE_DIR) if file.lower().endswith(extension)]

  def init_modules(self):
    self.avail = [ getattr(modules,mod) for mod in dir(modules) if not mod.startswith('__')]
    print "Available Modules " + str(self.avail)
    for mod in self.avail:
      log.info('loaded module ' + mod.path)
      self.register_module(mod)
      self.load_template(mod)
      for i in mod.dispatch:
        self.stats[i] = {}

  def load_template(self,mod):
    if getattr(mod,'template_name',False):
      p = TEMPLATE_DIR + 'templatename'
    else:
      p = TEMPLATE_DIR + mod.path + '.mustache' # probably not mustache dir?
    log.debug('Loaded Template: ' +str(p))
    f = open(p)
    self.templates[mod.path] = f.read()
    f.close()

  def register_module(self,mod):
    setattr(self,mod.path,lambda :mod.process(self))
    getattr(self,mod.path).exposed=True
    
  def populate_parser(self,parser): 
    parser.add_argument('--http-port',type=int,dest='http_port',help='Http Server host port',metavar='PORT')   
    parser.add_argument('--http-host',dest='http_host',help='Http Server host Address',metavar='ADDR')   
    #TODO template options for irc and mail
    #TODO refactor this piece

  def eval_parser(self,parsed): 
    conf = self.config[self.NAME]
    cherrypy.server.socket_port = parsed.http_port if parsed.http_port else conf['http']['socket_port']
    cherrypy.server.socket_host = parsed.http_host if parsed.http_host else conf['http']['socket_host']

  def close_connection(self):
    cherrypy.engine.exit()
