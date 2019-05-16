import xmlrpc.client
from PIL import Image
from os import path
import os

def check_avatar(username):
    status = path.exists('../assets/avatar/%s.jpg' % username)
    if not status:
        server = xmlrpc.client.ServerProxy('http://120.77.38.66:8015')
        with open('../assets/avatar/%s.jpg' % username, 'wb') as f:
            f.write(server.get_avatar(username).data)
            f.close()


def img_valid(img_path):
    valid = True
    try:
        Image.open(img_path).verify()
    except:
        valid = False
    return valid


def transform_jpg(img_path):
    if img_valid(img_path):
        string = img_path.rsplit(".", 1)
        out_path = string[0] + ".jpg"
        img = Image.open(img_path)
        try:
            if len(img.split()) == 4:
                r, g, b, a = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.convert('RGB').save(out_path, quality=70)
                os.remove(img_path)
            else:
                img.convert('RGB').save(out_path, quality=70)
                os.remove(img_path)
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Image is invalid.")
        return False
