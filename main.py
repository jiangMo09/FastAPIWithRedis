import os
from fastapi import FastAPI
from redis import Redis
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

app = FastAPI()

# 初始化 Redis 連接
redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
)


@app.get("/")
async def read_root():
    return {"message": "歡迎來到我的簡單API！"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    # 使用 Redis 來記錄訪問次數
    visits = redis.incr(f"visits:{name}")
    return {"message": f"你好，{name}！", "visits": visits}


@app.get("/visits/{name}")
async def get_visits(name: str):
    visits = redis.get(f"visits:{name}")
    if visits is None:
        return {"message": f"{name} 還沒有被訪問過"}
    return {"name": name, "visits": int(visits)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
