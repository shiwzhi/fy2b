from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
import subprocess
import requests
from time import sleep
import os
import json
import pickle
import base64
from urllib.parse import urlparse

## refer to it's hostname




fy2b_dir = os.path.abspath(os.path.dirname(__file__))
video_dir = fy2b_dir+'/videos'
player_templapte = "player.html"
host = 'https://swz1994.com'
host_url = host+'/fy2b/videos'



def download_video(input_vid):
	if os.path.isfile(video_dir+'/{}.lock'.format(input_vid)) == False:
		subprocess.call(["touch", video_dir+"/{}.lock".format(input_vid)])
		subprocess.Popen(["youtube-dl", '-f', 'bestvideo[height<=480]+bestaudio[ext=m4a]', "https://www.youtube.com/watch?v={}".format(input_vid), '-o', video_dir+'/%(id)s.mp4'])


class info(object):
	"""docstring for info"""
	def __init__(self, vid):
		super(info, self).__init__()
		info_file = video_dir+'/{}.info'.format(vid)
		if os.path.isfile(info_file) == False:
			vid_json = subprocess.check_output(['youtube-dl', '-j', "https://www.youtube.com/watch?v="+vid]).decode('utf-8', 'ignore')
			self.json = json.loads(vid_json)
			pickle.dump(self.json, open(info_file, 'wb'))
			print('info dumped')
		else:
			self.json = pickle.load(open(info_file, 'rb'))
			print('info loaded')
		self.title = self.json['title']
		self.description = self.json['description']
		self.like = self.json['like_count']
		self.dislike = self.json['dislike_count']
		self.views = self.json['view_count']
		self.vid = vid
		self.uploader = self.json['uploader']
		


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
@app.route("/fy2b/")
def default():
	return(redirect(host+"/fy2b/watch?v={}".format("dQw4w9WgXcQ")))


@app.route("/fy2b/index.php")
@app.route("/fy2b/watch")
def index():
	if request.method == "GET":
		vid = request.args.get('v')
		vid_info = info(vid)
		download_video(request.args.get('v'))
	return(render_template(player_templapte, info=vid_info))

@app.route("/fy2b/video")
@app.route("/fy2b/video/<v_id>")
def video(v_id='404'):
	video_url = "{}/{}.mp4".format(host_url, v_id)
	status = requests.head(video_url)
	if str(status.status_code)[0] != '2':
		sleep(1)
		return(redirect(request.url))
		# status = requests.head(status.headers["Location"])
	else:
		return(redirect(video_url))


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
