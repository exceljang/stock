import pandas as pd
from datetime import datetime
from pykrx import stock
import concurrent.futures
import os
import pickle
from pathlib import Path

class KRXDataCollector:
    def __init__(self):
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get_stock_data(self, date_str):
        """
        pykrx 라이브러리를 사용하여 KRX 웹사이트에서 주식 데이터를 수집합니다.
        캐싱을 사용하여 이미 수집한 데이터는 재사용합니다.
        
        Args:
            date_str (str): 'YYYYMMDD' 형식의 날짜 문자열
            
        Returns:
            pd.DataFrame: 수집된 주식 데이터
        """
        # 캐시 파일 경로
        cache_file = self.cache_dir / f"krx_data_{date_str}.pkl"
        
        # 캐시된 데이터가 있으면 로드
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"캐시 로드 중 오류 발생: {str(e)}")
        
        try:
            # 코스피 종목 리스트 가져오기
            kospi_tickers = stock.get_market_ticker_list(market="KOSPI")
            kosdaq_tickers = stock.get_market_ticker_list(market="KOSDAQ")
            
            # 병렬 처리를 위한 함수
            def fetch_stock_data(ticker, market):
                try:
                    df = stock.get_market_ohlcv_by_date(date_str, date_str, ticker)
                    if not df.empty:
                        df['종목코드'] = ticker
                        df['종목명'] = stock.get_market_ticker_name(ticker)
                        df['시장구분'] = market
                        return df
                except:
                    pass
                return None
            
            # 병렬 처리로 데이터 수집
            all_data = []
            
            # 코스피 데이터 수집
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_ticker = {executor.submit(fetch_stock_data, ticker, 'KOSPI'): ticker for ticker in kospi_tickers}
                for future in concurrent.futures.as_completed(future_to_ticker):
                    result = future.result()
                    if result is not None:
                        all_data.append(result)
            
            # 코스닥 데이터 수집
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_ticker = {executor.submit(fetch_stock_data, ticker, 'KOSDAQ'): ticker for ticker in kosdaq_tickers}
                for future in concurrent.futures.as_completed(future_to_ticker):
                    result = future.result()
                    if result is not None:
                        all_data.append(result)
            
            # 데이터 합치기
            if all_data:
                combined_data = pd.concat(all_data)
                
                # 필요한 컬럼만 선택
                result_df = combined_data[['종목코드', '종목명', '시장구분', '종가', '거래량']].copy()
                
                # 등락률 계산
                result_df['등락률'] = ((combined_data['종가'] - combined_data['시가']) / combined_data['시가'] * 100).round(2)
                
                # 결과 캐싱
                try:
                    with open(cache_file, 'wb') as f:
                        pickle.dump(result_df, f)
                except Exception as e:
                    print(f"캐시 저장 중 오류 발생: {str(e)}")
                
                return result_df
            else:
                print("수집된 데이터가 없습니다.")
                return pd.DataFrame()
            
        except Exception as e:
            print(f"데이터 수집 중 오류 발생: {str(e)}")
            return pd.DataFrame() 