import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

from data_collector import KRXDataCollector
from data_processor import DataProcessor
from utils import format_date, get_last_business_day, validate_inputs

# 페이지 설정
st.set_page_config(
    page_title="KRX 주식 데이터 분석",
    page_icon="📈",
    layout="wide"
)

# 제목
st.title("KRX 주식 데이터 분석")

# 사이드바 - 입력 파라미터
st.sidebar.header("검색 조건")

# 날짜 선택 (오늘 날짜로 기본 설정)
today = datetime.now().date()
selected_date = st.sidebar.date_input(
    "날짜 선택",
    value=today,
    max_value=today,
    min_value=datetime(2020, 1, 1).date()
)

# 최소 종가 입력 (정수만)
min_price = st.sidebar.number_input(
    "최소 종가",
    min_value=0,
    value=1000,
    step=100,
    format="%d"  # 정수 형식으로 표시
)

# 최소 거래량 입력
min_volume = st.sidebar.number_input(
    "최소 거래량",
    min_value=0,
    value=10000,
    step=1000
)

# 최소 등락률 입력 (정수만)
min_change_rate = st.sidebar.number_input(
    "최소 등락률",
    min_value=0,
    value=1,
    step=1,
    format="%d"  # 정수 형식으로 표시
)

# 데이터 수집 및 처리
if st.sidebar.button("데이터 조회"):
    # 입력값 검증
    is_valid, error_message = validate_inputs(min_price, min_volume, min_change_rate)
    
    if not is_valid:
        st.error(error_message)
    else:
        with st.spinner("데이터를 수집하고 있습니다..."):
            # 데이터 수집
            collector = KRXDataCollector()
            date_str = format_date(selected_date)
            df = collector.get_stock_data(date_str)
            
            if df.empty:
                st.error("데이터를 수집하는 중 오류가 발생했습니다.")
            else:
                # 데이터 필터링
                processor = DataProcessor()
                filtered_df = processor.filter_data(df, min_price, min_volume, min_change_rate)
                
                if filtered_df.empty:
                    st.warning("조건에 맞는 데이터가 없습니다.")
                else:
                    # 결과 표시
                    st.subheader("필터링된 결과")
                    st.write(f"검색 결과: {len(filtered_df)}개 종목 (등락률 > {min_change_rate}%인 종목 중에서 검색)")
                    st.dataframe(
                        filtered_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # CSV 다운로드 버튼
                    csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="CSV 다운로드",
                        data=csv,
                        file_name=f"krx_data_{date_str}.csv",
                        mime="text/csv"
                    )

# 사용 방법 안내
with st.expander("사용 방법"):
    st.markdown("""
    1. 왼쪽 사이드바에서 날짜를 선택합니다.
    2. 최소 종가를 입력합니다.
    3. 최소 거래량을 입력합니다.
    4. 최소 등락률을 입력합니다.
    5. '데이터 조회' 버튼을 클릭합니다.
    6. 필터링된 결과가 표시됩니다.
    7. 'CSV 다운로드' 버튼을 클릭하여 데이터를 저장합니다.
    """) 