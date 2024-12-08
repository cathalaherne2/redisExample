import redis
import os

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")

# Connect to Redis
redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
redis_port = 18857
client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Channel name
channel = "notifications"

# Subscribe to the channel
pubsub = client.pubsub()
pubsub.subscribe(channel)

print(f"Subscriber is listening to the channel: {channel}")
try:
    # Listen for messages
    for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Received: {message['data']}")
except KeyboardInterrupt:
    print("Subscriber stopped.")
