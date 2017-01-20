import subprocess
import json

output = subprocess.check_output(['youtube-dl', '-j', 'WWPMNm5Zh4U', '--proxy=socks5://127.0.0.1']).decode('utf-8', 'ignore')

j = json.loads(output)
print(j['like_count'])

