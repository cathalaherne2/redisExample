import redis
import time
import os

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")

# Connect to Redis
redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
redis_port = 18857
client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Channel name
channel = "notifications"

# Publish messages
print("Publisher is running. Sending messages...")
for i in range(10):
    message = f"Message {i}"
    client.publish(channel, message)  # Publish to the channel
    print(f"Published: {message}")
    time.sleep(1)  # Simulate some delay between messages

print("All messages sent!")
