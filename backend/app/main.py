from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api
from .database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="涂装工艺自动检测与智能评价系统")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "涂装工艺自动检测与智能评价系统API"} 