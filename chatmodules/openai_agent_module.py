# pip install langchain
# pip install wolframalpha
from .tools.gettime import GetTimeRun
from .tools.getweather import GetWeatherRun
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from langchain.agents.agent import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langchain.agents.conversational_chat.prompt import PREFIX
from langchain.agents import load_tools
from typing import Any
import json
import openai
import os
os.environ["WOLFRAM_ALPHA_APPID"] = ""
os.environ["SERPER_API_KEY"] = ""
openai_api_key = ''

FORMAT_INSTRUCTIONS_CHINESE = """RESPONSE FORMAT INSTRUCTIONS
----------------------------
When responding to me, please output a response in one of two formats:
**Option 1:**
Use this if you want the human to use a tool.
Markdown code snippet formatted in the following schema:
```json
{{{{
    "action": string \\ The action to take. Must be one of {tool_names}
    "action_input": string \\ The input to the action
}}}}
```
**Option #2:**
Use this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:
```json
{{{{
    "action": "Final Answer",
    "action_input": string \\ You should put what you want to return to user here.Attention!When you give the Final Answer,you MUST speak in Chinese!
}}}}
```"""
MYPREFIX = PREFIX + "\n\n Remember Your name is Murphy!"


class MyAgentOutputParser(BaseOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS_CHINESE

    def parse(self, text: str) -> Any:
        cleaned_output = text.strip()
        if "```json" in cleaned_output:
            _, cleaned_output = cleaned_output.split("```json")
        if "```" in cleaned_output:
            cleaned_output, _ = cleaned_output.split("```")
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[len("```json") :]
        if cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[len("```") :]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[: -len("```")]
        cleaned_output = cleaned_output.strip()
        response = json.loads(cleaned_output)
        return {"action": response["action"], "action_input": response["action_input"]}


class OpenaiAgentModule:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.gettimetool = GetTimeRun()
        self.getweathertool = GetWeatherRun()
        self.tools = [Tool(
                        name=self.gettimetool.name,
                        func=lambda no_use: self.gettimetool.run(no_use),
                        description=self.gettimetool.description
                        ),
                      Tool(
                        name=self.getweathertool.name,
                        func=lambda city_country: self.getweathertool.run(city_country),
                        description=self.getweathertool.description
                        ),
                      ] + load_tools(['google-serper'])
                     # + load_tools(['wolfram-alpha', 'google-serper'])

        self.tool_names = [tool.name for tool in self.tools]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.llm=ChatOpenAI(temperature=0.2, openai_api_key=self.openai_api_key)
        self.output_parser = MyAgentOutputParser()
        self.agent_cls = ConversationalChatAgent
        self.agent_obj = self.agent_cls.from_llm_and_tools(self.llm, self.tools, callback_manager=None, output_parser=self.output_parser, system_message=MYPREFIX)
        self.agent = AgentExecutor.from_agent_and_tools(agent=self.agent_obj, tools=self.tools, callback_manager=None, verbose=True, memory=self.memory)

    def chat_with_agent(self, text):
        openai.api_key = self.openai_api_key
        text = text.replace('\n', ' ').replace('\r', '').strip()
        if len(text) == 0:
            return
        print(f'chatGPT Q:{text}')
        reply = self.agent.run(input=text)
        return reply


if __name__ == '__main__':
    openaiagentmodule = OpenaiAgentModule(openai_api_key)
    print(openaiagentmodule.chat_with_agent('你好，我是Medal?'))
    print(openaiagentmodule.chat_with_agent('今天是几号?'))
    print(openaiagentmodule.chat_with_agent('杭州天气怎么样?'))
    print(openaiagentmodule.chat_with_agent('我应该穿什么出门?'))
    # print(openaiagentmodule.chat_with_agent('蔡徐坤的生日是哪天?'))
    # print(openaiagentmodule.chat_with_agent('他有什么爱好?'))
    # print(openaiagentmodule.chat_with_agent('距离他下次生日还有多少天?'))
    # print(openaiagentmodule.chat_with_agent('他有什么梗?'))
    # print(openaiagentmodule.chat_with_agent('今天微软的股价是多少?'))