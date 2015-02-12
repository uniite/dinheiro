import binascii
import json
import os
import uuid

import boto.sqs
import boto.sqs.message
import libnacl.public
import libnacl.utils

# Used for communication over SQS
RESPONSE_SECRET_KEY = os.environ.get('RESPONSE_SECRET_KEY')
REQUEST_PUBLIC_KEY = os.environ.get('REQUEST_PUBLIC_KEY')
REQUEST_QUEUE = os.environ.get('REQUEST_QUEUE')
RESPONSE_QUEUE = os.environ.get('RESPONSE_QUEUE')



def load_key(key):
    return binascii.unhexlify(key)


def transport_box():
    return libnacl.public.Box(load_key(RESPONSE_SECRET_KEY), load_key(REQUEST_PUBLIC_KEY))


class SecureMessage(boto.sqs.message.RawMessage):
    def encode(self, value):
        data = json.dumps(value)
        data = transport_box().encrypt(data)
        return binascii.hexlify(data)

    def decode(self, value):
        data = binascii.unhexlify(value)
        data = transport_box().decrypt(data)
        return json.loads(data)


class Client(object):
    def __init__(self):
        # The keyword args we have are currently boto defaults, but its good to confirm they're set
        self.sqs = boto.sqs.connect_to_region('us-east-1', is_secure=True, validate_certs=True)
        # Test connection
        self.sqs.get_all_queues()
        # Get the queues we're interested in
        self.request_queue = self.sqs.get_queue(REQUEST_QUEUE)
        self.response_queue = self.sqs.get_queue(RESPONSE_QUEUE)
        # Automatically decode and decrypt incoming messages
        self.response_queue.set_message_class(SecureMessage)

    def execute(self, action, *args):
        request_id = str(uuid.uuid4())
        print "Sending request %s" % request_id
        self.request_queue.write(SecureMessage(body={'id': request_id, 'action': action, 'args': args}))
        tries = 3
        while True:
            msgs = self.response_queue.get_messages(wait_time_seconds=20)
            if len(msgs) == 0:
                continue
            msg = msgs[0]
            body = msg.get_body()
            msg.delete()
            if body['request_id'] == request_id:
                return body
            else:
                print "Mismatched message: %s" % body
                tries -= 1
            if tries == 0:
                raise StandardError('Failed to execute request')


if __name__ == '__main__':
    sqs = boto.sqs.connect_to_region('us-east-1', is_secure=True, validate_certs=True)
    print sqs.get_all_queues()
    print Client().execute('ping', ['hello'])
