import psycopg2
import time

# Connect to PostgreSQL
conn = psycopg2.connect(user="postgres", password="3CHE4]#ZTD(MEDU0JE~#?mCw%PzX", host="database-3-instance-1.cowcxvjxt2yc.eu-west-1.rds.amazonaws.com", port="5432")
cur = conn.cursor()

# Sample data
user_data = {"name": "John Doe", "age": 30, "city": "New York"}

# Benchmark PostgreSQL writes
start_time = time.time()
for i in range(10000):
    cur.execute("INSERT INTO users (name, age, city) VALUES (%s, %s, %s)", (user_data["name"], user_data["age"], user_data["city"]))
conn.commit()
write_time = time.time() - start_time
print(f"PostgreSQL write time for 10,000 records: {write_time:.4f} seconds")

# Benchmark PostgreSQL reads
start_time = time.time()
for i in range(10000):
    cur.execute("SELECT name, age, city FROM users WHERE id = %s", (i,))
    cur.fetchone()
read_time = time.time() - start_time
print(f"PostgreSQL read time for 10,000 records: {read_time:.4f} seconds")