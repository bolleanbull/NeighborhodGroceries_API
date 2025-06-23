# creating custom throtteling policies like , a user can request max 10 request per minute, and max 15 in hour 
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


    