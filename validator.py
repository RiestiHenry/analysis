import re
from pypdf import PdfReader
from Levenshtein import ratio

def extract_text_from_pdf(pdf_file):
    """PDF 파일에서 텍스트 추출"""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

def normalize_text(text):
    """비교를 위한 공백 및 특수문자 정규화"""
    text_clean = re.sub(r'[\,\.\-\_]', ' ', text)  # 특수문자를 공백으로 변환
    text_clean = re.sub(r'\s+', ' ', text_clean)    # 연속 공백을 하나로
    return text_clean.strip().upper()

def compare_texts(box_text, cfs_text):
    """단상자 텍스트와 CFS 텍스트 글자 단위/유사도 비교"""
    norm_box = normalize_text(box_text)
    norm_cfs = normalize_text(cfs_text)
    
    # 레벤슈타인 거리 기반 유사도 계산 (0 ~ 100%)
    similarity = round(ratio(norm_box, norm_cfs) * 100, 2)
    
    exact_match = (box_text.strip() == cfs_text.strip())
    ignore_case_match = (box_text.strip().lower() == cfs_text.strip().lower())
    normalized_match = (norm_box == norm_cfs)
    
    return {
        "exact_match": exact_match,             # 완전히 일치 (대소문자, 문장부호 포함)
        "ignore_case_match": ignore_case_match, # 대소문자 무시 일치
        "normalized_match": normalized_match,   # 문장부호/공백 무시 일치
        "similarity": similarity                 # 유사도 퍼센트
    }
