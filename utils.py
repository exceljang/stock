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

def get_last_business_day():
    """
    마지막 거래일을 반환합니다.
    
    Returns:
        datetime: 마지막 거래일
    """
    today = datetime.now()
    last_day = today - timedelta(days=1)
    
    # 주말인 경우 금요일로 이동
    while last_day.weekday() >= 5:  # 5: 토요일, 6: 일요일
        last_day = last_day - timedelta(days=1)
        
    return last_day

def validate_inputs(min_price, min_volume, min_change_rate):
    """
    사용자 입력값을 검증합니다.
    
    Args:
        min_price (float): 최소 종가
        min_volume (float): 최소 거래량
        min_change_rate (float): 최소 등락률
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if min_price < 0:
        return False, "최소 종가는 0 이상이어야 합니다."
    
    if not float(min_price).is_integer():
        return False, "최소 종가는 정수여야 합니다."
    
    if min_volume < 0:
        return False, "최소 거래량은 0 이상이어야 합니다."
        
    if min_change_rate < 0:
        return False, "최소 등락률은 0 이상이어야 합니다."
        
    if not float(min_change_rate).is_integer():
        return False, "최소 등락률은 정수여야 합니다."
        
    return True, "" 