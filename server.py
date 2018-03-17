from webob import Request
from jinja2 import Environment, FileSystemLoader

class WsgiTopBottomMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            includes = [
                'app.js',
                'react.js',
                'leaflet.js',
                'D3.js',
                'moment.js',
                'math.js',
                'main.css',
                'bootstrap.css',
                'normalize.css',
            ]

            cssfiles = []
            jsfiles = []

            for include in includes:
                if(include.split('.')[1] == 'css'):
                    cssfiles.append(include)
                else:
                    jsfiles.append(include)

            response = self.app(environ, start_response)
            yield response.render(links = cssfiles, scripts = jsfiles).encode()  # str to bytes
        except:
            response_code = '404 Not Found'
            response_type = ('Content-Type', 'text/HTML')
            start_response(response_code, [response_type])
            yield ("404 Not Found").encode()

def app(environ, start_response):
    path = environ.get('PATH_INFO', '')

    #делаем страницу index.html главной
    if path == "/":
        path = "index.html"
    else:
        path = path[1:]

    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(path)
    return template

app = WsgiTopBottomMiddleware(app)
req = Request.blank('/')
print(req.get_response(app))
