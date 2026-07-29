#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
 file_name: routes/video_routes.py
 description: mahanokor matrix systems - real-time video streaming module
==============================================================================
"""

import cv2
from flask import Blueprint, Response

video_blueprint = Blueprint("video_control", __name__)

def generate_frames():
    # បើកកាមេរ៉ា (លេខ 0 សម្រាប់កាមេរ៉ាជាប់ម៉ាស៊ីន)
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # បំប្លែងរូបភាពទៅជាទម្រង់ JPEG សម្រាប់បញ្ជូនទៅកាន់ Web
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@video_blueprint.route('/video_feed')
def video_feed():
    # បញ្ជូនទិន្នន័យវីដេអូជាលក្ខណៈ Streaming
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
