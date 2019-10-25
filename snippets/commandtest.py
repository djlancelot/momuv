import subprocess
import time
import socket

"https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html"
host = "localhost"
port = 8888
cmd = '"c:\\Program Files (x86)\\VideoLAN\VLC\\vlc.exe" -I rc --rc-host {}:{} --play-and-pause d:\\Videok\\vagott.mpg'.format(host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
sock.connect((host, port))
time.sleep(5)
print("sending")
#p.stdin.write("seek 0")
sock.sendall("pause".encode())
time.sleep(5)
out, err = p.communicate("seek 0".encode())