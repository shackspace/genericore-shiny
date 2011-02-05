import pystache
dispatch=['backbone']
path='rabbithole'

def process(self):
  data = self.stats['backbone']

  if not data:
    return "No Backbone infos yet"
  stache = { 'infos' : [] }
  stache['timestamp'] = data['timestamp']
  del data['timestamp']
  for k,v in data.items():
    stache['infos'].append( { 'key' : k , 'value' : v.replace('\n','<br/>') } )

  data['timestamp'] = stache['timestamp']
  return pystache.render(self.templates['rabbithole'],stache)
