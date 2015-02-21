#!/usr/bin/python
'''
A basic bottle app skeleton
'''

import bottle

import imagelib

app = application = bottle.Bottle()

@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='{}/static'.format(conf.get('bottle', 'root_path')))

@app.route('/')
def show_index():
    '''
    The front "index" page
    '''
    return 'Helloes'

@app.route('/page/<page_name>')
def show_page(page_name):
    '''
    Return a page that has been rendered using a template
    '''
    return theme('page', name=page_name)

@app.route('/twitter', method='POST')
def createComic():
    arr = bottle.request.json['ids']
    imagelib.makeComic(arr)
    return bottle.static_file('comic.jpg', root='/home/azureuser/twitter-comics/results/', mimetype='image/jpeg')
    #return "Bye"

class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    bottle.run(app=StripPathMiddleware(app),
        host='0.0.0.0',
        port=8000)
