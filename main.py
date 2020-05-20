# -*- encoding: utf-8 -*-

from task import Task
from auth import Auth
from flask import abort
import json

def handle(request):
    try:
        request_sender = request.args.get('from')
        if not request_sender:
            abort(400)

        # just in case we dont have the function
        def func_not_found(payload):
            print('No `{}` driver found!'.format(request_sender))
            return False

        # trick to call apropriate method from Auth class
        check_auth = getattr(Auth, request_sender, func_not_found)

        # autenticate the message
        if not check_auth(request.headers, request.data):
            abort(401)

        task = Task()
        task.setDriver(request_sender)
        task.setPayload(request.get_json())
        return json.dumps(task.create())
    except Exception as e:
        print(str(e))
        abort(500)

