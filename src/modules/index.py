import pystache
dispatch = [] #Main page, do not react for anything
path ='index'
def process(self): 
  data = { }
  data['avail'] = [ { 'path' : d.path } for d in self.avail ]
  return pystache.render(self.templates['index'],data)


