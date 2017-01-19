from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
import subprocess
import requests
from time import sleep
import os
import base64

fy2b_dir = "/var/www/flask_y2b"
vid_url = "https://swz1994.com/fy2b/videos"

def download_video(input_vid):
	if os.path.isfile(fy2b_dir+'/videos/{}.lock'.format(input_vid)) == False:
		subprocess.call(["touch", fy2b_dir+"/videos/{}.lock".format(input_vid)])
		subprocess.Popen(["youtube-dl", '-f', 'bestvideo[height<=480]+bestaudio[ext=m4a]', "www.youtube.com/watch?v={}".format(input_vid), '-o', fy2b_dir+'/videos/%(id)s.mp4'])


app = Flask(__name__)


if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@app.route("/d/<url>")
def downloader(url="https://www.baidu.com"):
	r = requests.get(base64.b64decode(url).decode("utf-8"))
	response = make_response(r.content)
	response.headers['Content-Type'] = 'application/x-bittorrent'
	response.headers['Content-Disposition'] = 'attachment; filename=1.torrent'
	return response


@app.route("/")
@app.route("/index.php")
@app.route("/watch")
def index():
	if request.method == "GET":
		download_video(request.args.get('v'))
	return(render_template("temp.html", vid = request.args.get('v')))

@app.route("/video/")
@app.route("/video")
@app.route("/video/<v_id>")
def video(v_id='404'):
	status = requests.head("http://swz1994.com/videos/{}.mp4".format(v_id))
	while str(status.status_code)[0] == '3':
		status = requests.head(status.headers["Location"])
	if str(status.status_code)[0] != '2':
		sleep(1)
		return(redirect(request.url))
	else:
		return(redirect("https://swz1994.com/videos/"+v_id+".mp4"))


if __name__ == "__main__":
    app.run()