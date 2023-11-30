import os
import sys
import hashlib
import dotenv

def get_port(branch: str):
    return int.from_bytes(hashlib.sha256(branch.encode()).digest(), signed=False) % 50000 + 10000

branches = []
with open("/etc/nginx/branches", "r") as file:
    for branch in file.read().split("\n"):
        if branch != "":
            branches.append(branch)

new = sys.argv[1]
new_port = get_port(new)

if new not in branches:
    branches.append(new)

print(branches)

os.system("git submodule update --init --recursive")

os.system(f"docker stop hack4cure_{new}")
os.system(f"docker rm hack4cure_{new}")

os.system("cp /usr/local/share/hack4cure/.env .")
os.system(f"docker build -t hack4cure .")
os.system("docker run -d -p %s:7000 --name hack4cure_%s -e BRANCH=%s hack4cure" 
% (
    new_port, 
    new,
    new,
))

config = ""

for branch in branches:
    port = get_port(branch)

    config += ("""
        location ~ ^/hack4cure/%s/api/(.*)$ {
            rewrite ^/hack4cure/%s/api/(.*) /$1 break;
            proxy_pass http://127.0.0.1:%s;
        }
    """ % (branch, branch, port))

with open("/etc/nginx/nginx.conf", "w") as file:

    with open("/etc/nginx/nginx.conf.begin", "r") as begin:
        file.write(begin.read())

    file.write(config)

    with open("/etc/nginx/nginx.conf.end", "r") as end:
        file.write(end.read())

os.system("sudo /usr/sbin/nginx -s reload")

with open("/etc/nginx/branches", "w") as file:
    for branch in branches:
        file.write(branch + "\n")
