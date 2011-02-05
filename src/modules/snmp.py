import pystache
dispatch= ['snmp']
path='snmp'
def process(self):
  data = self.stats['snmp']

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

