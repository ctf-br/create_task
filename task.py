# -*- encoding: utf-8 -*-

from time import strftime
from drivers import Drivers
import json
import os

class Task:
    driver  = 'generic'
    payload = {}

    def setDriver(self, driver):
        self.driver = driver

    def setPayload(self, payload):
        self.payload = payload or {}

    def create(self):
        payload = self.build()

        if 'mr_id' not in payload:
            return {'message':'Can\'t creat task'}

        task = self.add_to_queue(payload)

        return {"message":'Created task {}'.format(task.name)}


    def build(self):
        # just in case we dont have the function
        def func_not_found(payload):
            print('No `{}` driver found!'.format(handler_name))
            return {}
        handler_name = self.driver
        # trick to call apropriate method from Driver class
        handle = getattr(Drivers, handler_name, func_not_found)

        return handle(self.payload) or {}


    def add_to_queue(self, payload):
        from google.cloud import tasks_v2

        # Create a client.
        client = tasks_v2.CloudTasksClient()

        project  = os.getenv('PROJECT_ID') # 'my-project-id'
        queue    = os.getenv('QUEUE_NAME') # 'my-queue'
        location = os.getenv('LOCATION')   # 'us-central1'
        url      = os.getenv('TARGET_URL') # 'https://example.com/task_handler'
        token    = os.getenv('OIDC_TOKEN') # EMAIL@appspot.com

        # Construct the fully qualified queue name.
        parent = client.queue_path(project, location, queue)

        # Construct the request body.
        task = {
            'name': '{}/tasks/pull-request-{:08d}-at-{}'.format(parent, payload['mr_id'], strftime('%H%M%S')),
            'http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'url': url,  # The full url path that the task will be sent to.
                'headers': {
                    'Content-Type': 'application/json',
                },
                'oidc_token': {
                    'service_account_email': token
                },
                'body': json.dumps(payload).encode()
            }
        }

        # Use the client to build and send the task.
        return client.create_task(parent, task)
