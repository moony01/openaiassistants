from dotenv import load_dotenv
from typing_extensions import override
from openai import OpenAI
from openai import AssistantEventHandler
import os

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# asst_mThe21KWoyXnz11Yn7Rp60GI
# assistant = client.beta.assistants.create(
#   name="Math Tutor2",
#   instructions="You are a personal math tutor. Write and run code to answer math questions.",
#   tools=[{"type": "code_interpreter"}],
#   model="gpt-4-turbo",
# )
# print(assistant)

# thread_YiwgVP2EZIfvKCZL2M8HrDwh
# thread = client.beta.threads.create()
# print(thread)

# msg_SJhurAwkvWH45LyeOmHMrQzS
# message = client.beta.threads.messages.create(
#   thread_id="thread_YiwgVP2EZIfvKCZL2M8HrDwh",
#   role="user",
#   content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
# )
# print(message)

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
with client.beta.threads.runs.stream(
  thread_id="thread_YiwgVP2EZIfvKCZL2M8HrDwh",
  assistant_id="asst_mThe21KWoyXnz11Yn7Rp60GI",
  instructions="Please address the user as Jane Doe. The user has a premium account.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()