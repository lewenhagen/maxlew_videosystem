#!/usr/bin/env python3

"""
MAXLEW Video System
Version 1.0
"""

from flask import Flask, render_template, make_response, Response, redirect, url_for, request
import functions
import gc
import json
import os
import math
import random

# User defined options
# ["<name>", <ipadress>]
# user_setup = [
#     ["Volt", "http://192.168.1.133"],
#     ["Kullerbytta", "http://192.168.1.158"]
# ]
# with open('script/user_config.txt') as json_file:
#     user_setup = json.load(json_file)
user_setup = functions.read_user_config()
# Supervariable, going to hold all values
data = {}
# data["cameras"] = functions.init_list_of_new_cameras(user_setup)
if user_setup:
    # for item in user_setup:
    #     if functions.pingwithip(item[1]):
    #         data["mapping"] = [item[0]]

    data["mapping"] = [item[0] for item in user_setup]

data["fps"] = 30
data["single"] = None
data["dual"] = tuple()
data["delayed"] = []
data["slowmotion"] = []
data["recording"] = False
# superdelay = 0

def generate_menu():
    menu = [
        {
            "choices": [
                "LIVE - Singlecam",
                "LIVE - Doublecam",
                "DELAY - Singlecam",
                "DELAY - Singlecam Quadview",
                "DELAY - Doublecam",
                "LIVE - 4 cam Quadview (need 4 cams)"
            ],
            "jsmenu": "menu.js"
        },
        {
            "choices": data["mapping"],
            "jsmenu": "live_single.js"
        },
        {
            "choices": data["mapping"],
            "jsmenu": "live_double.js"
        },
        {
            "choices": data["mapping"],
            "jsmenu": "delay_single.js"
        },
        {
            "choices": data["mapping"],
            "jsmenu": "quad.js"
        },
        {
            "choices": data["mapping"],
            "jsmenu": "delay_double.js"
        },
    ]
    return menu

if user_setup:
    menu = generate_menu()

def slow(percent):
    global data

    camera = data["slowcam"]

    if percent > 0:
        import time
        starttime = time.time()
        p = (100 / percent)
        counter = 0
        minicounter = 0
        while True:
            if (time.time() - starttime)*data["fps"] > p:
                counter += 1
                starttime = time.time()
            try:
                yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data["slowmotion"][counter % len(data["slowmotion"])] + b'\r\n')

            except:
                print("Slowmotion {}% done.".format(percent))
                break
    else:
        counter = -1
        while True:
            try:
                data["slowmotion"].append(camera.get_frame())

                counter+=1

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + data["slowmotion"][counter] + b'\r\n')

            except:
                print("Slowmotion recording done.")

                break

def gen1(delay):
    global data

    camera = data["delayed"][0]
    counter = 0
    frames = []
    # frames.append(camera.get_loading_image())
    while True:
        try:
            frames.append(camera.get_frame())

            counter+=1
            imgcounter = math.ceil(delay-len(frames)/data["fps"])
            if imgcounter > 36:
                imgcounter = 36
            if len(frames) >= (int(delay)*data["fps"]):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n')
            else:
                # if len(frames) > 0:
                # math.ceil(delay-len(frames)/30)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image(imgcounter) + b'\r\n')
        except:
            print("Gen 1 done.")
            frames = []
            # camera.release_cam()
            break
    # if len(data["delayed"]) > 0:
    #     camera.release_cam()

def gen2(delay):
    global data

    camera = data["delayed"][1]
    counter = 0
    frames = []
    while True:
        try:
            frames.append(camera.get_frame())
            counter+=1
            if len(frames) >= (int(delay)*data["fps"]):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n')
            else:
                # if len(frames) >= 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image(math.ceil(delay-len(frames)/data["fps"])) + b'\r\n')
        except:
            print("Gen 2 done.")
            frames = []
            # camera.release_cam()
            break

    # if len(data["delayed"]) > 0:
    #     camera.release_cam()

def gen3(delay):
    global data

    camera = data["delayed"][2]
    counter = 0
    frames = []
    while True:
        try:
            frames.append(camera.get_frame())
            counter+=1
            if len(frames) >= (int(delay)*data["fps"]):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n\r\n')
            else:
                if len(frames) >= 0:
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image(math.ceil(delay-len(frames)/data["fps"])) + b'\r\n\r\n')
        except:
            # camera.release_cam()
            print("Gen 3 done.")
            break
    # if len(data["delayed"]) > 0:

def gen4(delay):
    global data

    camera = data["delayed"][3]
    counter = 0
    frames = []
    while True:
        try:
            frames.append(camera.get_frame())
            counter+=1
            if len(frames) >= (int(delay)*data["fps"]):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n\r\n')
            else:
                if len(frames) > 0:
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image(math.ceil(delay-len(frames)/data["fps"])) + b'\r\n\r\n')
        except:
            # camera.rel0ease_cam()
            print("Gen 4 done.")
            break


    # if len(data["delayed"]) > 0:



