import re
from pdf2image import convert_from_bytes
import pytesseract
from Levenshtein import ratio

def extract_text_from_pdf(pdf_file):
    """PDF 파일을 이미지로 변환한 뒤 OCR을 통해 정확한 텍스트 추출"""
    try:
        # PDF 파일을 이미지 리스트로 변환 (poppler 필요)
        images = convert_from_bytes(pdf_file.read())
        extracted_text = ""
        
        for image in images:
            # OCR을 이용해 이미지 내 텍스트 추출 (영어/숫자 기준)
            text = pytesseract.image_to_string(image, lang='eng')
            extracted_text += text + "\n"
            
        return extracted_text.strip()
    except Exception as e:
        # poppler가 설치되지 않은 로컬 환경 등의 예외 처리 시 기존 방식 Fallback
        return f"OCR 추출 오류: {str(e)}"

def normalize_text(text):
    """비교를 위한 공백 및 특수문자 정규화"""
    text_clean = re.sub(r'[\,\.\-\_]', ' ', text)  
    text_clean = re.sub(r'\s+', ' ', text_clean)    
    return text_clean.strip().upper()

def compare_texts(box_text, cfs_text):
    """단상자 텍스트와 CFS 텍스트 글자 단위/유사도 비교"""
    norm_box = normalize_text(box_text)
    norm_cfs = normalize_text(cfs_text)
    
    similarity = round(ratio(norm_box, norm_cfs) * 100, 2)
    
    exact_match = (box_text.strip() == cfs_text.strip())
    ignore_case_match = (box_text.strip().lower() == cfs_text.strip().lower())
    normalized_match = (norm_box == norm_cfs)
    
    return {
        "exact_match": exact_match,
        "ignore_case_match": ignore_case_match,
        "normalized_match": normalized_match,
        "similarity": similarity
    }
