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
consumer_name = "consumer1"

# Join the consumer group
print(f"Consumer {consumer_name} is reading from group {group_name}")
try:
    while True:
        # Read messages from the group
        messages = client.xreadgroup(groupname=group_name, consumername=consumer_name, streams={stream_name: ">"}, count=5, block=0)
        for stream, message_list in messages:
            for message_id, message_data in message_list:
                print(f"Consumer {consumer_name} processed: {message_data} with ID {message_id}")
                # Acknowledge message
                client.xack(stream_name, group_name, message_id)
except KeyboardInterrupt:
    print("Consumer stopped.")
