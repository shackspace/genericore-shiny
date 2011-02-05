import pystache
dispatch = ['irc']
path ='irc'
def process(self): 
  return pystache.render(self.templates['irc'],self.stats['irc'])
