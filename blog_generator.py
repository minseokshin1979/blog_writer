"""
블로그 글 생성 모듈 - Google Gemini API를 이용한 블로그 글 작성
"""
import google.generativeai as genai
from typing import Optional


def generate_blog_post(
    api_key: str,
    keyword: str,
    perspective: str = "",
    style: str = "",
    reference_text: str = "",
    language: str = "한국어",
    model: str = "gemini-2.5-flash"
) -> str:
    """
    Google Gemini API를 사용하여 블로그 글 생성
    
    Args:
        api_key: Google AI Studio API 키
        keyword: 블로그 주제 키워드
        perspective: 작성자의 관점
        style: 글의 스타일
        reference_text: 참고 자료 텍스트
        language: 출력 언어 (기본값: 한국어)
        model: 사용할 모델 (기본값: gemini-2.5-flash)
    
    Returns:
        생성된 블로그 글
    """
    try:
        # Gemini API 설정
        genai.configure(api_key=api_key)
        
        # 모델 초기화
        model_instance = genai.GenerativeModel(model)
        
        # 언어별 시스템 메시지
        language_instructions = {
            "한국어": "한국어로 작성해주세요.",
            "English": "Please write in English.",
            "日本語": "日本語で書いてください。",
            "中文": "请用中文写作。",
            "Español": "Por favor, escribe en español."
        }
        
        # 프롬프트 구성
        prompt_parts = [
            "당신은 전문적인 블로그 글 작성자입니다.",
            "사용자가 제공하는 정보를 바탕으로 구조화되고 흥미로운 블로그 글을 작성해주세요.",
            "글은 서론, 본론, 결론의 구조를 가지며, 읽기 쉽고 유익한 내용이어야 합니다.\n",
            f"다음 키워드에 대한 블로그 글을 작성해주세요: {keyword}",
            f"\n출력 언어: {language_instructions.get(language, language_instructions['한국어'])}"
        ]
        
        if perspective:
            prompt_parts.append(f"\n작성자의 관점: {perspective}")
        
        if style:
            prompt_parts.append(f"\n글의 스타일: {style}")
        
        if reference_text:
            # 참고 자료가 너무 길면 잘라내기 (토큰 제한)
            max_ref_length = 3000
            if len(reference_text) > max_ref_length:
                reference_text = reference_text[:max_ref_length] + "..."
            prompt_parts.append(f"\n\n참고 자료:\n{reference_text}")
        
        prompt_parts.append(f"""

블로그 글 작성 요구사항:
1. 제목을 포함해주세요 (# 제목 형식)
2. 서론, 본론, 결론 구조로 작성해주세요
3. 적절한 문단 구분을 해주세요
4. 가독성 있게 작성해주세요
5. 2000자 이상의 내용으로 작성해주세요
6. 마크다운 형식으로 작성해주세요
7. 반드시 {language}로 작성해주세요
""")
        
        prompt = '\n'.join(prompt_parts)
        
        # API 호출
        response = model_instance.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 8192,
            }
        )
        
        blog_post = response.text
        return blog_post
        
    except Exception as e:
        raise Exception(f"블로그 글 생성 오류: {str(e)}")


def validate_api_key(api_key: str) -> bool:
    """
    API 키 유효성 검사
    """
    if not api_key or len(api_key) < 30:
        return False
    return True

