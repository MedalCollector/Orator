from aip import AipSpeech
from playsound import playsound
import pyttsx3

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_baidu_and_play(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 4, # 语速
            'vol': 5, # 音量大小
            'per': 4  # 发声人 百度丫丫
        })  # 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("./audio.wav", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        playsound('./audio.wav')

class Pyttsx3TTS:
    def __init__(self):
        pass

    def text_to_speech_pyttsx3(self, text=""):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()



if __name__ == '__main__':
    baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    baidutts.text_to_speech_baidu_and_play('今天天气真不错!')

    pyttsx3tts = Pyttsx3TTS()
    pyttsx3tts.text_to_speech_pyttsx3('今天天气真不错!')


















