# generate_big_log.py —— 运行一次，生成 5 万行 trade_complex.log
import random
from datetime import datetime, timedelta

# 参数
TOTAL_LINES = 50_000
START_TIME = datetime(2025, 11, 12, 9, 0, 0)
STOCKS = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META"]
LOG_FILE = "logs/trade_complex.log"

# 创建目录
import os

os.makedirs("logs/logs", exist_ok=True)


def random_time(base):
    return (base + timedelta(milliseconds=random.randint(0, 999))).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def random_latency():
    return random.choices([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 25, 30, 35, 50, 80, 120],
                          weights=[5, 5, 10, 10, 15, 15, 10, 8, 5, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1])[0]


with open(LOG_FILE, 'w', encoding='utf-8') as f:
    current_time = START_TIME
    for i in range(TOTAL_LINES):
        timestamp = random_time(current_time)
        current_time += timedelta(milliseconds=random.randint(10, 200))

        r = random.random()
        if r < 0.6:  # 60% BUY
            stock = random.choice(STOCKS)
            qty = random.randint(50, 500)
            price = round(random.uniform(100, 3000), 2)
            latency = random_latency()
            success = "success" if random.random() < 0.7 else ""
            f.write(
                f"[{timestamp}] INFO   BUY    {stock.ljust(5)}  {qty}@{price}  latency={latency}ms  exec_id=EXEC{i:05d} {success}\n")

        elif r < 0.8:  # 20% SELL
            stock = random.choice(STOCKS)
            qty = random.randint(50, 500)
            price = round(random.uniform(100, 3000), 2)
            latency = random_latency()
            failed = "failed: insufficient shares" if random.random() < 0.3 else ""
            f.write(
                f"[{timestamp}] INFO   SELL   {stock.ljust(5)}  {qty}@{price}  latency={latency}ms  exec_id=EXEC{i:05d} {failed}\n")

        elif r < 0.95:  # 15% 延迟告警
            delay = random.choice([95, 110, 120, 130, 150])
            threshold = 100 if delay > 100 else 90
            f.write(f"[{timestamp}] WARN   MARKET_DATA_DELAY: {delay}ms > {threshold}ms threshold\n")

        else:  # 5% 其他
            f.write(f"[{timestamp}] DEBUG  HEARTBEAT  seq={i}\n")

print(f"已生成 {TOTAL_LINES} 行日志 → {LOG_FILE}")