import fire
import redis


if __name__ == '__main__':
    fire.Fire(redis.StrictRedis)
