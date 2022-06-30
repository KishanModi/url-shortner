from flask import Flask, request, redirect, render_template,url_for
import string,random
import pymongo
app = Flask(__name__)
import time


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient = pymongo.MongoClient("")

mydb = myclient["n"]
mycol = mydb["urls"]

#home page
@app.route('/')
def home():
	return render_template('index.html')

#generate shortened url
@app.route('/',methods=['POST'])
def generate_url():
	url = request.form.get('url')

	dayago = time.time() - 86400
	print(dayago)
	mycol.delete_many({"timestamp": {"$lt": dayago}})
	checkurl = mycol.find({'url':url})
	results = list(checkurl)
	if len(results) == 0:
		shorturl = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
		mycol.insert_one({'url':url,'shorturl':shorturl, "timestamp": time.time()})
		url = mycol.find_one({'url':url})
		print(url['url'])
		url=url['url']
		shorturl = 'http://localhost:5000/'+shorturl
		return render_template('index.html',shorturl=shorturl,url=url)
	url = mycol.find_one({'url':url})
	shorturl=url['shorturl']
	url=url['url']
	print(url)
	shorturl = 'http://localhost:5000/'+shorturl
	return render_template('index.html',url=url,shorturl=shorturl)

# redirect to original url
@app.route('/<shorturl>')
def redirect_url(shorturl):
	url = mycol.find_one({"shorturl":shorturl})
	url=url['url']
	if url.find("http://") != 0 and url.find("https://") != 0:
		url = "http://" + url
	return redirect(url)

if __name__ == '__main__':
	app.run(debug=True)
