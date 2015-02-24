import csv
from urllib2 import urlopen
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import dateutil.parser as parser
import cherrypy
import os.path


class Test(object):
  @cherrypy.expose
  def index(self):
    return """<!DOCTYPE html>
<html>
<head>
	<h2 align="center">Historical data for NASDAQ symbol from the Google Fianance API</h2>
	
	<style>
html {
	background: url('http://subtlepatterns.com/patterns/wood_pattern.png');
	font-size: 10pt;
}
label {
	display: block;
	color: #999;
}
.cf:before,
.cf:after {
    content: ""; 
    display: table;
}

.cf:after {
    clear: both;
}
.cf {
    *zoom: 1;
}
:focus {
	outline: 0;
}
.loginform {
	width: 410px;
	margin: 50px auto;
	padding: 25px;
	background-color: rgba(250,250,250,0.5);
	border-radius: 5px;
    box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.2), 
    			inset 0px 1px 0px 0px rgba(250, 250, 250, 0.5);
    border: 1px solid rgba(0, 0, 0, 0.3);
}
.loginform ul {
	padding: 0;
	margin: 0;
}
.loginform li {
	display: inline;
	float: left;
}
.loginform input:not([type=submit]) {
	padding: 5px;
	margin-right: 10px;
	border: 1px solid rgba(0, 0, 0, 0.3);
	border-radius: 3px;
	box-shadow: inset 0px 1px 3px 0px rgba(0, 0, 0, 0.1), 
				0px 1px 0px 0px rgba(250, 250, 250, 0.5) ;
}
.loginform button[type=submit] {
	border: 1px solid rgba(0, 0, 0, 0.3);
	background: #64c8ef; /* Old browsers */
	background: -moz-linear-gradient(top,  #64c8ef 0%, #00a2e2 100%); /* FF3.6+ */
	background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#64c8ef), color-stop(100%,#00a2e2)); /* Chrome,Safari4+ */
	background: -webkit-linear-gradient(top,  #64c8ef 0%,#00a2e2 100%); /* Chrome10+,Safari5.1+ */
	background: -o-linear-gradient(top,  #64c8ef 0%,#00a2e2 100%); /* Opera 11.10+ */
	background: -ms-linear-gradient(top,  #64c8ef 0%,#00a2e2 100%); /* IE10+ */
	background: linear-gradient(to bottom,  #64c8ef 0%,#00a2e2 100%); /* W3C */
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#64c8ef', endColorstr='#00a2e2',GradientType=0 ); /* IE6-9 */
	color: #fff;
	padding: 5px 15px;
	margin-right: 0;
	margin-top: 15px;
	border-radius: 3px;
	text-shadow: 1px 1px 0px rgba(0, 0, 0, 0.3);
}
</style>
</head>
<body>
	<section class="loginform cf">
		<form name="login" method="get" action="generate" accept-charset="utf-8">
			<ul>
				<li>
					<label for="symbol">Enter a Symbol(AAPL,AAIT,AAME,AAOI,AAON etc..)</label>
					<input type="text" value="AAPL" name="symbol"  required>
				</li>
				
				<li>
					<button type="submit">Submit!</button>
				</li>
			</ul>
		</form>
	</section>
</body>
</html>"""

  @cherrypy.expose
  def generate(self, symbol='AAPL'):
    url = "http://www.google.com/finance/historical?q=NASDAQ:%s&authuser=0&output=csv"%symbol
    response = urlopen(url)
    data = []
    date = []
    close = []
    cr = csv.reader(response)
    for i in cr:
      data.append(i)
    date = []
    close = []
    for j in data:
	date.append(j[0])
	close.append(j[4])
    new = []
    for i in date[1:]:
	new.append(parser.parse(i))
    fig = plt.figure()
    plt.xlabel("Date")
    plt.ylabel("Close")
    plt.title(" Historical data for %s from the Google Fianance API"%symbol)
    plt.plot(new,close[1:])
    fig.autofmt_xdate()
    plt.show()

serverconfigfile = os.path.join(os.path.dirname(__file__), 'server.config')
approot=Test()
cherrypy.config.update("server.config") 
cherrypy.tree.mount(approot,'/')
cherrypy.quickstart(Test()) 
cherrypy.engine.start() 

