Shiny Web Frontend Module
=======================

The shiny module is a simple module which provides a way to visualize data
with the help of a few lines of python code and a template if you want.

Example
======
A shiny submodule normally contains 2 parts:
1. The template (e.g. Mustache) in _templates/example.mustache_
<html><head><title>Example Submodule</title></head>
<body>{{NAME}}
{{#list}}
{{listitem}}<br/>
{{/list}}
</body></html>
2. The python module in _src/modules/example.py_
    import pystache
    dispatch=['sample_type'] #type of message you want to receive
    path='example'           #the path on the webserver (http://localhost/example)
    #template_name='' # if you want other extraordinary templates
    def process(self): # self is the shiny class (see code for all cool stuff it has)
      # you can do all the weird stuff you want, return what the user should
      # see at the end
      return pystache.render(self.templates['example'],self.stats['example'])

After you dropped these two files you are already finished.
If you want other exchanges to listen on, add them to _conf/config.json_
(this is important because otherwise the exchange won't be polled for data)
