from rq import Worker
from redis import Redis
from manager import queue_name

redis = Redis()

if __name__ == '__main__':
    worker = Worker([queue_name], connection=redis)
    worker.work()
