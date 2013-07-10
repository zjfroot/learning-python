#!/usr/bin/python
from subprocess import call, CalledProcessError, check_call
from multiprocessing import Pool, Manager, Process

def nslookup_range(a):
    for b in range(1,256):
        call(["nslookup","10.240.%d.%d"%(a,b)])

def ping_range(a):
    for b in range(1,256):
        call(["ping","-c 1","-W 1","10.240.%d.%d"%(a,b)])

def ping_one(y):
    a = y/256
    b = y%256
    ip = "10.240.%d.%d"%(a,b)
    try:
        check_call(["ping","-c 1","-W 1", ip])
        return ip, "is alive"
    except CalledProcessError:
        return ip, "not alive"

if __name__ == '__main__':
    p = Pool(128)
    #imap_it = p.imap(ping_one, range(0,100))
    imap_it = p.imap(ping_one, range(0,65536))
    p.close()
    p.join()

    f = open('ping_result', 'w')
    print 'Ordered results using pool.imap():'
    for x in imap_it:
        f.write(str(x)+'\n')
