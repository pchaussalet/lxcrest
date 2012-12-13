from flask import Flask, request, redirect
from flask.ext import restful

from lxc4u.service import LXCService as lxc
import subwrap

app = Flask(__name__)
api = restful.Api(app)

class ContainerListResource(restful.Resource):
  def get(self):
    names = lxc.list_names()
    response = []
    for name in names:
      response.append({ 'name':   name,
                        'state':  lxc.info(name)['state']})
    return response

  def put(self):
    data = request.json
    name = data['name']
    template = data['template']
    try:
      lxc.create(name, template)
    except subwrap.CommandError, e:
      print e
    return redirect('/%s' % name)

class ContainerResource(restful.Resource):
  def get(self, name):
    return {'name':   name,
            'state':  lxc.info(name)['state']}

  def delete(self, name):
    lxc.destroy(name)
    return '', 204
    
class ContainerActionResource(restful.Resource):
  def post(self, name, action):
    if action == 'start':
      lxc.start(name)
    elif action == 'stop':
      lxc.stop(name)
    return '', 204

api.add_resource(ContainerListResource, '/')
api.add_resource(ContainerResource, '/<string:name>')
api.add_resource(ContainerActionResource, '/<string:name>/<string:action>')

if __name__ == '__main__':
  app.run(debug=True)
