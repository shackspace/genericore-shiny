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
amqp1 = gen.auto_amqp() 
amqp2 = gen.auto_amqp() 
s = mail_shiny()       # the magic mail parsing class

conf.configure([amqp1,amqp2,s]) #set up parser and eval parsed stuff

#TODO fix this thingy... 
amqp1.load_conf({'amqp' : {"in" : { "exchange" : "mail_stats"}}})
amqp2.load_conf({'amqp' : {"in" : { "exchange" : "snmp_src"}}})
# start network connections
s.create_connection()
amqp1.create_connection()
amqp2.create_connection()

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
  amqp1.close_connection()
  amqp2.close_connection()
  s.close_connection()
