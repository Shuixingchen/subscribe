from datetime import datetime
import pytz

def convert_timestamp_to_localized_string(timestamp):
    datetime_obj_utc = datetime.utcfromtimestamp(timestamp)

    utc_8_tz = pytz.FixedOffset(8 * 60)

    datetime_obj_utc8 = datetime_obj_utc.replace(tzinfo=pytz.utc).astimezone(utc_8_tz)
    # 使用 strftime 打印出格式化的时间
    return datetime_obj_utc8.strftime('%Y-%m-%d %H:%M:%S')