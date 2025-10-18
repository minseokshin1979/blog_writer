"""
웹 스크래핑 모듈 - 웹 링크에서 텍스트 추출
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_web_content(url: str) -> str:
    """
    웹 페이지에서 본문 텍스트 추출
    """
    try:
        # User-Agent 헤더 추가 (일부 사이트의 차단 방지)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 인코딩 설정
        response.encoding = response.apparent_encoding
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 스크립트, 스타일 태그 제거
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # 본문 텍스트 추출 시도
        text = ""
        
        # 일반적인 본문 컨테이너 찾기
        article_tags = ['article', 'main', 'div[class*="content"]', 'div[class*="article"]', 
                       'div[id*="content"]', 'div[id*="article"]']
        
        for tag in article_tags:
            content = soup.select_one(tag)
            if content:
                text = content.get_text(separator='\n', strip=True)
                if len(text) > 100:  # 충분한 텍스트가 있으면 사용
                    break
        
        # 본문을 찾지 못한 경우 body 전체 사용
        if not text or len(text) < 100:
            body = soup.find('body')
            if body:
                text = body.get_text(separator='\n', strip=True)
        
        # 빈 줄 정리
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        if not text:
            raise Exception("웹 페이지에서 텍스트를 추출할 수 없습니다.")
        
        return text
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"웹 페이지 로딩 오류: {str(e)}")
    except Exception as e:
        raise Exception(f"웹 스크래핑 오류: {str(e)}")


def is_valid_url(url: str) -> bool:
    """
    유효한 URL인지 확인
    """
    return url.startswith('http://') or url.startswith('https://')

