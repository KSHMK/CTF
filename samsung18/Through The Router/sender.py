from socket import *
packet= "450000023CB04000401100000A0107080A00000115b35678000E3c51736563726574".decode('hex')
s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)
s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
s.sendto(packet, ('10.0.0.1', 0))
