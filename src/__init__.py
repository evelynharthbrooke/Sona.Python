import subprocess

VERSION = "0.1.0"
GIT_SHA = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf8')
