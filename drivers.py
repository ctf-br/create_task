# -*- encoding: utf-8 -*-

import os

class Drivers:
    @staticmethod
    def github(payload):
        # filtering
        if 'pull_request' not in payload:
            return {}
        if payload['action'] not in {'opened', 'reopened'}:
            return {}
        if payload['pull_request']['base']['repo']['full_name'] != os.getenv('SUBMISSION_PROJECT'):
            return {}
        if payload['pull_request']['base']['ref'] != 'master':
            return {}
        # mappings
        return {
            'mr_id'          : payload['pull_request']['number'],
            'source_ssh_url' : payload['pull_request']['head']['repo']['ssh_url'],
            'source_commit'  : payload['pull_request']['head']['sha'],
            'user_id'        : payload['pull_request']['user']['id'],
            'username'       : payload['pull_request']['user']['login']
        }

    @staticmethod
    def gitlab(payload):
        # filtering
        if payload['object_kind'] != 'merge_request':
            return {}
        if payload['object_attributes']['action'] not in {'open', 'reopen'}:
            return {}
        if payload['object_attributes']['target']['path_with_namespace'] != os.getenv('SUBMISSION_PROJECT'):
            return {}
        if payload['object_attributes']['target_branch'] != 'master':
            return {}
        # mappings
        return {
            'mr_id'          : payload['object_attributes']['id'],
            'source_ssh_url' : payload['object_attributes']['source']['git_ssh_url'],
            'source_commit'  : payload['object_attributes']['last_commit']['id'],
            'user_id'        : payload['object_attributes']['author_id'],
            'username'       : payload['user']['username']
        }
