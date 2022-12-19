from os.path import join
from secrets import token_urlsafe

import requests
from bleach import clean
from flask import Flask, render_template, redirect, abort, request, send_from_directory

app = Flask(__name__)
app.secret_key = token_urlsafe(32)


@app.route("/")
def index():
    return render_template("index.html", index=True)


@app.route("/create", methods=["POST"])
def create():
    form = request.form
    content = clean(form["log"])
    r = requests.post("https://hastebin.blankdvth.com/documents", data=content.encode("utf-8"))
    if not r.ok:
        abort(500)
    return redirect(f"/{r.json()['key']}")


@app.route("/<hastebin_slug>")
def view(hastebin_slug):
    if "." in hastebin_slug:
        hastebin_slug = hastebin_slug[:hastebin_slug.index(".")]
    content = clean(requests.get("https://hastebin.blankdvth.com/raw/" + hastebin_slug).text)


@app.route("/<hastebin_slug>/simple")
def view_simple(hastebin_slug):
    if "." in hastebin_slug:
        hastebin_slug = hastebin_slug[:hastebin_slug.index(".")]
    content = clean(requests.get("https://hastebin.blankdvth.com/raw/" + hastebin_slug).text)


@app.route("/<hastebin_slug>/analysis")
def analysis(hastebin_slug):
    if "." in hastebin_slug:
        hastebin_slug = hastebin_slug[:hastebin_slug.index(".")]
    content = clean(requests.get("https://hastebin.blankdvth.com/raw/" + hastebin_slug).text)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon")


if __name__ == "__main__":
    app.run(debug=True)
