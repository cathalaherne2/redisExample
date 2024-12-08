import os
import redis

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")


# Check if the password is set
if not redis_password:
    raise ValueError("Redis password is not set in environment variables!")



