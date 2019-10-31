__author__ = 'Lacika'
"""Inspired by https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html"""

import socket
import subprocess
import time
from enum import Enum
import cv2
import click
import numpy as np


class Status(Enum):
    paused = 0
    playing = 1


class VLC:
    def __init__(self, cmd, port=8888, renderer="opengl"):
        self.HOST = 'localhost'
        self.PORT = port

        cmd = '"{}" -I rc --vout {} --rc-host {}:{}'.format(
            cmd, renderer, self.HOST, self.PORT)
        self.PROC = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True)

        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCK.connect((self.HOST, self.PORT))

    def x(self, cmd):
        '''Prepare a command and send it to VLC'''
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)

    def pause(self):
        self.x('pause')

    def play(self):
        self.x('play')

    def stop(self):
        self.x('stop')

    def prev(self):
        self.x('prev')

    def next(self):
        self.x('next')

    def add(self, path):
        self.x('add %s\n'  % (path,))

    def enqueue(self, path):
        self.x('enqueue %s' % (path,))

    def clear(self):
        self.x('clear')

    def shutdown(self):
        self.x('shutdown')

    def seek(self, sec):
        self.x('seek %s' % (sec,))

    def __del__(self):
        if self.PROC:
            self.PROC.kill()


class VLCContainer:
    def __init__(self, infiles, cmd, renderer="opengl", start_port=8888):
        self.video_cnt = len(infiles)
        self.players = [VLC(cmd, port, renderer) for port in range(start_port, start_port + self.video_cnt)]
        for i in range(self.video_cnt):
            self.players[i].add(infiles[i])
        time.sleep(0.1)
        self.seek_zero()
        self.pause()

    def seek_zero(self):
        for player in self.players:
            player.seek(0)
        time.sleep(0.01)

    def pause(self):
        for player in self.players:
            player.pause()
        time.sleep(0.01)

@click.command()
@click.option('-i', '--input', 'infiles', required=True, multiple=True, help='Video file to play. Can be repeated more than once.')
@click.option('-r', '--renderer', default="opengl", help='Video render parameter passed to VLC player.')
@click.option('-p', '--port', default=8888, type=int, help='Starting port number. Port numbers are assigned sequentially.')
@click.option('-v', '--vlc', required=True,  help='Path to VLC executable.')
@click.option('-s', '--stop', 'max_play', required=True, type=int,  help='Stop and wait for motion after this many seconds.')
@click.option('-c', '--camera', default=0, type=int, help='Camera ID to use.')
@click.option('-s', '--sensitivity', default=100000, type=int, help='Camera sensitivity for motion alert. The higher the number the more sensitive the app,')
def player(infiles, renderer, port, vlc, max_play, camera, sensitivity):
    """Motion triggered Multi-VLC player

    This is a simple application to play a single or multiple videos using
    VLC player. The videos can be moved to different screens and can be part
    of a distributed, synchronized animation.

    It can be used for motion-triggered Halloween or holiday projections.

    VLC has to be installed separately and the path to the VLC executable needs to be passed
    as parameter.

    Press ESC to stop the main loop.

    """
    container = VLCContainer(infiles, vlc, renderer, start_port=port)
    cap = cv2.VideoCapture(camera)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    status = Status.paused
    old_frame = None
    start_time = time.time()
    frame_time = time.time()
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        if old_frame is None:
            old_frame = frame
        frameDelta = cv2.absdiff(frame, old_frame)
        #cv2.imshow('Input', frameDelta)
        if time.time() - frame_time > 1:
            if status == Status.paused:
                movement = np.sum(frameDelta)
                print(movement)
                if movement > sensitivity:
                    print("Movement, start")
                    container.pause()
                    container.seek_zero()
                    play_time = time.time()
                    status = Status.playing
            frame_time = time.time()
            old_frame = frame
        c = cv2.waitKey(1)
        if status == Status.playing:
            if (time.time() - play_time) > max_play:
                container.pause()
                status = Status.paused

        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    player()
