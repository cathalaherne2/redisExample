import redis
import os
import time

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")

# Connect to Redis
redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
redis_port = 18857
client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Stream name
stream_name = "message_stream"

# Produce messages
print("Producer is running. Writing messages to the stream...")
for i in range(10):
    message = {"message": f"Message {i}", "timestamp": str(time.time())}
    message_id = client.xadd(stream_name, message)  # Add message to stream
    print(f"Produced: {message} with ID {message_id}")
    time.sleep(1)  # Simulate delay

print("All messages produced!")
