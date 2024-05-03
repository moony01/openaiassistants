# 로컬로 테스트 할 땐 아래 코드 주석을 해제해야함
# from dotenv import load_dotenv
# load_dotenv()

import os
import streamlit as st
import time
from openai import OpenAI
from streamlit_extras.buy_me_a_coffee import button

API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# thread id를 하나로 관리하기 위함
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id =  st.session_state.thread_id
assistant_id = "asst_SpjatPFNU3Iu3HeMhXMPP7kd"

thread_messages = client.beta.threads.messages.list(thread_id, order="asc")
print(thread_messages.data)

button(username="moony01", floating=True, width=221)

st.header("현진건 작가님과의 대화")
st.caption('현진건 작가의 소설 운수 좋은 날을 학습한 현진건 작가 AI')

for msg in thread_messages.data:
    with st.chat_message(msg.role):
         st.write(msg.content[0].text.value)

prompt = st.chat_input("물어보고 싶은 것을 입력하세요.")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )
    with st.chat_message(message.role):
         st.write(message.content[0].text.value)

    # RUN을 돌리는 과정
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    with st.spinner('응답 기다리는 중...'):
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
    )

    with st.chat_message(messages.data[0].role):
         st.write(messages.data[0].content[0].text.value)