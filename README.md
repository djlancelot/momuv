# Motion-triggered Multi-VLC player

This app can open multiple VLC players and start different videos all in sync, 
triggered by motion on the selected web camera.

It can be used to start Halloween or Holiday projections.

## Usage
```shell
λ python players.py --help
Usage: players.py [OPTIONS]

  Motion triggered Multi-VLC player

  This is a simple application to play a single or multiple videos using VLC
  player. The videos can be moved to different screens and can be part of a
  distributed, synchronized animation.

  It can be used for motion-triggered Halloween or holiday projections.

  VLC has to be installed separately and the path to the VLC executable
  needs to be passed as parameter.
  
  Press ESC to stop the main loop.

Options:
  -i, --input TEXT           Video file to play. Can be repeated more than
                             once.  [required]
  -r, --renderer TEXT        Video render parameter passed to VLC player.
  -p, --port INTEGER         Starting port number. Port numbers are assigned
                             sequentially.
  -v, --vlc TEXT             Path to VLC executable.  [required]
  -s, --stop INTEGER         Stop and wait for motion after this many seconds.
                             [required]
  -c, --camera INTEGER       Camera ID to use.
  -s, --sensitivity INTEGER  Camera sensitivity for motion alert. The higher
                             the number the more sensitive the app,
  --help                     Show this message and exit.
```

## Architecture

The app spawns subprocesses for each VLC player started per each input file. 
The subprocesses are controlled using the VLC telnet interface. 
To avoid rendering errors the animation pauses after STOP seconds instead of stopping at the end of the file.
After the pause it looks for changes on the webcamera image and restarts the animation if the movement is
 bigger than the set SENSITIVITY.
 
## Requirements

- VLC needs to be installed on the computer so that the app can start it up.
- Runs on Python 3.7.
- OpenCV python is used to read the web camera image for the motion trigger.
- Frame differences are partially calculated using `numpy`.
- Command parameters are parsed with `click`.
All python dependencies are listed in the `requirements.txt` file.

## Acknowledgments

The app was inspired by a great blog post called [Marios Zindilis: Control VLC with Python](https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html)
 
 