import subprocess

version = "0.0.1"
hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip().decode("utf8")
