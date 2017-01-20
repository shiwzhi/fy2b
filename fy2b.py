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
		self.j = json.loads(subprocess.check_output(['youtube-dl', '-j', vid]).decode('utf-8', 'ignore'))
		self.title = self.j['title']
		self.description = self.j['description']
		self.like = self.j['like_count']
		self.dislike = self.j['dislike_count']
		self.views = self.j['view_count']
		


app = Flask(__name__)


if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@app.route("/fy2b/d/<url>")
def downloader(url="https://www.baidu.com"):
	r = requests.get(base64.b64decode(url).decode("utf-8"))
	response = make_response(r.content)
	response.headers['Content-Type'] = 'application/x-bittorrent'
	response.headers['Content-Disposition'] = 'attachment; filename=1.torrent'
	return response


@app.route("/fy2b")
@app.route("/fy2b/index.php")
@app.route("/fy2b/watch")
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

@app.route("/fy2b/video")
@app.route("/fy2b/video/<v_id>")
def video(v_id='404'):
	vid_file_url = vid_url+vid_url+".mp4"
	status = requests.head(vid_file_url)
	if str(status.status_code)[0] != '2':
		sleep(1)
		return(redirect(request.url))
		# status = requests.head(status.headers["Location"])
	else:
		return(redirect(vid_file_url))


if __name__ == "__main__":
    app.run(host='0.0.0.0')