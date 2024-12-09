from flask import Flask
import logging
import sys
from ddtrace import tracer
import time
import redis
import os

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# Function to connect to Redis
def get_redis_client():
    redis_password = os.getenv("REDIS_PASSWORD")
    if not redis_password:
        raise ValueError("Redis password is not set in environment variables!")
    
    redis_host = "redis-18857.c2.eu-west-1-3.ec2.redns.redis-cloud.com"
    redis_port = 18857
    return redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Redis operations (Benchmark without pipeline)
@tracer.wrap(service="my-sandwich-making-svc", resource="redis_benchmark_without_pipeline")
@app.route('/api/redis_benchmark')
def redis_benchmark():
    client = get_redis_client()
    user_data = {"name": "John Doe", "age": 30, "city": "New York"}

    # Benchmark Redis writes
    start_time = time.time()
    for i in range(10000):
        client.hset(f"user:{i}", mapping=user_data)
    write_time = time.time() - start_time

    # Benchmark Redis reads
    start_time = time.time()
    for i in range(10000):
        client.hgetall(f"user:{i}")
    read_time = time.time() - start_time

    return f"Redis write time for 10,000 records: {write_time:.4f} seconds\nRedis read time for 10,000 records: {read_time:.4f} seconds"

# Redis operations (Benchmark with pipeline)
@tracer.wrap(service="my-sandwich-making-svc", resource="redis_benchmark_with_pipeline")
@app.route('/api/redis_benchmark_pipeline')
def redis_benchmark_pipeline():
    client = get_redis_client()
    user_data = {"name": "John Doe", "age": 30, "city": "New York"}

    # Benchmark Redis writes with pipeline
    start_time = time.time()
    with client.pipeline() as pipe:
        for i in range(10000):
            pipe.hset(f"user:{i}", mapping=user_data)
        pipe.execute()  # Execute all commands in one go
    write_time = time.time() - start_time

    # Benchmark Redis reads with pipeline
    start_time = time.time()
    with client.pipeline() as pipe:
        for i in range(10000):
            pipe.hgetall(f"user:{i}")
        pipe.execute()  # Execute all read commands in one go
    read_time = time.time() - start_time

    return f"Redis write time for 10,000 records with pipeline: {write_time:.4f} seconds\nRedis read time for 10,000 records with pipeline: {read_time:.4f} seconds"

# Existing APM routes
@tracer.wrap(service="my-sandwich-making-svc", resource="root")
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@tracer.wrap(service="my-sandwich-making-svc", resource="apm")
@app.route('/api/apm')
def apm_endpoint():
    tracer.set_tags({"customer": "123456789"})
    adding()
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@tracer.wrap(service="my-sandwich-making-svc", resource="adding")
def adding():
    time.sleep(.1)
    var = 1234567890 + 1234567890
    tracer.set_tags({"varValue": str(var)})
    minus()
    return var

@tracer.wrap(service="my-sandwich-making-svc", resource="minus")
def minus():
    time.sleep(.1)
    var = 1234567890 - 1234567880
    tracer.set_tags({"varValue": str(var)})
    return var

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
