#!/usr/bin/env python3

from videocamera import VideoCamera

def init_list_of_new_cameras(options):
    result = {}

    for cam in options:
        result[cam[0]] = VideoCamera(cam)

    return result

def get_single_cam(data):
    return data["cameras"][data["mapping"][data["single"]]]

def get_delayed_cam(data, index):
    return data["delayed"][index]

def get_dual_cams(data):
    return (data["cameras"][data["mapping"][data["dual"][0]]], data["cameras"][data["mapping"][data["dual"][1]]])

def set_quad_cam(data, user_setup):
    result = []

    for _ in range(4):
        quad = VideoCamera(user_setup[data["single"]], "640x360")
        result.append(quad)

    return result
