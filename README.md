![image](https://github.com/user-attachments/assets/c947fde1-7eee-4fe4-8245-e45051bede44)# redis Example


to play around with redis I have spun up a short script to use  aredis hash set to create a user


I was then able to connect to the same endpoint from my local PC and was able to increment the users age rather than overriding data 


![Screenshot 2024-12-08 203028](https://github.com/user-attachments/assets/c59a7e1f-4783-46c5-ab45-53b40fc1ef3c)


# Postgres performance Example

I wanted to test how fast postgres would be to create and read 10,000 users

![Screenshot 2024-12-08 224009](https://github.com/user-attachments/assets/93e46a80-58a8-42ef-a075-54de6526090c)

Taking about 7 seconds in total, 3.8 seconds to write and 3.6 to read

# Redis performance Example

okay, in an awkward scenario, it seems like my redis query actually took much longer, taking 20.2 seconds in total

![Screenshot 2024-12-08 224538](https://github.com/user-attachments/assets/35fae1cb-50a4-4b6b-b71c-8d38d1f58cc4)


Lets check to see what the issue is


# Redis pipelining to the rescue


so from what I can see using tools like chatGPT, the issue with the script I wrote was that it would write and read one at a time from each of the queries, and as such, it was quite slow. instead, if I used "pipe.execute()" to run a bunch of saved queries all at once, we could run a bunch of queries in parallel

when I modified my code to use pipelines in redis, I saw a massive performance uplift

![Screenshot 2024-12-08 231116](https://github.com/user-attachments/assets/e426d857-d5d1-40da-9822-e632ecfaee91)


in the interest of fairness, I found the equivalent in postgres is called "bulk inserts" while it made a difference on the write side, I did not see the same uplift as redis on the read side



![Screenshot 2024-12-08 231634](https://github.com/user-attachments/assets/1cf2ace6-6fe3-486f-a52d-59caac8425ed)


To ensure that these were not just one-off instances, I reran these tests several times

![Screenshot 2024-12-08 230426](https://github.com/user-attachments/assets/81556358-d023-4f13-ad47-bf7d3d2ab525)


# Redis pubsub testing

I wanted to see how redis pubsub compared with a solution like SQS, so at first I created a pub application, and began using the redis desktop client, but I didnt see any messages, even after I subscribed to the queue, there was no messages


![Screenshot 2024-12-08 235250](https://github.com/user-attachments/assets/306354bd-5b52-4683-9c31-4a1cdcc783e1)

when doing some digging, i found that redis pubsub is actually different to other queues that I have used in the past that you actually need to be subscribed at the time in order to hear the messages that are being sent.

in my experience this is quite similar to Kinesis in AWS (with some slight differences)

One interesting detail was that when subscribed with multiple consumers, they all receive every message, so there is a 1 to many relationship in this case. I also did not need to create a channel ahead of time like I believe I need to in SQS, I was directly able to push to the "notifications" channel


 when I was doing research, it seemed that Redis Streams would actually contain the older messages also, so I tried that out too


# Redis streams testing

I found that when using streams, I kept getting errors that the group i was publishing to didnt exist and I couldnt figure out why. It turns out that unlike redis pubsub we cannot just expect that a new topic is automatically being created, and so we need to do some validation to ensure when we write a message it is able to be consumed and not just disappearing into the either

# Redis + Datadog testing
I decided to instrument the redis code that I had written with Datadogs APM tool to get a better visualisation as to what exactly was going on.


I can clearly see the 200ms that it takes for the redis pipelines to execute here 

![462652580_567261996050256_6345916724041212472_n](https://github.com/user-attachments/assets/eabbd5d9-1c08-43d8-a16b-2c2ab1f65a9c)

when I hovered over the query I can see all of the redis insert statements that we are making

When I run the unoptimised query, it actually takes quite a while to load as there are 20,000 spans being sent which is highly unusual for one application.

When it does load we see 20,000 individual spans all showing microsecond/millisecond performance, it was quite interesting

![462639784_906653377863742_2152618269971130163_n](https://github.com/user-attachments/assets/fc2f6894-50eb-4952-a207-bba1dcfac20d)

