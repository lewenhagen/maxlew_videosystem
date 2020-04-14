#!/usr/bin/env python3

"""
A set of helper functions
"""

from videocamera import VideoCamera
import os
import json

def init_list_of_new_cameras(config):
    """ Initiate the cameras """
    result = {}

    for cam in config:
        result[cam[0]] = VideoCamera(cam)

    return result



def get_single_cam(data):
    """ Returns a single camera """
    return data["cameras"][data["mapping"][data["single"]]]


def get_all_cams(data, user_setup):
    """ Returns four cameras """

    return [
        VideoCamera(user_setup[0], "640x360"),
        VideoCamera(user_setup[1], "640x360"),
        VideoCamera(user_setup[2], "640x360"),
        VideoCamera(user_setup[3], "640x360")
    ]


def get_dual_cams(data):
    """ Returns the chosen dual cams, based on number """
    return [data["cameras"][data["mapping"][data["dual"][0]]], data["cameras"][data["mapping"][data["dual"][1]]]]

def set_quad_cam(data, user_setup):
    """ Sets the chosen camera as quad cam with lower resolution """
    result = []

    for _ in range(4):
        quad = VideoCamera(user_setup[data["single"]], "640x360")
        result.append(quad)

    return result

def get_ips_from_file():
    filename = "script/ips.txt"
    lines = []
    with open(filename) as filehandle:
        lines = filehandle.read().splitlines()

    return lines


def get_config_from_file():
    filename = "script/user_config.txt"
    message = ""
    lines = []
    if not os.path.exists(filename):
        os.mknod(filename)

    with open(filename) as filehandle:
        lines = filehandle.read().splitlines()

    if len(lines) < 1:
        message = "No config yet, but the file is there."
    else:
        message = "\n".join(lines)

    return message

# def run_ip_check(search):
#     from subprocess import call
#     call(["script/maxlew.sh", "init", search])
#     return "Done. Press - to get back to the admin menu."
def get_subnet():
    import subprocess

    process = os.popen("echo $(hostname -I | cut -d'.' -f1-3)")
    sn = process.read()
    process.close()
    return sn.strip()

def pingwithip(ipaddress):
    online = False

    process = os.popen("ping -c 1 -w2 {} > /dev/null; echo $?".format(ipaddress))
    response = process.read().strip()

    process.close()

    if response == "0":
        online = True

    return online

def insert_ip(ipadress):
    filename = "script/ips.txt"
    lines = []
    message = "No address added."

    with open(filename) as filehandle:
        lines = filehandle.read().splitlines()

    lines.append(ipadress)

    with open(filename, "w") as filehandle:
        filehandle.write("\n".join(lines))

    message = "Address: {} inserted.".format(ipadress)

    return message

def remove_ip(ipaddress):
    filename = "script/ips.txt"
    lines = []
    message = "No address removed."
    temp = ""

    if ipaddress != "":
        with open(filename) as filehandle:
            lines = filehandle.read().splitlines()

        temp = lines[ipaddress-1]
        del lines[ipaddress-1]

        with open(filename, "w") as filehandle:
            filehandle.write("\n".join(lines))

        message = "Address: {} removed.".format(temp)

    return message

def generate_user_config(form):
    ips = get_ips_from_file()

    result = []
    for index, ip in enumerate(ips):
        result.append([form["name_" + str(index+1)], "http://" + ip])

    filename = "script/user_config.txt"
    with open(filename, "w") as outfile:
        json.dump(result, outfile)

    return result

def read_user_config():
    configpath = "script/user_config.txt"
    if os.path.exists(configpath) and os.path.getsize(configpath) > 0:
        with open(configpath) as json_file:
            user_setup = json.load(json_file)
    else:
        return False
    return user_setup

def delete_config():
    configpath = "script/user_config.txt"
    message = "File: {} removed.".format(configpath)
    if os.path.exists(configpath):
        os.remove(configpath)
    else:
        message = "The file {} does not exist!".format(configpath)

    return message
