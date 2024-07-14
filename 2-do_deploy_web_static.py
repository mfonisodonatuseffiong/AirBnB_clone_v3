#!/usr/bin/python3
"""Compress web static package and deploy to servers
"""
from fabric.api import env, put, run
from datetime import datetime
from os import path


env.hosts = ['18.209.152.5', '100.25.46.59']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    if not path.exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract the timestamp from the archive filename
        timestamp = archive_path[-18:-4]

        # Create the release directory on the server
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress the archive to the release directory
        run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/web_static_{}/'
            .format(archive_path.split('/')[-1].split('.')[0], timestamp))

        # Remove the archive from the server
        run('sudo rm /tmp/{}.tgz'.format(archive_path.split('/')[-1].split('.')[0]))

        # Move the contents of the uncompressed archive to the release directory
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove the now empty web_static directory
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Remove the existing symbolic link to the current release
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

    # Return True if the deployment succeeded
    return True
