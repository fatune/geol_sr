from django.utils import timezone

DELTA_0 = timezone.timedelta(seconds=5)
DELTA_1 = timezone.timedelta(seconds=30)
DELTA_2 = timezone.timedelta(seconds=60)
DELTA_3 = timezone.timedelta(seconds=300) # 5 minutes
DELTA_4 = timezone.timedelta(seconds=3600*12) # 1/2 of a day
DELTA_5 = timezone.timedelta(seconds=3600*48) # 2 days

# Postopne time to answer if related card rated
DELTA_POSTPONE = timezone.timedelta(seconds=600)
