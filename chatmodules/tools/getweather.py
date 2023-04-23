"""获取当前天气的工具."""
import requests
OPENWEATHER_API_KEY = ""


class GetWeatherRun(object):
    name = "Get Weather"
    description = (
        "Useful for when you need to answer questions about weather information. "
        "Input should be a string of city and country split by ',', both must be in English, the country should be a ISO 3166-1 alpha-2 code, for example 'London,GB'."
    )

    def run(self, city_country: str) -> str:
        # 获取当天天气的工具
        base_url = f'http://api.openweathermap.org/data/2.5/weather?'
        city = city_country.split(",", 0)
        url = f"{base_url}q={city_country}&appid={OPENWEATHER_API_KEY}"
        res = requests.get(url)
        weather = res.json()
        temp = int(weather["main"]["temp"] - 273.15)
        feels_like = int(weather["main"]["feels_like"] - 273.15)
        pressure = weather["main"]["pressure"]
        humidity = weather["main"]["humidity"]
        main = weather["weather"][0]["main"]
        description = weather["weather"][0]["description"]
        wind = weather["wind"]
        return f"{main},{description},体感温度{feels_like}摄氏度,空气湿度{humidity}%,风速{wind['speed']}米/秒"


if __name__ == '__main__':
    weather = GetWeatherRun()
    print(weather.run('Shanghai,CN?'))
