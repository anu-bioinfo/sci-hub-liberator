import cherrypy
import requests
from bs4 import BeautifulSoup
from random import randint
from cherrypy.lib.static import serve_file

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 8080

class api(object):

    @cherrypy.expose
    def get_paper_id(self, pattern):
        '''
        receives url to gated paper
        delivers id of the paper
        '''
        scihub_html = requests.post(
            'http://sci-hub.cc/', 
            data = {'request': pattern},
            headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'}
            )
        soup = BeautifulSoup(scihub_html.text)
        url_to_pdf = 'http:' + soup.find_all('iframe')[0].get('src')
        scihub_bytes = requests.get(url_to_pdf)
        paper_id = str(randint(0,60000000))
        with open('static/paper{}.pdf'.format(paper_id), mode = 'wb') as fbuffer:
            fbuffer.write(scihub_bytes.text)
        return paper_id

    @cherrypy.expose
    def download(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")

cherrypy.quickstart(api())
