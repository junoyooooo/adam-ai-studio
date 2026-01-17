import streamlit as st
from google import genai
import PIL.Image
import re

# --- [1. API 설정] ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'를 등록해 주세요.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- [2. 레이아웃 및 디자인 (CSS)] ---
st.set_page_config(page_title="ADAM AI STUDIO", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Pretendard', sans-serif; 
        background-color: #F8F6F2; 
        color: #1A1A1A;
    }
    
    /* 카메라 화면 확대 및 좌우 반전 수정 */
    div[data-testid="stCameraInput"] { width: 100% !important; max-width: 900px !important; margin: 0 auto; }
    video { 
        border-radius: 20px; 
        border: 10px solid #FFF; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.1); 
        transform: scaleX(-1); /* 실물처럼 보이게 좌우 반전 */
    }
    
    .main-title { 
        font-family: 'Gilda Display', serif; 
        font-size: 4rem; text-align: center; margin-top: 1rem; 
        letter-spacing: -2px; color: #1A1A1A; 
    }
    .sub-title { 
        font-size: 0.8rem; color: #BC9F8B; text-align: center; 
        margin-bottom: 2rem; letter-spacing: 8px; font-weight: 700; text-transform: uppercase;
    }
    
    .stButton>button { 
        width: 100%; border-radius: 0px; background: #1A1A1A; color: #FFF; 
        border: none; padding: 22px; font-weight: 700; font-size: 1.2rem; 
        letter-spacing: 2px; transition: 0.4s; margin-top: 20px;
    }
    .stButton>button:hover { background: #BC9F8B; color: #FFF; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">ADAM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI VISUAL CONSULTING</div>', unsafe_allow_html=True)

# --- [3. 사진 입력] ---
img_file = st.camera_input("")
uploaded_file = st.file_uploader("이미지 업로드", type=['jpg', 'png', 'jpeg'])
if uploaded_file: img_file = uploaded_file

# --- [4. AI 분석 및 고해상도 리포트 생성] ---
if img_file:
    img = PIL.Image.open(img_file)
    if st.button("✨ 프리미엄 매거진 리포트 발행"):
        with st.spinner("전문 에디터가 한국어로 상세 리포트를 작성 중입니다..."):
            
            # [강력한 한글 프롬프트] - 서론 금지 및 한국어 전용 지시
            analysis_prompt = """
            당신은 세계적인 럭셔리 뷰티 매거진의 편집장입니다. 
            반드시 모든 분석 내용을 '한국어'로만 작성하세요. 영어 제목이나 설명을 절대 쓰지 마세요.
            서론(알겠습니다 등)이나 ```html 같은 마크다운 기호 없이 오직 <div>로 시작하는 HTML 본문만 출력하세요. 
            분량은 각 항목당 최소 10문장 이상, 매우 상세하고 전문적인 한국어 용어로 작성하세요.

            [디자인 가이드]:
            - 배경은 순백색(#FFFFFF), 포인트 컬러는 샌드 베이지(#BC9F8B).
            - 각 섹션은 <h2> 태그로 시작하고, 잡지 내지처럼 여백을 충분히 줄 것.
            - 얼굴 비율(상/중/하안부)은 1:1.1:0.9와 같은 정밀 수치와 함께 반드시 CSS 막대 그래프로 표현할 것.
            - 퍼스널 컬러는 5개의 동그란 색상 칩으로 시각화할 것.

            [리포트 필수 구성 (모두 한국어로)]:
            1. [이미지 무드 분석]: 고객이 풍기는 전체적인 분위기와 첫인상을 아주 세밀하게 묘사 (10문장 이상)
            2. [골격 구조 분석]: 상/중/하안부의 정밀 비율과 광대, 턱선, 이마 볼륨의 특징을 전문가적 시각으로 분석
            3. [퍼스널 컬러 전략]: 피부 톤의 미세한 차이를 분석하고 가장 고급스러운 배색 전략 제안
            4. [맞춤형 헤어 디자인]: 얼굴형의 단점을 보완할 3가지 스타일을 커트 방식과 볼륨 위치까지 상세히 설명
            5. [토털 스타일링 팁]: 안경 테, 넥라인, 주얼리 등 전반적인 스타일 조언
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[analysis_prompt, img]
            )
            
            # HTML 정제 (에러 코드 방지)
            html_content = response.text
            html_content = re.sub(r'```html', '', html_content)
            html_content = re.sub(r'```', '', html_content).strip()
            
            # 한글 깨짐 방지 및 잡지 디자인 래핑
            final_html = f"""
            <meta charset="UTF-8">
            <style>
                @import url('[https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap](https://fonts.googleapis.com/css2?family=Gilda+Display&family=Pretendard:wght@300;400;700&display=swap)');
                .magazine-body {{ 
                    background: white; padding: 70px 50px; border: 1px solid #EEE; 
                    font-family: 'Pretendard', sans-serif; color: #1A1A1A; line-height: 2.2;
                    max-width: 800px; margin: 30px auto; box-shadow: 0 50px 100px rgba(0,0,0,0.05);
                    text-align: justify;
                }}
                .magazine-body h2 {{ font-family: 'Gilda Display', serif; font-size: 2.8rem; border-bottom: 3px solid #1A1A1A; padding-bottom: 15px; margin-top: 60px; color: #1A1A1A; }}
                .magazine-body p {{ font-size: 1.15rem; margin-bottom: 30px; }}
                .gold {{ color: #BC9F8B; font-weight: bold; }}
                .bar-container {{ background: #F4F1EE; height: 15px; width: 100%; border-radius: 0px; margin: 15px 0; }}
                .bar-fill {{ background: #1A1A1A; height: 100%; }}
                .chip-group {{ display: flex; gap: 20px; margin: 25px 0; }}
                .color-chip {{ width: 65px; height: 65px; border-radius: 50%; border: 1px solid #EEE; }}
            </style>
            <div class="magazine-body">
                <div style="text-align:right; color:#BC9F8B; font-weight:bold; letter-spacing:4px; font-size:0.8rem;">ADAM AI VISUAL REPORT</div>
                {html_content}
                <div style="margin-top:120px; text-align:center; border-top:1px solid #EEE; padding-top:40px; font-family:'Gilda Display', serif; color:#AAA; font-size:1.1rem;">
                    CONSULTED BY ADAM AI STUDIO
                </div>
            </div>
            """
            
            # 화면 출력
            st.markdown(final_html, unsafe_allow_html=True)
            
            # 다운로드 버튼 (한글 깨짐 방지 BOM 추가)
            bom_html = "\ufeff" + final_html
            st.download_button(
                label="📥 프리미엄 매거진 리포트 저장 (HTML)",
                data=bom_html.encode('utf-8'),
                file_name="ADAM_PREMIUM_REPORT.html",
                mime="text/html",
            )
