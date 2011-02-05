""" template file is always modulename.mustache """
import pystache

dispatch = ['mail'] #dispatch for the following messages
path = 'mail'

def process(self):
  if not self.stats['mail']:
    return "No Mail Statistics received yet!"
  return pystache.render(self.template['mail'],self.stats['mail'])
