import sqlite3 as sqlite
from flask import Flask, redirect, request
import random
import string

app = Flask(__name__)

@app.route("/")
def home():
	return {"data": "Welcome to fast.sh - URL Shortener"}

@app.route("/<i>")
def redirec(i):
	with sqlite.connect("main.db") as db:
		long_url = db.execute("SELECT long FROM URLs WHERE short=?", (i,))
		long_url = long_url.fetchone()
	print(long_url)
	if long_url:
		return redirect(long_url[0], code=301)
	else:
		return {"data": "Not Found"}

@app.route("/shorten")
def shorten():
	url = request.args.get("url")
	if url:
		with sqlite.connect("main.db") as db:
			data = db.execute("SELECT short FROM URLs WHERE long=?", (url,)).fetchone()
			if data:
				print(data)
				return {"url": f"http://localhost:5000/{data[0]}"}

	r = "".join([random.choice(string.ascii_letters) for _ in range(6)])
	inside = True
	while inside:
		with sqlite.connect("main.db") as db:
			if db.execute("SELECT long FROM URLs WHERE short=?", (r,)).fetchone():
				r = "".join([random.choice(string.ascii_letters) for _ in range(6)])
			else:
				inside = False


	if url:
		with sqlite.connect("main.db") as db:
			temp = db.execute("INSERT INTO URLs (short, long) VALUES (?, ?)", (r, url))
		return {"url": f"http://localhost:5000/{r}"}
	else:
		return {"data": "URL Missing"}

app.run(port=5000)