import base64
import sys

import bcrypt

if __name__ == "__main__":
    if sys.argv[1] == "mkpasswd":
        with open(".SECRET_KEY") as k:
            salt = base64.b64decode(k.read())
            print(base64.b64encode(bcrypt.hashpw(sys.argv[2].encode(), salt)))
    
    if sys.argv[1] == "mksalt":
        with open(".SECRET_KEY", "w") as f:
            f.write(str(base64.b64encode(bcrypt.gensalt()))[2:-1])
