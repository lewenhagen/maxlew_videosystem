#!/usr/bin/env python3

"""
MAXLEW Video System
Version 1.0
"""

from flask import Flask, render_template, make_response, Response, redirect, url_for, request
import functions
import gc

# User defined options
# ["<name>", <ipadress>]
user_setup = [
    ["Volt", "http://192.168.1.133"],
    ["Kullerbytta", "http://192.168.1.158"]
]

# Supervariable, going to hold all values
data = {}
# data["cameras"] = functions.init_list_of_new_cameras(user_setup)
data["mapping"] = [item[0] for item in user_setup]

data["single"] = None
data["dual"] = tuple()
data["delayed"] = []

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
            if len(frames) >= (int(delay)*25):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n')
            else:
                # if len(frames) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image() + b'\r\n')
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
            if len(frames) >= (int(delay)*25):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n')
            else:
                # if len(frames) >= 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image() + b'\r\n')
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
            if len(frames) >= (int(delay)*25):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n\r\n')
            else:
                if len(frames) >= 0:
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image() + b'\r\n\r\n')
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
            if len(frames) >= (int(delay)*25):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n\r\n')
            else:
                if len(frames) > 0:
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + camera.get_loading_image() + b'\r\n\r\n')
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

    global menu
    global data

    data["cameras"] = []
    data["cameras"] = functions.init_list_of_new_cameras(user_setup)
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

        print("Releasing single, dual cams")
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

    return render_template("selectbox.html")



@app.route('/stream', methods=['GET'])
def stream():
    """ Route for streaming single cam """
    global data

    chosencamera = functions.get_single_cam(data)

    delay = int(request.args.get("delay"))
    if delay > 0:
        data["delayed"] = [chosencamera]
        return render_template("one_cam_delay.html", data=data["delayed"], delay=delay)
    else:
        return render_template("one_cam.html", data=chosencamera)



@app.route("/select-dual-cams/<int:left>/<int:right>")
def select_dual_cam(left, right):
    """ select_dual_cam route """
    global data
    data["dual"] = (left-1, right-1)
    chosencams = functions.get_dual_cams(data)

    return render_template("dual.html", cams=chosencams, left=left, right=right)



@app.route("/select-dual-delay/<int:left>/<int:right>")
def select_dual_delay(left, right):
    """ select_dual_delay route """
    global data

    data["dual"] = (left-1, right-1)
    data["delayed"] = list(functions.get_dual_cams(data))

    return render_template("selectdualdelay.html")



@app.route('/stream-dual-delay', methods=['GET'])
def stream_dual_delay():
    """ Route for streaming dual with delay """
    global data

    delay = int(request.args.get("delay"))
    return render_template("dual_delay.html", data=data["delayed"], delay=delay)



@app.route("/delta/<int:cam_nr>")
def delta(cam_nr):
    """ delta middle route """

    global data
    global user_setup

    if int(cam_nr) <= len(user_setup):
        data["single"] = cam_nr - 1
        data["delayed"] = functions.set_quad_cam(data, user_setup)

    return render_template("selectdelta.html")


@app.route('/delta2', methods=['GET'])
def delta2():
    """ Route for the infamous quad cam #2 """
    global data

    delay = int(request.args.get("delay"))
    data["delay"] = delay

    return render_template("select_time_delta.html")


@app.route('/quad', methods=['GET'])
def quad():
    """ Route for the infamous quad cam """
    timedelta = int(request.args.get("timedelta"))

    return render_template("quad.html", data=data["delayed"], delay=data["delay"], delta=timedelta)



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
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000, threads=8)
    # app.run(threaded=True)
