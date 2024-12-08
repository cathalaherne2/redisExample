import redis
import time
import os


# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")


# Check if the password is set
if not redis_password:
    raise ValueError("Redis password is not set in environment variables!")


# Connect to Redis
redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
redis_port = 18857

client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Sample data
user_data = {"name": "John Doe", "age": 30, "city": "New York"}

# Benchmark Redis writes
start_time = time.time()
for i in range(10000):
    client.hset(f"user:{i}", mapping=user_data)
write_time = time.time() - start_time
print(f"Redis write time for 10,000 records: {write_time:.4f} seconds")

# Benchmark Redis reads
start_time = time.time()
for i in range(10000):
    client.hgetall(f"user:{i}")
read_time = time.time() - start_time
print(f"Redis read time for 10,000 records: {read_time:.4f} seconds")
