import base64
import sys

import bcrypt

if __name__ == "__main__":
    with open(".SECRET_KEY") as k:
        salt = base64.b64decode(k.read())

    if sys.argv[1] == "mkpasswd":
        print(base64.b64encode(bcrypt.hashpw(sys.argv[2].encode(), salt)))
