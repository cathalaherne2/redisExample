import redis
import os

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")

# Connect to Redis
redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
redis_port = 18857
client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Stream and consumer group settings
stream_name = "message_stream"
group_name = "group1"

# Ensure the stream and consumer group exist
try:
    client.xgroup_create(name=stream_name, groupname=group_name, id="$", mkstream=True)
    print(f"Consumer group {group_name} created for stream {stream_name}.")
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP" in str(e):
        print(f"Consumer group {group_name} already exists.")
    else:
        raise

# Produce messages
for i in range(10):
    message = {"field1": f"value-{i}", "field2": f"data-{i}"}
    client.xadd(stream_name, message)
    print(f"Produced message: {message}")
