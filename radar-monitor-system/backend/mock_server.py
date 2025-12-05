import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import math
import random
import threading
import numpy as np

# 初始化 FastAPI
app = FastAPI(title="雷达模拟器", description="为前端开发提供的假数据服务")

# 允许跨域 (CORS)，这样你的 Vue 就能访问了
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟的全局状态
state = {
    "heart_rate": 75.0,
    "target_distance": 0.8,
    "target_bin": 30,
    "phase_values": [],
    "running": True,
    "start_time": time.time(),
    "frame_count": 0
}


# 后台线程：不断生成变化的假数据
def generate_fake_data():
    t = 0
    while True:
        t += 0.1
        # 1. 模拟心率：在 70-80 之间浮动
        state["heart_rate"] = 75 + 5 * math.sin(t * 0.5) + random.uniform(-1, 1)

        # 2. 模拟呼吸波形 (相位数据)：正弦波 + 噪声
        # 生成 100 个点的波形数据供前端画图
        wave_t = np.linspace(t, t + 4 * np.pi, 100)
        phase_signal = np.sin(wave_t) * 1.5 + np.random.normal(0, 0.1, 100)
        state["phase_values"] = phase_signal.tolist()

        # 3. 模拟距离：偶尔动一下
        state["target_distance"] = 0.8 + 0.05 * math.sin(t * 0.1)

        state["frame_count"] += 1
        time.sleep(0.1)  # 10Hz 更新频率


# 启动后台造数线程
threading.Thread(target=generate_fake_data, daemon=True).start()


# --- 接口定义 (保持与真实后端一致) ---

@app.get("/")
async def root():
    return {"message": "这是模拟雷达服务器"}


@app.get("/heartrate")
async def get_heart_rate():
    return {
        "heart_rate": round(state["heart_rate"], 1),
        "timestamp": time.time(),
        "status": "ok"
    }


@app.get("/target")
async def get_target_data():
    return {
        "heart_rate": round(state["heart_rate"], 1),
        "target_distance": round(state["target_distance"], 2),
        "target_bin": state["target_bin"],
        "timestamp": time.time(),
        "status": "ok"
    }


@app.get("/detailed")
async def get_detailed_data():
    return {
        "phase_values": state["phase_values"],  # 这是一个数组，前端拿去画折线图
        "target_distance": state["target_distance"],
        "heart_rate": state["heart_rate"],
        "timestamp": time.time()
    }


@app.get("/status")
async def get_status():
    return {
        "running": True,
        "uptime": time.time() - state["start_time"],
        "processed_frames": state["frame_count"]
    }


if __name__ == "__main__":
    print("启动模拟服务器: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)