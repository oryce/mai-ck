from app.pipeline.manager import process_document
from redis import Redis

redis = Redis()
if __name__ == "__main__":
    path = '/app/app/pipeline/test.pdf'
    process_document("1", path)
    print(redis.hget(f"task:1", "status").decode("UTF-8"))
    print(redis.hget(f"task:1", "signature").decode("UTF-8"))
    print(redis.hget(f"task:1", "stamp").decode("UTF-8"))
    print(redis.hget(f"task:1", "type").decode("UTF-8"))
