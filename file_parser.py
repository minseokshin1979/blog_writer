"""
파일 파싱 모듈 - txt, pdf, hwp 파일에서 텍스트 추출
"""
import os
from typing import Optional
import PyPDF2
import olefile


def read_txt_file(file_path: str) -> str:
    """
    텍스트 파일 읽기
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # utf-8로 읽기 실패시 cp949 (한글 인코딩) 시도
        with open(file_path, 'r', encoding='cp949') as f:
            return f.read()


def read_pdf_file(file_path: str) -> str:
    """
    PDF 파일에서 텍스트 추출
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF 파일 읽기 오류: {str(e)}")


def read_hwp_file(file_path: str) -> str:
    """
    HWP 파일에서 텍스트 추출
    HWP 5.0 이상 형식 지원 (ole 기반)
    """
    try:
        if not olefile.isOleFile(file_path):
            raise Exception("지원하지 않는 HWP 파일 형식입니다.")
        
        ole = olefile.OleFileIO(file_path)
        
        # HWP 파일 내 텍스트 스트림 찾기
        text_list = []
        
        # 섹션별로 텍스트 추출
        for stream in ole.listdir():
            stream_name = '/'.join(stream)
            
            # BodyText로 시작하는 스트림이 본문 텍스트
            if stream_name.startswith('BodyText'):
                try:
                    data = ole.openstream(stream).read()
                    # HWP는 UTF-16LE 인코딩 사용
                    # 텍스트만 추출 (간단한 방법)
                    decoded = data.decode('utf-16le', errors='ignore')
                    # 제어 문자 제거
                    cleaned = ''.join(char for char in decoded if char.isprintable() or char in ['\n', '\r', '\t', ' '])
                    text_list.append(cleaned)
                except:
                    continue
        
        ole.close()
        
        full_text = '\n'.join(text_list)
        return full_text.strip() if full_text else "텍스트를 추출할 수 없습니다."
        
    except Exception as e:
        raise Exception(f"HWP 파일 읽기 오류: {str(e)}")


def parse_file(file_path: str) -> str:
    """
    파일 확장자에 따라 적절한 파서 선택
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        return read_txt_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    elif ext in ['.hwp', '.hwpx']:
        return read_hwp_file(file_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")


def parse_uploaded_file(uploaded_file) -> str:
    """
    Streamlit 업로드 파일 객체에서 텍스트 추출
    """
    # 임시 파일로 저장
    temp_path = f"temp_{uploaded_file.name}"
    
    try:
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        text = parse_file(temp_path)
        return text
    finally:
        # 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)

