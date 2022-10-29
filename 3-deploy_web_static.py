#!/usr/bin/python3
""" generates a .tgz achive """
from fabric.api import local, run, put, env
from datetime import datetime
import os.path

env.hosts = ['3.239.2.4', '54.146.87.101']


def do_pack():
    """ generates a .tgz achive of web_static folder
       returns the file on succes or None
    """
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path_name = "versions/web_static_{}.tgz".format(date)
    tgz_path = local("tar -cvzf {} web_static".format(archive_path_name))
    print("Archive created at => {}".format(archive_path_name))
    if tgz_path.succeeded:
        return archive_path_name
    else:
        return None


def do_deploy(archive_path):
    """
    distributes an archive to the servers
    """
    if os.path.isfile(archive_path) is False:
        return False
    else:
        upload = put(archive_path, '/tmp')
        stripped_path = archive_path.strip('.tgz')
        run1 = run("sudo mkdir -p \
        /data/web_static/releases/{}".format(stripped_path))
        run2 = run("sudo tar xzf /tmp/{} -C \
        /data/web_static/releases/{}".format(
            archive_path.strip("versions/"), stripped_path)
        )
        run3 = run("sudo rm /tmp/{}".format(archive_path.strip("versions/")))
        run4 = run("sudo mv /data/web_static/releases/{}/web_static/* "
                   "/data/web_static/releases/{}/".format(
                       stripped_path, stripped_path
                   ))
        run5 = run("sudo rm -rf /data/web_static/releases/{}/web_static".
                   format(stripped_path))
        run6 = run("sudo rm -rf /data/web_static/current")
        run7 = run("sudo ln -s /data/web_static/releases/{}/ \
        /data/web_static/current".format(
            stripped_path)
        )
    if 'False' in [
            upload.succeeded,
            run1.succeeded,
            run2.succeeded,
            run3.succeeded,
            run4.succeeded,
            run5.succeeded,
            run6.succeeded,
            run7.succeeded
    ]:
        return False
    print("new version deployed")
    return True


def deploy():
    """
        creates an archive of the web_static folder and distribute it to server
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    status = do_deploy(archive_path)
    return status