app = Flask(__name__)



@app.route("/", defaults={'menu_nr': 0})
@app.route("/<int:menu_nr>")
def main(menu_nr):
    """ Main route """
    global user_setup
    global menu
    global data
    user_setup = functions.read_user_config()

    if not user_setup:
        return redirect(url_for("admin", action="menu"))

    data["cameras"] = []
    data["cameras"] = functions.init_list_of_new_cameras(user_setup)
    data["mapping"] = [item[0] for item in user_setup]
    menu = generate_menu()
    print(data["mapping"])
    print("Initializing cameras")
    try:
        gc.collect()
        print("Freeing some memory")
    except:
        print("No memory to set free...")

    try:
        if len(data["delayed"]) > 0:
            for cam in data["delayed"]:
                del cam
            print("Releasing delayed cams")
    except Exception as e:
        print(e)

    try:
        data["single"] = None
        data["dual"] = tuple()
        data["slowmotion"] = []
        print("Releasing single, dual, slowmotion cams")
    except:
        print("No cams to release")

    if menu_nr > 0:
        header = menu[0]["choices"][menu_nr-1]

    else:
        header = "Menu"

    return render_template("index.html", header=header, menu=menu[menu_nr], choices=data["mapping"])



@app.route("/selectcam/", defaults={'cam_nr': 0})
@app.route("/selectcam/<int:cam_nr>")
def selectcam(cam_nr):
    """ select single cam route """
    global data

    if cam_nr <= len(user_setup):
        data["single"] = cam_nr-1

        return redirect(url_for("stream", delay=0))
    else:
        return redirect(url_for("main"))



@app.route("/selectbox/", defaults={'cam_nr': 0})
@app.route("/selectbox/<int:cam_nr>")
def selectbox(cam_nr):
    """ select middle route """
    global data

    if cam_nr <= len(user_setup):
        data["single"] = cam_nr-1

    return render_template("selectbox.html", cam=functions.get_single_cam(data))



@app.route('/stream', methods=['GET'])
def stream():
    """ Route for streaming single cam """
    global data

    chosencamera = functions.get_single_cam(data)
    delay = 0
    try:
        delay = int(request.args.get("delay"))
    except:
        pass

    if delay > 0:
        data["delayed"] = [chosencamera]
        return render_template("one_cam_delay.html", data=data["delayed"], delay=delay)
    else:
        data["slowcam"] = chosencamera
        return render_template("one_cam.html", data=chosencamera)



@app.route("/select-dual-cams/<int:left>/<int:right>")
def select_dual_cam(left, right):
    """ select_dual_cam route """
    global data
    data["dual"] = (left-1, right-1)
    chosencams = functions.get_dual_cams(data)

    return render_template("dual.html", cams=chosencams, left=left, right=right)


@app.route("/shutdown", methods=['GET', 'POST'])
def shutdown():
    """ shutdown route """
    if request.method == 'POST':
        if request.values.get('shutdown') == request.values.get('secret'):
            return functions.shutdown()
        else:
            return render_template("shutdown.html", secret=random.randint(1000, 9999))
    else:
        return render_template("shutdown.html", secret=random.randint(1000, 9999))



@app.route("/select-dual-delay-left/<int:left>/<int:right>")
def select_dual_delay(left, right):
    """ select_dual_delay route """
    global data

    data["dual"] = (left-1, right-1)
    data["delayed"] = list(functions.get_dual_cams(data))

    return render_template("selectdualdelay_left.html", cam=data["delayed"][0])

@app.route("/select-dual-delay-right", methods=['GET'])
def select_dual_delay_right():
    """ select_dual_delay route """
    global data
    delay = 0
    try:
        delay = int(request.args.get("delay"))
    except:
        pass

    data["delayleft"] = delay

    return render_template("selectdualdelay_right.html", cam=data["delayed"][1])



@app.route('/stream-dual-delay', methods=['GET'])
def stream_dual_delay():
    """ Route for streaming dual with delay """
    global data
    delay = 0
    try:
        delay = int(request.args.get("delay"))
    except:
        pass

    data["delayright"] = delay

    return render_template("dual_delay.html", data=data["delayed"], delayl=data["delayleft"], delayr=data["delayright"])



@app.route("/delta/<int:cam_nr>")
def delta(cam_nr):
    """ delta middle route """

    global data
    global user_setup

    if int(cam_nr) <= len(user_setup):
        data["single"] = cam_nr - 1
        data["delayed"] = functions.set_quad_cam(data, user_setup)

    return render_template("selectdelta.html", cam=data["delayed"][0])


@app.route('/delta2', methods=['GET'])
def delta2():
    """ Route for the infamous quad cam #2 """
    global data

    delay = int(request.args.get("delay"))
    data["delay"] = delay

    return render_template("select_time_delta.html", cam=data["delayed"][0])


