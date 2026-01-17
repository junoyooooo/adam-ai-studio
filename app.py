import streamlit as st
from google import genai
import PIL.Image
import base64

# --- [1. API 및 초기 설정] ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- [2. 럭셔리 디자인 테마 (CSS)] ---
st.set_page_config(page_title="ADAM AI STUDIO", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap');
    
    /* 전체 배경 */
    html, body, [class*="css"] { 
        font-family: 'Pretendard', sans-serif; 
        background-color: #F4F1EE; 
        color: #1A1A1A;
    }
    
    /* 카메라 및 UI 요소 */
    div[data-testid="stCameraInput"] { width: 100% !important; max-width: 900px !important; margin: 0 auto; }
    video { border-radius: 20px; border: 8px solid #FFF; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    
    .main-title { 
        font-family: 'Gilda Display', serif; 
        font-size: 4rem; text-align: center; margin-top: 1rem; 
        letter-spacing: -2px; color: #1A1A1A; 
    }
    .sub-title { 
        font-size: 0.8rem; color: #BC9F8B; text-align: center; 
        margin-bottom: 2rem; letter-spacing: 8px; font-weight: 700; 
    }
    
    /* 버튼 디자인 */
    .stButton>button { 
        width: 100%; border-radius: 0px; background: #1A1A1A; color: #FFF; 
        border: none; padding: 25px; font-weight: 700; font-size: 1.2rem; 
        letter-spacing: 2px; transition: 0.4s; margin-top: 20px;
    }
    .stButton>button:hover { background: #BC9F8B; color: #FFF; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">ADAM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI PERSONAL ANALYSIS</div>', unsafe_allow_html=True)

# --- [3. 사진 입력] ---
img_file = st.camera_input("")
uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
if uploaded_file: img_file = uploaded_file

# --- [4. AI 분석 및 고해상도 리포트 생성] ---
if img_file:
    img = PIL.Image.open(img_file)
    if st.button("GENERATE PREMIUM REPORT"):
        with st.spinner("전문 AI 어드바이저가 리포트를 큐레이팅 중입니다..."):
            
            # [수정된 프롬프트] - 분량 확대 및 디자인 강화
            analysis_prompt = """
            당신은 세계 최고의 패션 매거진 에디터이자 비주얼 컨설턴트입니다. 
            서론 없이 오직 <div class='magazine-report'>로 시작하는 완벽한 HTML 본문만 출력하세요. 
            분량은 각 섹션당 매우 구체적이고 전문적인 용어를 사용하여 기존의 2배 이상 작성하세요.

            [디자인 지침]:
            1. 잡지 내지 디자인처럼 여백과 폰트 크기 대비를 크게 할 것.
            2. 테마 색상: Charcoal(#1A1A1A), Sand Beige(#BC9F8B), Off White(#FFFFFF).
            3. 차트: HTML/CSS로 구현한 정밀한 프로그레스 바와 컬러 칩 활용.
            4. 출력 시 깨짐 방지를 위해 반드시 <meta charset='UTF-8'>를 최상단에 포함할 것.

            [분석 필수 내용]:
            - [Editorial Mood]: 고객의 이목구비가 주는 인상과 심리적 이미지 분석 (최소 5문장)
            - [Structural Analysis]: 상/중/하안부 비율 및 광대, 턱선의 골격적 특징 정밀 분석 (수치 포함)
            - [Color Palette]: 피부 톤의 RGB 추정 및 어울리는 컬러 칩 5개 제시
            - [Hair Styling Curating]: 얼굴형 보완을 위한 맞춤 헤어 3가지를 전문가적 관점에서 매우 상세히 설명 (커트 선, 볼륨 위치 등)
            - [Lifestyle Advice]: 안경, 네크라인, 향후 스타일링 방향성 제안
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[analysis_prompt, img]
            )
            
            # HTML 정제 (에러 방지 및 한글 깨짐 방지 처리)
            raw_html = response.text.replace("```html", "").replace("```", "").strip()
            
            # 한글 깨짐 방지를 위한 메타 태그 및 스타일 강제 주입
            final_report_html = f"""
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap');
                .magazine-report {{ 
                    background: white; padding: 60px 50px; border: 1px solid #EEE; 
                    font-family: 'Pretendard', sans-serif; color: #1A1A1A; max-width: 800px; margin: 0 auto;
                }}
                .magazine-report h2 {{ font-family: 'Gilda Display', serif; font-size: 2.5rem; border-bottom: 2px solid #1A1A1A; padding-bottom: 10px; margin-top: 40px; }}
                .magazine-report p {{ font-size: 1.1rem; line-height: 2; margin-bottom: 20px; text-align: justify; }}
                .highlight {{ color: #BC9F8B; font-weight: bold; }}
                .bar-container {{ background: #F4F1EE; border-radius: 5px; height: 12px; width: 100%; margin: 10px 0; }}
                .bar-fill {{ background: #1A1A1A; height: 100%; border-radius: 5px; }}
                .color-chip {{ width: 60px; height: 60px; border-radius: 50%; display: inline-block; margin-right: 15px; border: 1px solid #EEE; }}
            </style>
            <div class="magazine-report">
                {raw_html}
            </div>
            """
            
            # 화면 출력
            st.markdown(final_report_html, unsafe_allow_html=True)
            
            # 파일 다운로드 (BOM 추가로 한글 깨짐 방지)
            bom_html = "\ufeff" + final_report_html
            st.download_button(
                label="📥 DOWNLOAD DIGITAL MAGAZINE (HTML)",
                data=bom_html.encode('utf-8'),
                file_name="ADAM_MAGAZINE_REPORT.html",
                mime="text/html",
            )
