import streamlit as st
import validator

st.set_page_config(page_title="단상자 - CFS 오류 검토 시스템", layout="wide")

st.title("📦 단상자 ↔ CFS 오류 검토 자동화 시스템")
st.markdown("단상자 파일(PDF/이미지)과 CFS(자유판매증명서 PDF)를 업로드하여 제조사, 책임판매업자, 주소 및 오타를 자동으로 비교합니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ 단상자 파일 업로드")
    box_file = st.file_uploader("단상자 PDF 또는 이미지 선택", type=["pdf", "png", "jpg", "jpeg"])

with col2:
    st.subheader("2️⃣ CFS 문서 업로드")
    cfs_file = st.file_uploader("CFS PDF 문서 선택", type=["pdf"])

if box_file and cfs_file:
    st.divider()
    st.subheader("🔍 검토 결과 리포트")
    
    # CFS 텍스트 추출
    cfs_text = validator.extract_text_from_pdf(cfs_file)
    
    # 단상자 텍스트 추출 (PDF 처리 예시)
    if box_file.type == "application/pdf":
        box_text = validator.extract_text_from_pdf(box_file)
    else:
        st.info("이미지 OCR 추출 기능 적용 영역입니다.")
        box_text = ""

    col_box, col_cfs = st.columns(2)
    with col_box:
        st.markdown("**[단상자 추출 텍스트]**")
        st.text_area("Box Text", box_text, height=200)

    with col_cfs:
        st.markdown("**[CFS 추출 텍스트]**")
        st.text_area("CFS Text", cfs_text, height=200)

    # 단순 비교 예시
    if box_text and cfs_text:
        result = validator.compare_texts(box_text, cfs_text)
        
        st.markdown("### 📊 정밀 대조 결과")
        st.metric(label="텍스트 일치 유사도", value=f"{result['similarity']}%")
        
        if result['exact_match']:
            st.success("✅ 대소문자 및 문장부호까지 완벽하게 일치합니다.")
        elif result['normalized_match']:
            st.warning("⚠️ 텍스트 내용은 일치하나, 대소문자 또는 쉼표/하이픈/공백 차이가 존재합니다.")
        else:
            st.error("❌ 주소 또는 법인명 스펠링 불일치(오타)가 감지되었습니다. 상세 확인이 필요합니다.")
