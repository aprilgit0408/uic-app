from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from backports.zoneinfo import ZoneInfo
una_fecha = '2022-10-12T22:05'
# fecha_dt = datetime.strptime(una_fecha, '%Y-%m-%dT%H:%M')
naive = parse_datetime(una_fecha)
naive.replace(tzinfo=ZoneInfo("America/Guayaquil"))
print(naive)