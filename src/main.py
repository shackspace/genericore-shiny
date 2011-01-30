#!/usr/bin/env python2
import sys,json
from mail_shiny import mail_shiny
import logging
import genericore as gen
log = logging.getLogger('mail_shiny')
PROTO_VERSION = 1
DESCRIPTION = 'Makes Statistics shiny'

# set up instances of needed modules

conf = gen.Configurator(PROTO_VERSION,DESCRIPTION)  
multi = gen.multi_amqp() 
s = mail_shiny()       # the magic mail parsing class

conf.configure([multi,s]) #set up parser and eval parsed stuff

# start network connections
amqp1,amqp2 = multi.create_connection()
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

amqp1.consume(cb)
amqp2.consume(cb)
print "waiting for messages"
try:
  amqp1.start_loop()
except:
  multi.close_connection() 
  s.close_connection()
