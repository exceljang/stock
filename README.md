# KRX 주식 데이터 분석 애플리케이션

KRX 웹사이트의 주식 데이터를 수집하여 상승 종목 중 지정된 조건의 종목을 필터링하고 시각화하는 웹 애플리케이션입니다.

## 주요 기능

- KRX 웹사이트에서 주식 데이터 수집
- 사용자 지정 조건에 따른 데이터 필터링
- 데이터 시각화 및 테이블 표시
- CSV 파일 다운로드

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yourusername/krx-stock-analyzer.git
cd krx-stock-analyzer
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
streamlit run src/app.py
```

## 사용 방법

1. 웹 브라우저에서 `http://localhost:8501` 접속
2. 날짜 선택
3. 필터 조건 입력:
   - 종가 최소값
   - 거래량 최소값
   - 등락률 > 0 (자동 적용)
4. 결과 확인 및 CSV 다운로드

## 기술 스택

- Python 3.x
- Streamlit
- pandas
- requests
- BeautifulSoup4

## 라이선스

MIT License 