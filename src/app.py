import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_collector import KRXDataCollector
from data_processor import DataProcessor
from utils import format_date, get_default_date, format_number

# 페이지 설정
st.set_page_config(
    page_title="KRX 주식 데이터 분석",
    page_icon="📈",
    layout="wide"
)

# 세션 상태 초기화
if 'should_refresh' not in st.session_state:
    st.session_state['should_refresh'] = False
if 'last_date' not in st.session_state:
    st.session_state['last_date'] = None
if 'last_price' not in st.session_state:
    st.session_state['last_price'] = None
if 'last_volume' not in st.session_state:
    st.session_state['last_volume'] = None
if 'last_change_rate' not in st.session_state:
    st.session_state['last_change_rate'] = None
if 'initial_data' not in st.session_state:
    st.session_state['initial_data'] = None

# 제목
st.title("KRX 주식 데이터 분석")
st.markdown("---")

# 사이드바 - 필터 설정
with st.sidebar:
    st.header("필터 설정")
    
    # 날짜 선택
    default_date = get_default_date()
    selected_date = st.date_input(
        "날짜 선택",
        value=default_date,
        max_value=datetime.now(),
        min_value=datetime(2020, 1, 1)
    )
    
    # 필터 조건
    min_price = st.number_input(
        "종가",
        min_value=0,
        value=5000,
        step=100
    )
    
    min_volume = st.number_input(
        "거래량",
        min_value=0,
        value=80000,
        step=1000
    )
    
    min_change_rate = st.number_input(
        "등락률",
        min_value=-100.0,
        value=0.0,
        step=0.1,
        format="%.1f"
    )
    
    # 정렬 기준
    sort_by = st.selectbox(
        "정렬 기준",
        options=["등락률", "종가", "거래량"],
        index=0
    )
    
    sort_ascending = st.checkbox("오름차순 정렬", value=False)
    
    # 조회 버튼
    if st.button("조회", type="primary"):
        st.session_state['should_refresh'] = True
        st.session_state['last_date'] = selected_date
        st.session_state['last_price'] = min_price
        st.session_state['last_volume'] = min_volume
        st.session_state['last_change_rate'] = min_change_rate

# 메인 컨텐츠
try:
    # 초기 데이터 로드 또는 조건이 변경된 경우 데이터 갱신
    if st.session_state['initial_data'] is None or st.session_state['should_refresh']:
        # 데이터 수집
        collector = KRXDataCollector()
        date_str = format_date(selected_date)
        df = collector.get_stock_data(date_str)
        
        if df.empty:
            st.error("데이터를 불러올 수 없습니다. 날짜를 확인해주세요.")
        else:
            # 데이터 처리
            processor = DataProcessor()
            processor.set_data(df)
            filtered_df = processor.filter_data(min_price, min_volume, min_change_rate)
            sorted_df = processor.sort_data(filtered_df, sort_by, sort_ascending)
            
            if len(sorted_df) > 0:
                # 데이터 개수 표시
                st.markdown(f"### 검색 결과: {len(sorted_df)}개")
                
                # 데이터 테이블
                st.dataframe(
                    sorted_df,
                    column_config={
                        "종목코드": st.column_config.TextColumn("종목코드", width="small"),
                        "종목명": st.column_config.TextColumn("종목명", width="medium"),
                        "시장구분": st.column_config.TextColumn("시장구분", width="small"),
                        "종가": st.column_config.NumberColumn("종가", format="%d"),
                        "거래량": st.column_config.NumberColumn("거래량", format="%d"),
                        "등락률": st.column_config.NumberColumn("등락률", format="%.2f%%")
                    },
                    hide_index=True
                )
                
                # CSV 다운로드
                csv_file = processor.save_to_csv(sorted_df, date_str)
                with open(csv_file, 'rb') as f:
                    st.download_button(
                        label="CSV 다운로드",
                        data=f,
                        file_name=f"krx_data_{date_str}.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("현재 설정된 조건에 맞는 종목이 없습니다. 필터 조건을 조정해보세요.")
            
            # 초기 데이터 저장
            st.session_state['initial_data'] = sorted_df

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}") 