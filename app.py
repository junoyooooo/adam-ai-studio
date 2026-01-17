from google import genai
import streamlit as st

# --- [설정] ---
API_KEY = "AIzaSyBdNxk_ytJFxFPlAaRlf20HMarLIT9oO9A".strip()
client = genai.Client(api_key=API_KEY)

def generate_all_in_one(topic):
    # 아담님 리스트에서 확인된 최강 모델 2.5 Flash 사용
    model_name = "gemini-2.5-flash"
    
    prompt = f"""
    주제: {topic}
    너는 15년 차 커머스 MD이자 건강 전문가 '아담'이야. 
    아래 주제로 3가지 플랫폼용 콘텐츠를 생성해줘.
    
    1. [워드프레스 블로그]: Rank Math SEO 90점 타겟. 전문적이고 다정한 아빠 말투. (1500자)
    2. [틱톡/쇼츠 대본]: 24초 분량. 1.2배속을 고려한 긴박한 후킹 문구 포함. [TTS용] 섹션 필수.
    3. [뉴스레터]: 구독자에게 직접 말을 거는 듯한 친근한 '모닝 브리핑' 스타일. (500자)
    """
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"에러 발생: {e}"

# --- [Streamlit UI] ---
st.title("🚀 아담 AI 통합 콘텐츠 관제탑")
topic = st.text_input("오늘의 건강/영양제 주제를 입력하세요", "식후 커피가 영양제 흡수를 방해하는 이유")

if st.button("모든 채널 콘텐츠 생성 시작"):
    with st.spinner("제미나이 2.5 Flash가 3개 채널 글을 깎는 중..."):
        result = generate_all_in_one(topic)
        st.markdown(result)