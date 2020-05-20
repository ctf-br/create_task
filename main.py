# -*- encoding: utf-8 -*-

from task import Task;
import json

def handle(request):
    task = Task()
    task.setDriver(request.args.get('from', 'generic'))
    task.setPayload(request.get_json())
    return json.dumps(task.create())

