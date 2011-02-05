#!/usr/bin/env python2
import sys,json
from shiny import Shiny
import logging
import genericore as gen
MODULE_NAME='shiny'
log = logging.getLogger(MODULE_NAME)
PROTO_VERSION = 1
DESCRIPTION = 'Makes Statistics shiny'

# set up instances of needed modules

conf = gen.Configurator(PROTO_VERSION,DESCRIPTION)  
multi = gen.multi_amqp(MODULE_NAME) 
s = Shiny(MODULE_NAME)       # the magic mail parsing class

conf.configure([multi,s]) #set up parser and eval parsed stuff

# start network connections
amqp = multi.create_connection()
s.create_connection()
# main method
def cb (ch,method,header,body):
  log.debug ( "Header %r" % (header,))
  log.debug ( "Body %r" % (body,))
  try:
    entry = s.process(json.loads(body))
  except Exception as e:
    print 'Something just fuckin happened ' + str(e)
    raise e
for i in amqp:
  log.debug('registering new consumer ' +str(i.name))

  i.consume(cb,i.qname)
print "waiting for messages"
try:
  amqp[0].start_loop()
except:
  multi.close_connection() 
  s.close_connection()
