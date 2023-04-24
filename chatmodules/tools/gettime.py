"""获取当前时间的工具."""
from datetime import datetime
# pip install cn2an
import cn2an


class GetTimeRun(object):
    name = "Get Time"
    description = (
        "Useful for when you need to answer questions about Date or Time "
    )

    def run(self, no_use: str) -> str:
        time_now = datetime.now()
        time_now_str = time_now.strftime('%H时%M分%S秒')
        date_now_str = time_now.strftime('%Y年%m月%d日')
        weekday = str(time_now.weekday() + 1)
        weekday_cn = cn2an.an2cn(weekday)
        if weekday_cn == "七":
            weekday_cn = "日"
        return "今天的日期是:" + date_now_str + ",目前的时间是:" + time_now_str + ",今天是星期" + weekday_cn


if __name__ == '__main__':
    print(GetTimeRun().run(''))
    # 今天的日期是: 2023年04月24日, 目前的时间是: 14时40分43秒, 今天是星期一