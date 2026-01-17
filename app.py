import streamlit as st
from google import genai
import PIL.Image

# --- [1. API 및 초기 설정] ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- [2. 럭셔리 매거진 디자인 및 카메라 반전 해결 (CSS)] ---
st.set_page_config(page_title="ADAM AI STUDIO", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap');
    
    /* 전체 배경 */
    html, body, [class*="css"] { 
        font-family: 'Pretendard', sans-serif; 
        background-color: #F8F6F2; 
        color: #1A1A1A;
    }
    
    /* 카메라 좌우 반전 고정 및 크기 확대 */
    div[data-testid="stCameraInput"] { width: 100% !important; max-width: 900px !important; margin: 0 auto; }
    video { 
        border-radius: 30px; 
        border: 12px solid #FFF; 
        box-shadow: 0 30px 60px rgba(0,0,0,0.12); 
        transform: scaleX(-1); /* 좌우 반전 해결 (거울 모드 해제) */
    }
    
    .main-title { 
        font-family: 'Gilda Display', serif; 
        font-size: 4.5rem; text-align: center; margin-top: 2rem; 
        letter-spacing: -3px; color: #1A1A1A; 
    }
    .sub-title { 
        font-size: 0.8rem; color: #BC9F8B; text-align: center; 
        margin-bottom: 3rem; letter-spacing: 10px; font-weight: 700; text-transform: uppercase;
    }
    
    /* 버튼 디자인 */
    .stButton>button { 
        width: 100%; border-radius: 0px; background: #1A1A1A; color: #FFF; 
        border: none; padding: 25px; font-weight: 700; font-size: 1.3rem; 
        letter-spacing: 3px; transition: 0.5s; margin-top: 30px;
    }
    .stButton>button:hover { background: #BC9F8B; color: #FFF; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">ADAM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Visual Consulting Studio</div>', unsafe_allow_html=True)

# --- [3. 사진 입력] ---
img_file = st.camera_input("")
uploaded_file = st.file_uploader("Upload Profile Image", type=['jpg', 'png', 'jpeg'])
if uploaded_file: img_file = uploaded_file

# --- [4. AI 분석 및 고해상도 매거진 리포트 생성] ---
if img_file:
    img = PIL.Image.open(img_file)
    if st.button("GENERATE MASTERPIECE REPORT"):
        with st.spinner("비주얼 에디터가 정밀 분석 리포트를 큐레이팅 중입니다..."):
            
            # [수정된 프롬프트] - 분량 2배, 초정밀 전문 용어, 완벽한 디자인 요청
            analysis_prompt = """
            당신은 전 세계 1%를 위한 퍼스널 브랜딩 전문가이자 'Vogue' 매거진의 수석 에디터입니다.
            서론 없이 오직 <div class='magazine-report'>로 시작하는 완벽한 HTML 본문만 출력하세요. 
            분량은 각 섹션당 매우 구체적이고 전문적인 스타일 용어를 사용하여 기존보다 2배 이상 길게 작성하세요.

            [디자인 지침]:
            1. 잡지 화보 시안처럼 레이아웃을 구성할 것.
            2. 테마 색상: Charcoal(#1A1A1A), Muted Sand(#BC9F8B), Cloud White(#FFFFFF).
            3. 차트: HTML/CSS로 구현한 'Facial Ratio Chart'와 'Chromatology Palette' 5개를 포함할 것.
            4. 텍스트: 강렬한 헤드라인과 섬세한 본문 폰트 대비를 강조할 것.

            [분석 필수 내용]:
            - [01. Archetype Mood]: 고객의 이목구비 골격이 주는 심리적, 시각적 아우라 분석 (최소 10문장 이상)
            - [02. Facial Architecture]: 상/중/하안부의 황금 비율 대비 현재 수치를 0.1단위로 분석하고, 골격적 특징(광대, 턱선, 이마의 볼륨감)을 매우 상세히 서술
            - [03. Chromatic Strategy]: 피부 톤의 언더톤(Warm/Cool/Neutral)을 심층 분석하고, 가장 럭셔리해 보이는 컬러 칩 5개와 그 활용법 제시
            - [04. Hair Design Curating]: 얼굴형의 단점을 100% 소멸시키는 마법 같은 헤어스타일 3가지를 커트 선, 층의 높이, 질감 처리 방식까지 전문가 수준으로 제안
            - [05. Final Styling Advice]: 어울리는 주얼리 소재, 안경 테의 굵기, 넥라인 디자인까지 제안
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[analysis_prompt, img]
            )
            
            # HTML 정제 (에러 방지 및 한글 깨짐 방지)
            raw_html = response.text.replace("```html", "").replace("```", "").strip()
            
            # 마스터피스 리포트 HTML 구조 (BOM 및 Meta 태그 포함)
            final_report_html = f"""
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap');
                .magazine-report {{ 
                    background: #FFF; padding: 80px 60px; border: 1px solid #EAEAEA; 
                    font-family: 'Pretendard', sans-serif; color: #1A1A1A; max-width: 850px; margin: 0 auto;
                    box-shadow: 0 50px 100px rgba(0,0,0,0.05);
                }}
                .magazine-report h2 {{ font-family: 'Gilda Display', serif; font-size: 3rem; border-bottom: 3px solid #1A1A1A; padding-bottom: 15px; margin-top: 60px; letter-spacing: -1px; }}
                .magazine-report p {{ font-size: 1.15rem; line-height: 2.2; margin-bottom: 25px; text-align: justify; color: #444; }}
                .highlight {{ color: #BC9F8B; font-weight: 700; }}
                .bar-container {{ background: #F4F1EE; border-radius: 0px; height: 15px; width: 100%; margin: 15px 0; overflow: hidden; }}
                .bar-fill {{ background: #1A1A1A; height: 100%; }}
                .color-palette {{ display: flex; gap: 20px; margin: 30px 0; }}
                .color-chip {{ width: 70px; height: 70px; border-radius: 50%; border: 1px solid #EEE; }}
                .hair-card {{ border-left: 5px solid #BC9F8B; padding-left: 25px; margin: 40px 0; }}
            </style>
            <div class="magazine-report">
                <div style="text-align:right; font-weight:700; letter-spacing:3px; color:#BC9F8B;">VOL. 2026 ISSUE 01</div>
                {raw_html}
                <div style="margin-top:100px; text-align:center; font-family:'Gilda Display', serif; font-size:1.2rem; border-top:1px solid #EEE; padding-top:30px;">
                    CONSULTED BY ADAM AI STUDIO
                </div>
            </div>
            """
            
            # 화면 출력
            st.markdown(final_report_html, unsafe_allow_html=True)
            
            # 한글 깨짐 방지 다운로드 (BOM 추가)
            bom_html = "\ufeff" + final_report_html
            st.download_button(
                label="📥 DOWNLOAD MASTERPIECE MAGAZINE (HTML)",
                data=bom_html.encode('utf-8'),
                file_name="ADAM_MASTERPIECE_REPORT.html",
                mime="text/html",
            )
