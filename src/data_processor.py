import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def filter_data(df, min_price, min_volume, min_change_rate):
        """
        주어진 조건에 따라 데이터를 필터링합니다.
        
        Args:
            df (pd.DataFrame): 필터링할 데이터프레임
            min_price (float): 최소 종가
            min_volume (float): 최소 거래량
            min_change_rate (float): 최소 등락률
            
        Returns:
            pd.DataFrame: 필터링된 데이터프레임
        """
        try:
            # 등락률이 양수이고 최소 등락률 이상인 종목만 선택
            filtered_df = df[
                (df['등락률'] > 0) & 
                (df['등락률'] >= min_change_rate) &
                (df['종가'] >= min_price) & 
                (df['거래량'] >= min_volume)
            ]
            
            # 등락률 기준으로 내림차순 정렬
            filtered_df = filtered_df.sort_values('등락률', ascending=False)
            
            return filtered_df
            
        except Exception as e:
            print(f"데이터 필터링 중 오류 발생: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def save_to_csv(df, date_str):
        """
        데이터프레임을 CSV 파일로 저장합니다.
        
        Args:
            df (pd.DataFrame): 저장할 데이터프레임
            date_str (str): 'YYYYMMDD' 형식의 날짜 문자열
            
        Returns:
            str: 저장된 파일 경로
        """
        try:
            # 저장 경로 설정
            save_dir = r"C:\AI\Cursor\Stock"
            
            # 디렉토리가 없으면 생성
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            filename = os.path.join(save_dir, f"krx_data_{date_str}.csv")
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            return filename
            
        except Exception as e:
            print(f"CSV 파일 저장 중 오류 발생: {str(e)}")
            return None 