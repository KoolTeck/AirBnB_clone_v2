#!/usr/bin/python3
""" generates a .tgz achive """
from fabric.api import local
from datetime import datetime


def do_pack():
    """ generates a .tgz achive of web_static folder
       returns the file on succes or None
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path_name = "versions/web_static_{}.tgz".format(date)
    tgz_path = local("tar -cvzf {} web_static".format(archive_path_name))
    if tgz_path.succeeded:
        return tgz_path
    else:
        return None
