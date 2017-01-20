import subprocess


output = subprocess.check_output(['youtube-dl', '--get-description', 'WWPMNm5Zh4U', '--proxy=socks5://127.0.0.1'])

print(output.decode('utf-8', "ignore"))

