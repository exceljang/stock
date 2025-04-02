from datetime import datetime, timedelta

def format_date(date):
    """
    datetime 객체를 'YYYYMMDD' 형식의 문자열로 변환합니다.
    
    Args:
        date (datetime): 변환할 날짜
        
    Returns:
        str: 'YYYYMMDD' 형식의 날짜 문자열
    """
    return date.strftime('%Y%m%d')

def get_default_date():
    """
    오늘 날짜를 반환합니다. 주말인 경우 가장 최근 거래일을 반환합니다.
    
    Returns:
        datetime: 기본 날짜
    """
    today = datetime.now()
    
    # 주말인 경우 가장 최근 거래일로 조정
    if today.weekday() >= 5:  # 5: 토요일, 6: 일요일
        days_to_subtract = today.weekday() - 4
        today = today - timedelta(days=days_to_subtract)
        
    return today

def format_number(number):
    """
    숫자를 천 단위 구분자가 있는 문자열로 변환합니다.
    
    Args:
        number (float): 변환할 숫자
        
    Returns:
        str: 천 단위 구분자가 있는 문자열
    """
    return f"{number:,.0f}" 