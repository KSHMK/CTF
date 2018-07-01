import dpkt
C = 0
BUF = ""
P = 0
T = 0
f = open("SO"+str(T)+".jpg","wb")
for ts, pkt in dpkt.pcap.Reader(open('HideInSSL.pcap','r')):
    C+=1
    eth=dpkt.ethernet.Ethernet(pkt) 
    if not isinstance(eth.data, dpkt.ip.IP):
        continue
    ip = eth.data
    if not isinstance(ip.data, dpkt.tcp.TCP):
        continue
    tcp = ip.data
    if len(tcp.data) <= 0:
        continue
    if tcp.sport == 443 and tcp.dport == P:
        if tcp.data[0] == '1':
            f.write(BUF[4:4+ord(BUF[0])])
        
    if tcp.dport != 443:
        continue
    
    if ord(tcp.data[0]) != 22:
        continue
    tls = dpkt.ssl.TLS(tcp.data)
    if len(tls.records) < 1:
        continue
    for record in tls.records:
        # TLS handshake only
        if record.type != 22:
            continue
        if len(record.data) == 0:
            continue
        # Client Hello only
        if ord(record.data[0]) != 1:
            continue
        try:
            handshake = dpkt.ssl.TLSHandshake(record.data)
        except dpkt.dpkt.UnpackError, e:
            print C
            # TODO: shouldn't happen in practice for handshakes... but could. meh.
            continue

        if not isinstance(handshake.data, dpkt.ssl.TLSClientHello):
            continue
    
        K = handshake.data.random[4:]
        
        if K[1] == '\x00':
            BUF = K
            P = tcp.sport
            
            
f.close()
f = open("SO"+str(T)+".jpg","rb")
K = f.read()
f.close()
P_len= len(K)
while True:
    P = K.find("\xff\xd9")
    if P != -1:
        
        f = open("SO"+str(T)+".jpg","wb")
        f.write(K[:P+2])
        f.close()
        T+=1
        K = K[P+2:]
    else:
        break
