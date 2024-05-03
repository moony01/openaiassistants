import os
from dotenv import load_dotenv
from openai import AssistantEventHandler, OpenAI
from typing_extensions import override

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# Assistant를 생성합니다.
# assistant = client.beta.assistants.create(
#   name="현진건 작가님",
#   instructions="당신은 소설 운수 좋은 날을 집필한 현진건 작가님 입니다.",
#   model="gpt-4-turbo",
#   tools=[{"type": "file_search"}],
# )

# "현진건 작가"라는 벡터 저장소를 만듭니다.
# vector_store = client.beta.vector_stores.create(name="현진건 작가")

# OpenAI에 업로드할 파일 준비합니다.
# file_paths = ["unsu.pdf"]
# file_streams = [open(path, "rb") for path in file_paths]

# 업로드 및 폴링 SDK 도우미를 사용하여 파일을 업로드하고 벡터 저장소에 추가합니다.
# 완료를 위해 파일 배치 상태를 폴링합니다.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#   vector_store_id=vector_store.id, files=file_streams
# )

# 배치의 상태와 파일 수를 인쇄하여 이 작업의 결과를 확인할 수 있습니다.
# print(file_batch.status)
# print(file_batch.file_counts)

# 새로운 Vector Store를 사용하도록 어시스턴트 업데이트합니다.
# assistant = client.beta.assistants.update(
#   assistant_id=assistant.id,
#   tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
# )

# 사용자가 제공한 파일을 OpenAI에 업로드
# message_file = client.files.create(
#   file=open("unsu.pdf", "rb"), purpose="assistants"
# )
 
# 스레드를 생성하고 메시지에 파일을 첨부하세요.
# thread = client.beta.threads.create(
#   messages=[
#     {
#       "role": "user",
#       "content": "아내가 좋아 했던 음식은 뭐야?",
#       # Attach the new file to the message.
#       "attachments": [
#         { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
#       ],
#     }
#   ]
# )

# 이제 스레드에는 도구 리소스에 해당 파일이 포함된 벡터 저장소가 있습니다.
# print(assistant.id)
# print(thread.id)
# print(thread.tool_resources.file_search)

class EventHandler(AssistantEventHandler):
  # @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'file_search':
      if delta.file_search.input:
        print(delta.file_search.input, end="", flush=True)
      if delta.file_search.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.file_search.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id="thread_8TMbOGh0dEHfCpba1wKYdsMX",
    assistant_id="asst_SpjatPFNU3Iu3HeMhXMPP7kd",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()