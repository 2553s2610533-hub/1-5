import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="달콤살벌 연애상담소", page_icon="💖", layout="centered")
st.title("💖 달콤살벌 연애상담소")
st.caption("누구에게도 말 못 한 연애 고민, 시원하게 털어놓으세요!")

# Streamlit Secrets에서 API 키 불러오기 및 검증
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# Gemini 클라이언트 초기화 (최신 google-genai SDK 기준)
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

try:
    client = get_client(api_key)
except Exception as e:
    st.error(f"클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("연애 고민을 입력해보세요... (예: 남친이 연락을 잘 안 해요)"):
    # 1. 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 챗봇 답변 생성 및 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 시스템 지침(페르소나) 및 이전 대화 기록 포함하여 프롬프트 구성
        # gemini-2.5-flash-lite 모델은 가벼우면서도 대화 문맥을 잘 파악합니다.
        system_instruction = (
            "당신은 공감 능력이 뛰어나면서도 때로는 뼈를 때리는 현실적인 조언을 해주는 "
            "전문 연애 상담사입니다. 친구처럼 친근하고 다정한 말투(반말과 존댓말을 적절히 섞거나, "
            "친근한 해요체 사용)로 답변해주세요. 상대방의 감정에 먼저 공감한 후, "
            "상황을 객관적으로 분석하고 실질적인 해결책이나 행동 지침을 제안하세요."
        )
        
        # 대화 맥락을 API에 전달하기 위해 형식 변환
        contents = []
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            ))

        try:
            with st.spinner("생각 중... 💬"):
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
            
            # 답변 출력 및 저장
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as ae:
            message_placeholder.error(f"❌ Gemini API 오류가 발생했습니다: {ae.message}")
        except Exception as e:
            message_placeholder.error(f"An unexpected error occurred: {e}")
l