@app.route('/quad', methods=['GET'])
def quad():
    """ Route for the infamous quad cam """
    timedelta = 0
    try:
        timedelta = int(request.args.get("timedelta"))
    except:
        pass

    return render_template("quad.html", data=data["delayed"], delay=data["delay"], delta=timedelta)


@app.route('/view_slow', methods=['GET'])
def view_slow():
    """ Route for the view slow """
    percent = 0
    try:
        percent = int(request.args.get("slowpercent"))
    except:
        pass

    return render_template("view_slow.html", data=data["slowcam"], percent=percent)



@app.route('/delaystream/<int:delay>/<int:gen>')
def delaystream(delay, gen):
    """ Route used by delayed streams """

    if gen == 1:
        return Response(gen1(delay), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif gen == 2:
        return Response(gen2(delay), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif gen == 3:
        return Response(gen3(delay), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif gen == 4:
        return Response(gen4(delay), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/slowmotion')
def slowmotion():
    """ Route used to slowmotion streams """
    global data
    # data["slowmotion"].append()
    return render_template("one_cam_slow.html", data=data["slowcam"])

@app.route('/slowmotion_stream/<int:percent>')
def slowmotion_stream(percent):
    """ Route used by slowmotion streams """
    res_percent = 0
    try:
        res_percent = int(percent)
    except:
        pass
    return Response(slow(res_percent), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/slowmotion/break')
def slowmotion_break():
    """ Route used to break slowmotion streams """
    global data

    return render_template("slow_percent.html", cam=data["slowcam"])


@app.route("/splashscreen")
def splashscreen():
    """ splashscreen middle route """

    return render_template("splashscreen.html")

@app.route("/all_quad")
def all_quad():
    """ All quad route """
    global data
    if len(user_setup) < 4:
        return redirect(url_for("main"))
    else:
        temp = functions.get_all_cams(data, user_setup)

        return render_template("super_quad.html", data=temp)

@app.route("/admin/<string:action>")
def admin(action=None):
    """ Admin route """
    global data
    admindata = []

    if action == "menu":
        pass
    elif action == "check":
        ips = functions.get_ips_from_file()

        for ip in ips:
            if functions.pingwithip(ip):
                admindata.append(ip + "\t\t<span class='green'>(online)</span>")
            else:
                admindata.append(ip + "\t\t<span class='red'>(offline)</span>")

    elif action == "checkconfig":
        admindata = functions.get_config_from_file()
    elif action == "deleteconfig":
        admindata = functions.delete_config()
    elif action == "deleteipadress":
        return render_template("admin_deleteip.html", data=functions.get_ips_from_file())


    return render_template("admin.html", action=action, data=admindata)

@app.route('/admin-insert', methods=['GET'])
def admin_insert():
    """ Route for the admin insert ip route """
    insert_ip = request.args.get("ipadress")
    action = "ipinsert"

    if insert_ip == "":
        admindata = "No ip provided."
        return render_template("admin.html", action=action ,data=admindata)
    elif not str(insert_ip).startswith(str(functions.get_subnet())):

        admindata = "The camera must be on the local network. (ip should start with {})".format(functions.get_subnet())
        return render_template("admin.html", action=action ,data=admindata)

    else:

        result = functions.pingwithip(insert_ip)

        if result == True:
            admindata = functions.insert_ip(insert_ip)
        else:
            action = "acceptip"
            admindata = insert_ip
            return render_template("admin.html", action=action ,data=admindata)

    #
    return render_template("admin.html", action=action ,data=admindata)

@app.route('/admin-remove/<int:ipaddress>')
def admin_remove(ipaddress=None):
    """ Route for the admin remove ip route """
    admindata = ""

    if ipaddress != None:
        admindata = functions.remove_ip(ipaddress)

    action = "removeip"
    return render_template("admin.html", action=action ,data=admindata)

@app.route('/admin-force-add/<string:ipaddress>')
def admin_force_add(ipaddress=None):
    """ Route for the admin remove ip route """
    admindata = "Nothing here..."

    if ipaddress != None:
        admindata = functions.insert_ip(ipaddress)


    action = "ipinsert"
    return render_template("admin.html", action=action ,data=admindata)



@app.route('/admin-config', methods=['POST', 'GET'])
def adminconfig():
    """ Route for the admin config route """
    admindata = ""
    action = ""
    if request.method == "POST":
        functions.generate_user_config(request.form)

        return redirect(url_for("admin", action="menu"))
    else:
        action = "config"
        admindata = functions.get_ips_from_file()

        return render_template("admin_config.html", action=action, data=admindata)


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."

@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    import traceback
    return "<p>Flask 500<pre>" + traceback.format_exc()


if __name__ == "__main__":
    # configpath = "script/user_config.txt"

    from waitress import serve
    serve(app, host="0.0.0.0", port=5000, threads=8)
    # app.run(threaded=True)
