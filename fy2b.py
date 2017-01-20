from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
import subprocess
import requests
from time import sleep
import os
import json
import base64

fy2b_dir = "/root/fy2b"
vid_url = "https://swz1994.com/fy2b/videos/"

player_templapte = "player.html"

def download_video(input_vid):
	if os.path.isfile(fy2b_dir+'/videos/{}.lock'.format(input_vid)) == False:
		subprocess.call(["touch", fy2b_dir+"/videos/{}.lock".format(input_vid)])
		subprocess.Popen(["youtube-dl", '-f', 'bestvideo[height<=480]+bestaudio[ext=m4a]', "https://www.youtube.com/watch?v={}".format(input_vid), '-o', fy2b_dir+'/videos/%(id)s.mp4'])

def get_info(parameter, vid):
	output = subprocess.check_output(['youtube-dl', parameter, vid])
	return output.decode('utf-8', "ignore")

class info(object):
	"""docstring for info"""
	def __init__(self, vid):
		super(info, self).__init__()
		self.json = json.loads(subprocess.check_output(['youtube-dl', '-j', vid]).decode('utf-8', 'ignore'))
		self.title = json['title']
		self.description = json['description']
		self.like = json['like_count']
		self.dislike = json['dislike_count']
		self.views = json['view_count']
		


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
		vid = request.args.get('v')
		vid_info = info(vid)
		download_video(request.args.get('v'))
	return(render_template(player_templapte, 
		vid = request.args.get('v'), 
		title = vid_info.title, 
		description = vid_info.description,
		like = vid_info.like,
		dislike = vid_info.dislike,
		views = vid_info.views))

@app.route("/video")
@app.route("/video/<v_id>")
def video(v_id='404'):
	vid_file_url = vid_url+vid_url+".mp4"
	status = requests.head(vid_file_url)
	if str(status.status_code)[0] != '2':
		return(redirect(request.url))
		# status = requests.head(status.headers["Location"])
	else:
		return(redirect(request.url))


if __name__ == "__main__":
    app.run(host='0.0.0.0')