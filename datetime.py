import re, datetime
s = "I have a meeting on 2018-12-10 in New York"
match = re.search('\d{4}-\d{2}-\d{2}', s)
date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
print (date)

date_time_str = format(datetime.datetime.now())
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)
print (datetime.datetime.now().date() - datetime.timedelta(days=35))
