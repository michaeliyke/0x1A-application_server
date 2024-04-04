#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, run, put
from pathlib import Path

env.user = "ubuntu"
env.hosts = ["18.204.16.105", "18.234.145.122"]


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    path = Path(archive_path)
    # env.hosts = ["18.234.145.122"]
    # Local file archive_path doesn't exist, return false
    if not path.exists():
        return False

    # upload to the temp dir of each server
    put(archive_path, "/tmp")
    # uncompress to /data/web_static/releases/archive_name
    run("sudo mkdir -p /data/web_static/releases/{}".format(path.stem))
    run("sudo rm -rf /data/web_static/releases/{}/*".format(path.stem))
    run("sudo tar -xzf /tmp/{}  -C /data/web_static/releases/{}"
        .format(path.name, path.stem))
    run("sudo mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}".format(path.stem, path.stem))
    run("sudo rmdir /data/web_static/releases/{}/web_static".format(path.stem))
    # delete archive from /tmp/
    run("sudo rm /tmp/{}".format(path.name))
    # recreate the symlink /data/web_static/current and point to archive_name
    run("sudo rm -f /data/web_static/current")
    run("sudo ln -s /data/web_static/releases/{}  /data/web_static/current"
        .format(path.stem))
    return True
