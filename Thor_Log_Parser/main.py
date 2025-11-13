#_____ _
#  / ____| |
# | (___ | |__   ___  _ __
#  \___ \| '_ \ / _ \| '__|
#  ____) | | | | (_) | |
# |_____/|_| |_|\___/|_|
#高频交易日志实时分析系统
#文件名：Thor_Log_Parser v1.0.0
#版本：v1.0.0(2025-11-13)
#作者：曾祥龙(Zeng Xianglong)
#Email:zengxianglong53@outlook.com(zengxianglong@nbut.edu.cn)



import re
from pathlib import Path

log_file = Path(r"/\logs\trade_simple.log")

patterns = {
    "latency":        r"latency=(\d*)",
    "buy_success":    r"BUY.*success",
    "market_delay":   r"MARKET_DATA_DELAY"
}


def extract_data():
    total_latency : float = 0
    latency_count : int = 0
    buy_success_count : int = 0
    market_delay_count : int = 0

    with open(Path(log_file), "r", encoding="utf-8") as f:
        for line in f:
            m=re.search(patterns["latency"],line)
            if m:
                total_latency += float(m.group(1))
                latency_count += 1
            if re.search(patterns["buy_success"], line):
                buy_success_count += 1
            if re.search(patterns["market_delay"], line):
                market_delay_count += 1
    avg_latency = total_latency / latency_count

    result = {
        "平均延迟(ms)": avg_latency,
        "成功买入次数": buy_success_count,
        "延迟警告次数": market_delay_count
    }
    print(result)

extract_data()