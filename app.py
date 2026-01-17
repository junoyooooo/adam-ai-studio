import streamlit as st
from google import genai
import PIL.Image
import io

# --- [1. API 설정] ---
# Streamlit Secrets에서 API 키를 가져옵니다.
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# --- [2. UI/UX 디자인 (고급 퍼스널 스튜디오 스타일)] ---
st.set_page_config(page_title="ADAM AI STUDIO", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #FDFBF9; }
    .main-title { font-size: 2.8rem; font-weight: 700; color: #1A1A1A; text-align: center; margin-top: 2rem; }
    .sub-title { font-size: 0.9rem; color: #A0A0A0; text-align: center; margin-bottom: 3rem; letter-spacing: 4px; text-transform: uppercase; }
    .stButton>button { width: 100%; border-radius: 12px; background: #1A1A1A; color: white; border: none; padding: 20px; font-weight: 600; font-size: 1.1rem; transition: 0.3s; }
    .stButton>button:hover { background: #444; border: none; color: #EEE; }
    .result-card { background: white; padding: 40px; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); margin-top: 30px; line-height: 1.8; color: #333; }
    hr { border: 0; height: 1px; background: #EEE; margin: 40px 0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">ADAM AI STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Premium Personal Diagnosis</div>', unsafe_allow_html=True)

# --- [3. 카메라 및 파일 업로드 기능] ---
st.markdown("### 📷 진단할 사진을 찍거나 올려주세요")
img_file = st.camera_input("") # 여기에 카메라 버튼이 생깁니다!

uploaded_file = st.file_uploader("또는 갤러리에서 사진 선택", type=['jpg', 'png', 'jpeg'])
if uploaded_file:
    img_file = uploaded_file

# --- [4. AI 초정밀 분석 및 리포트 생성] ---
if img_file:
    img = PIL.Image.open(img_file)
    
    if st.button("✨ 초정밀 AI 분석 리포트 발행"):
        with st.spinner("이미지를 정밀 분석하여 리포트를 작성 중입니다..."):
            
            # 전문적인 분석을 위한 프롬프트 (남녀 통합 및 정밀 수치 요청)
            analysis_prompt = """
            당신은 세계적인 비주얼 컨설팅 전문가입니다. 
            첨부된 사진을 보고 아래 항목을 포함한 '프리미엄 퍼스널 리포트'를 HTML 형식으로 작성하세요.
            
            1. 성별 및 전체적인 분위기 분석
            2. 얼굴형 분석: 상안부, 중안부, 하안부의 비율을 1:1:1 기준으로 소수점 단위까지 분석 (예: 1 : 1.2 : 0.9)
            3. 이목구비 분석: 눈 사이 거리, 턱선의 각도, 가로/세로 황금 비율 측정
            4. 퍼스널 컬러 진단: 피부 톤과 어울리는 계절별 컬러 팔레트 제안
            5. 헤어 솔루션: 얼굴형의 단점을 보완하고 장점을 살리는 헤어스타일 3가지 상세 추천
            6. 스타일링 팁: 안경 테 디자인, 메이크업 또는 눈썹 모양 제안
            
            디자인 가이드: 
            - 제목은 <h2> 태그로, 강조할 수치는 <strong> 태그를 사용하세요.
            - 잡지 기사처럼 우아하고 정중한 말투를 유지하세요.
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[analysis_prompt, img]
            )
            
            # 결과 출력
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(response.text, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # PDF 다운로드 모사 (현재는 HTML로 제공)
            st.download_button(
                label="📥 분석 결과 PDF(HTML) 저장하기",
                data=response.text,
                file_name="ADAM_AI_REPORT.html",
                mime="text/html",
            )

