#!/usr/bin/env python3

"""
A set of helper functions
"""

from videocamera import VideoCamera

def init_list_of_new_cameras(options):
    """ Initiate the cameras """
    result = {}

    for cam in options:
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
