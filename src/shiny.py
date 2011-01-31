#!/usr/bin/python2
from genericore import Configurable
import pystache,cherrypy
import logging, sys
from datetime import datetime
from os import path


log = logging.getLogger('shiny')

DEFAULT_CONFIG = {
        "http" : {
          "socket_port" : 8080,
          "socket_host" : "0.0.0.0"
          },
        "template" : {
            "engine" : "mustache", #currently only mustache is supported,so this entry has no effect
            #TODO register modules
            "files" : {
              "mail" : path.join( path.dirname(sys.argv[0]) + "/../template/mail.mustache")  ,
              "irc" : path.join( path.dirname(sys.argv[0]) + "/../template/irc.mustache")  ,
              "snmp" : path.join( path.dirname(sys.argv[0]) + "/../template/snmp.mustache")  
              }
          }
}

class Shiny(Configurable):  #TODO pull out the HTTP server Component
  stats = {'mail' : {}, 'irc' : {}, 'snmp' : {}} 
  def __init__(self,MODULE_NAME,conf=None):
    self.NAME = MODULE_NAME
    newConf = {MODULE_NAME : DEFAULT_CONFIG}
    Configurable.__init__(self,newConf)
    self.load_conf(conf)
    cherrypy.server.__dict__.update(self.config[MODULE_NAME]["http"])

  def process(self,stats):
    log.debug("Received Stats: " + str(stats))
    self.stats[stats['type']] = stats['data']
    self.stats[stats['type']]['timestamp'] = datetime.now().ctime()

  def create_connection(self):
    cherrypy.tree.mount(self)
    cherrypy.server.quickstart()
    cherrypy.engine.start()
    self.load_templates()

  def populate_parser(self,parser): 
    parser.add_argument('--http-port',type=int,dest='http_port',help='Http Server host port',metavar='PORT')   
    parser.add_argument('--http-host',dest='http_host',help='Http Server host Address',metavar='ADDR')   
    #TODO template options for irc and mail
    #TODO refactor this piece

  def eval_parser(self,parsed): 
    conf = self.config[self.NAME]
    cherrypy.server.socket_port = parsed.http_port if parsed.http_port else conf['http']['socket_port']
    cherrypy.server.socket_host = parsed.http_host if parsed.http_host else conf['http']['socket_host']

  def load_templates(self):
    self.templates = {}
    for k,v in self.config[self.NAME]['template']['files'].items():
      log.debug("Loading Template:" + str(v) )
      f = open(v)
      self.templates[k] = f.read()
      f.close()

  # path functions
  def index(self):
    """ will be called when a client requests '/' """
    # TODO write status "LED"s when mails and irc comes in 
    return "Check out : <a href='mail'>Mail</a> or <a href='irc'>IRC</a> or <a href='snmp'>SNMP User</a>stats"
  index.exposed=True
  
  # TODO make this more generic if necessary
  def mail(self):
    self.load_templates()
    if not self.stats['mail']:
      return "No Mail Statistics received yet!"
    return pystache.render(self.templates['mail'],self.stats['mail'])
  mail.exposed=True

  def snmp(self):
    data = self.stats['snmp']
    self.load_templates() # only if the template is changing a lot 

    if not data:
      return "No SNMP Statistics received yet!"

    stache = {'num_clients' : 0, 'mlist' : []}
    #strip out the timestamp and put it into root object
    stache['timestamp'] = data['timestamp']
    del data['timestamp']

    stache['num_clients'] = len(data)
    for mac,ips in data.items():
      stache['mlist'].append({'mac': mac, 'ips' : ', '.join(ips)})
    data['timestamp'] = stache['timestamp']
    return pystache.render(self.templates['snmp'],stache)
  snmp.exposed=True

  def irc(self): 
    return pystache.render(self.templates['irc'],self.stats['irc'])
  irc.exposed=True

  def close_connection(self):
    cherrypy.engine.exit()
