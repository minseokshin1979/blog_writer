"""
블로그 글 작성 프로그램
Streamlit 기반 웹 인터페이스
"""
import streamlit as st
from file_parser import parse_uploaded_file
from web_scraper import scrape_web_content, is_valid_url
from blog_generator import generate_blog_post, validate_api_key
import os


# 페이지 설정
st.set_page_config(
    page_title="AI 블로그 글 작성기",
    page_icon="✍️",
    layout="wide"
)


def main():
    st.title("✍️ AI 블로그 글 작성기")
    st.markdown("---")
    
    # 사이드바 - API 키 입력
    with st.sidebar:
        st.header("⚙️ 설정")
        api_key = st.text_input(
            "Google AI Studio API 키",
            value="AIzaSyC1DzM1t-gMMXZGy0Ugekg90ONIO6h2RS4",
            type="password",
            help="Google AI Studio API 키를 입력해주세요 (https://makersuite.google.com/app/apikey)"
        )
        
        model_option = st.selectbox(
            "모델 선택",
            ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro", "gemini-flash-latest"],
            help="사용할 Gemini 모델을 선택해주세요"
        )
        
        st.markdown("---")
        st.markdown("""
        ### 사용 방법
        1. Google AI Studio API 키 입력
        2. 필수 항목 입력 (키워드)
        3. 선택 항목 입력 (관점, 스타일, 참고자료)
        4. '블로그 글 생성' 버튼 클릭
        5. 생성된 글을 복사하거나 파일로 저장
        """)
    
    # 메인 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 입력 정보")
        
        # 입력 1: 키워드
        keyword = st.text_input(
            "1️⃣ 키워드 (필수)",
            placeholder="예: 인공지능, 건강한 식습관, 여행 팁",
            help="블로그 글의 주제가 될 키워드를 입력해주세요"
        )
        
        # 입력 2: 작성자의 관점
        perspective = st.text_area(
            "2️⃣ 작성자의 관점 (선택)",
            placeholder="예: 초보자 입장에서, 전문가의 시각으로, 실용적인 관점에서",
            help="글을 작성할 때 어떤 관점에서 접근할지 설명해주세요"
        )
        
        # 입력 3: 글의 스타일
        style = st.text_input(
            "3️⃣ 글의 스타일 (선택)",
            placeholder="예: 친근하게, 진지하게, 정중하게, 20대를 위한",
            help="글의 톤과 스타일을 지정해주세요"
        )
        
        # 입력 3-1: 출력 언어
        language = st.selectbox(
            "🌐 출력 언어 (선택)",
            ["한국어", "English", "日本語", "中文", "Español"],
            help="블로그 글이 작성될 언어를 선택해주세요"
        )
        
        # 입력 4: 참고 자료
        st.subheader("4️⃣ 참고 자료 (선택)")
        
        reference_type = st.radio(
            "참고 자료 타입",
            ["없음", "웹 링크", "파일 업로드"],
            horizontal=True
        )
        
        reference_text = ""
        
        if reference_type == "웹 링크":
            web_url = st.text_input(
                "웹 페이지 URL",
                placeholder="https://example.com/article"
            )
            
            if web_url and st.button("웹 내용 가져오기"):
                if is_valid_url(web_url):
                    with st.spinner("웹 페이지 내용을 가져오는 중..."):
                        try:
                            reference_text = scrape_web_content(web_url)
                            st.success(f"✅ 웹 내용을 성공적으로 가져왔습니다 ({len(reference_text)} 글자)")
                            with st.expander("가져온 내용 미리보기"):
                                st.text(reference_text[:500] + "..." if len(reference_text) > 500 else reference_text)
                        except Exception as e:
                            st.error(f"❌ 오류: {str(e)}")
                else:
                    st.error("올바른 URL을 입력해주세요 (http:// 또는 https://로 시작)")
        
        elif reference_type == "파일 업로드":
            uploaded_file = st.file_uploader(
                "파일 선택",
                type=["txt", "pdf", "hwp"],
                help="txt, pdf, hwp 파일을 업로드할 수 있습니다"
            )
            
            if uploaded_file is not None:
                with st.spinner("파일을 읽는 중..."):
                    try:
                        reference_text = parse_uploaded_file(uploaded_file)
                        st.success(f"✅ 파일을 성공적으로 읽었습니다 ({len(reference_text)} 글자)")
                        with st.expander("파일 내용 미리보기"):
                            st.text(reference_text[:500] + "..." if len(reference_text) > 500 else reference_text)
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")
        
        # 세션 상태에 참고 자료 저장
        if reference_text:
            st.session_state['reference_text'] = reference_text
        
        st.markdown("---")
        
        # 생성 버튼
        generate_button = st.button("🚀 블로그 글 생성", type="primary", use_container_width=True)
    
    with col2:
        st.header("📄 생성된 블로그 글")
        
        if generate_button:
            # 유효성 검사
            if not keyword:
                st.error("❌ 키워드를 입력해주세요!")
                return
            
            if not api_key:
                st.error("❌ Google AI Studio API 키를 입력해주세요!")
                return
            
            if not validate_api_key(api_key):
                st.error("❌ 올바른 Google AI Studio API 키를 입력해주세요!")
                return
            
            # 참고 자료 가져오기
            ref_text = st.session_state.get('reference_text', '')
            
            # 블로그 글 생성
            with st.spinner("블로그 글을 생성하는 중... (1-2분 소요될 수 있습니다)"):
                try:
                    blog_post = generate_blog_post(
                        api_key=api_key,
                        keyword=keyword,
                        perspective=perspective,
                        style=style,
                        reference_text=ref_text,
                        language=language,
                        model=model_option
                    )
                    
                    st.session_state['blog_post'] = blog_post
                    st.success("✅ 블로그 글이 성공적으로 생성되었습니다!")
                    
                except Exception as e:
                    st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                    return
        
        # 생성된 글 표시
        if 'blog_post' in st.session_state:
            blog_post = st.session_state['blog_post']
            
            # 탭으로 미리보기와 원본 구분
            tab1, tab2 = st.tabs(["📖 미리보기", "📝 원본 텍스트"])
            
            with tab1:
                st.markdown(blog_post)
            
            with tab2:
                st.text_area(
                    "생성된 글 (복사 가능)",
                    value=blog_post,
                    height=500,
                    label_visibility="collapsed"
                )
            
            # 다운로드 버튼
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.download_button(
                    label="💾 마크다운으로 저장 (.md)",
                    data=blog_post,
                    file_name=f"blog_post_{keyword[:10]}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col_d2:
                st.download_button(
                    label="💾 텍스트로 저장 (.txt)",
                    data=blog_post,
                    file_name=f"blog_post_{keyword[:10]}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # 새 글 작성 버튼
            if st.button("🔄 새로운 글 작성", use_container_width=True):
                del st.session_state['blog_post']
                if 'reference_text' in st.session_state:
                    del st.session_state['reference_text']
                st.rerun()
        
        else:
            st.info("👈 왼쪽에서 정보를 입력하고 '블로그 글 생성' 버튼을 클릭해주세요.")


if __name__ == "__main__":
    main()

