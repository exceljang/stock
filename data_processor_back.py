import pandas as pd
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.data = None
        
    def set_data(self, df):
        """
        처리할 데이터를 설정합니다.
        
        Args:
            df (pd.DataFrame): 처리할 데이터프레임
        """
        self.data = df.copy()
        
    def filter_data(self, min_price=0, min_volume=0, min_change_rate=0):
        """
        주어진 조건에 따라 데이터를 필터링합니다.
        
        Args:
            min_price (float): 최소 종가
            min_volume (int): 최소 거래량
            min_change_rate (float): 최소 등락률
            
        Returns:
            pd.DataFrame: 필터링된 데이터프레임
        """
        if self.data is None:
            return pd.DataFrame()
            
        # 필터링 조건 적용
        filtered_df = self.data[
            (self.data['종가'] >= min_price) &
            (self.data['거래량'] >= min_volume) &
            (self.data['등락률'] >= min_change_rate)
        ].copy()
        
        return filtered_df
        
    def sort_data(self, df, sort_by='등락률', ascending=False):
        """
        데이터를 정렬합니다.
        
        Args:
            df (pd.DataFrame): 정렬할 데이터프레임
            sort_by (str): 정렬 기준 컬럼
            ascending (bool): 오름차순 정렬 여부
            
        Returns:
            pd.DataFrame: 정렬된 데이터프레임
        """
        return df.sort_values(by=sort_by, ascending=ascending)
        
    def save_to_csv(self, df, date_str):
        """
        데이터프레임을 CSV 파일로 저장합니다.
        
        Args:
            df (pd.DataFrame): 저장할 데이터프레임
            date_str (str): 파일명에 포함할 날짜 문자열
            
        Returns:
            str: 저장된 파일 경로
        """
        filename = f"data/krx_data_{date_str}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return filename 