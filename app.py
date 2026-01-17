import streamlit as st
from google import genai
import PIL.Image

# --- [1. API 설정] ---
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# --- [2. UI/UX 디자인 (카메라 확대 및 프리미엄 테마)] ---
# layout="wide"를 설정하여 화면을 더 넓게 씁니다.
st.set_page_config(page_title="ADAM AI STUDIO", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;700&display=swap');
    
    /* 전체 배경 및 폰트 */
    html, body, [class*="css"] { 
        font-family: 'Pretendard', sans-serif; 
        background-color: #F8F6F2; 
    }
    
    /* 카메라 화면 크기 강제 확대 */
    div[data-testid="stCameraInput"] {
        width: 100% !important;
        max-width: 1000px !important; /* 카메라를 훨씬 크게 만듭니다 */
        margin: 0 auto;
    }
    
    /* 카메라 내부 영상 둥글게 */
    video {
        border-radius: 24px;
        border: 4px solid #FFF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .main-title { font-size: 3rem; font-weight: 700; color: #1A1A1A; text-align: center; margin-top: 1rem; letter-spacing: -2px; }
    .sub-title { font-size: 0.9rem; color: #BC9F8B; text-align: center; margin-bottom: 2rem; letter-spacing: 6px; font-weight: 700; }
    
    /* 버튼 디자인 */
    .stButton>button { 
        width: 100%; border-radius: 14px; background: #1A1A1A; color: #FFF; 
        border: none; padding: 22px; font-weight: 700; font-size: 1.2rem; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.15); transition: all 0.3s;
        margin-top: 10px;
    }
    .stButton>button:hover { background: #444; transform: translateY(-3px); }

    /* 결과 리포트 컨테이너 */
    .report-container { 
        background: white; border-radius: 35px; padding: 60px 45px; 
        box-shadow: 0 40px 80px rgba(0,0,0,0.06); margin-top: 40px;
        border: 1px solid #F0EBE3; line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">ADAM AI STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">PREMIUM ANALYSIS SERVICE</div>', unsafe_allow_html=True)

# --- [3. 카메라 입력 (크기 대폭 확대)] ---
st.markdown("<h3 style='text-align:center; color:#555; font-size:1.1rem;'>고객님의 정면을 촬영해 주세요</h3>", unsafe_allow_html=True)
img_file = st.camera_input("") # CSS에서 확대한 크기가 적용됩니다.

# --- [4. AI 분석 및 고퀄리티 리포트 생성] ---
if img_file:
    img = PIL.Image.open(img_file)
    
    if st.button("✨ 초정밀 퍼스널 진단 리포트 발행"):
        with st.spinner("전문 AI가 골격과 컬러를 분석 중입니다..."):
            
            analysis_prompt = """
            서론(알겠습니다 등)은 절대 하지 말고, 오직 <div class='report-container'>로 시작하는 세련된 HTML 리포트 본문만 출력하세요.

            [디자인 필수사항]:
            1. 현대적인 뷰티 매거진 레이아웃.
            2. 얼굴 비율 분석: <div style='background:#eee; border-radius:10px; height:20px; width:100%;'>와 같은 HTML/CSS 막대 그래프를 활용하여 상/중/하안부 비율을 시각화할 것.
            3. 퍼스널 컬러: 분석된 컬러를 <div style='background:색상코드; width:50px; height:50px; border-radius:50%; display:inline-block;'> 형태의 예쁜 원형 칩으로 보여줄 것.
            4. 텍스트 강조: 중요 수치는 골드톤(#BC9F8B) 글자색과 굵은 글씨를 사용할 것.

            [분석 필수사항]:
            - 성별 및 이미지 무드 분석
            - 얼굴 삼등분 비율 (상:중:하) 정밀 수치
            - 추천 헤어스타일 TOP 3 (각 스타일별 포인트 설명)
            - 어울리는 패션 아이템(안경, 네크라인 등) 추천
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[analysis_prompt, img]
            )
            
            # HTML 정제 (마크다운 기호 제거)
            final_html = response.text.replace("```html", "").replace("```", "").strip()
            
            # 결과 출력
            st.markdown(final_html, unsafe_allow_html=True)
            
            # 저장 버튼
            st.download_button(
                label="📥 진단서 PDF 저장 (HTML)",
                data=final_html,
                file_name="ADAM_AI_REPORT.html",
                mime="text/html",
            )
