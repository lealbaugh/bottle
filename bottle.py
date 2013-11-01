from flask import *
from urlparse import *
import re

app = Flask(__name__)

database={}
mostrecent = ""
filename = "db.text"

@app.route('/', methods=['GET'])
def index():
	return render_template("shortener.html", database=database, mostrecent=mostrecent)

@app.route('/', methods=['POST'])
def handle_form():
	if request.form.get('shortURL', None):
		return redirect(request.form.get('shortURL'))
	else:
		newURL = request.form.get('URL', 'http://www.google.com') 
		newURL = cleanse(newURL)
		shortened = shortify(newURL)
		database[shortened] = newURL
		with open(filename, 'a') as f:
			f.write(shortened+"|"+newURL+"\n")
			f.close()
		mostrecent = shortened
		return render_template("shortener.html", database=database, mostrecent=mostrecent)

def shortify(URL):
	shortened = URL[7:]
	shortened = re.sub('[aeiou\W]', '', shortened)
	return shortened

def cleanse(URL):
	URLcomponents = urlparse(URL)
	if not URLcomponents.scheme:
		URL = "http://"+URL
	return URL

@app.route('/<shortened>')
def redirect_to_longer(shortened):
	if database.get(shortened) is not None:
		return redirect(database[shortened])
	else:
		return "Sorry, we don't seem to have that one yet."

def initDataBase(filename):
	with open(filename, 'r') as f:
		for line in f:
			data = line.split("|")
			database[data[0]] = data[1]
		f.close()

if __name__ == "__main__":
	initDataBase(filename)
	app.run(debug=True)

