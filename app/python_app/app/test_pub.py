import os
from google.cloud import pubsub_v1
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
import json

with open(cred_path) as json_file:
    creds = json.load(json_file)


publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(creds.get('project_id'), 'MY_TOPIC_NAME')

for n in range(1, 10):
    data = "Message number {}".format(n)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

print(f"Published messages to {topic_path}.")