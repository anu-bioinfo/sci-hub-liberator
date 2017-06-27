import requests
import requests_toolbelt.adapters.appengine
from flask import Flask
from flask import request
from flask import send_file
from google.appengine.api import urlfetch

requests_toolbelt.adapters.appengine.monkeypatch()

urlfetch.set_default_fetch_deadline(60)

app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = 'some_long_random_string'

BACKEND_IP_ADDRESS = 'IP ADDRESS OF YOUR BACKEND'

html = '''
<!DOCTYPE HTML>
<html>
<head>
    <title>Sci-Hub Liberator</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
</head>
<style>
    div#loading {
        width: 70px;
        height: 70px;
        display: none;
        background: url(/static/loading.gif) no-repeat;
        cursor: wait;
        }
</style>
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
<script type="text/javascript">// <![CDATA[
        function loading(){
            $("#loading").show();
            $("#content").hide();       
        }
// ]]></script>
<body>
    <div class="w3-container w3-teal">
        <h2>Sci-Hub Liberator</h2>
    </div>
    <form class="w3-container w3-display-middle" method="POST" action="/generate">
        <div id="loading"></div>
        <div id="content">
            <label class="w3-text-teal"><b>enter URL, PMID/DOI or search string:</b></label>
            <input class="w3-input w3-border w3-light-grey" type="text" size="100" name="gatedurl">
            <br>
            <br>
            <button class="w3-btn w3-blue-grey" onclick="loading();">ungate the paper!</button>
        </div>
    </form>
    <div class="w3-display-bottomright w3-padding-large">
        created by <a href="http://thiagomarzagao.com/about">Thiago Marzagao</a>
    </div>
</body>
</html>
'''

@app.route('/', methods = ['GET'])
def index():
    return html

@app.route('/generate', methods = ['POST'])
def generate():
    gated_url = request.form['gatedurl']
    api_response = requests.get('http://BACKEND_IP_ADDRESS/get_paper_id?pattern=' + gated_url)
    paper_id = api_response.text
    paper_link = 'http://BACKEND_IP_ADDRESS/download/static/paper{}.pdf'.format(paper_id)
    return paper_link
