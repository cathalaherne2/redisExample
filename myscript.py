import os
import redis

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")


# Check if the password is set
if not redis_password:
    raise ValueError("Redis password is not set in environment variables!")





redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
redis_port = 18857

client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Sample data to write
key = "user:1000"
value = {"name": "John Doe", "age": 30, "city": "New York"}

client.hmset(key, value)  # Using hash data type

print(f"Data written to Redis with key: {key}")

