#!/usr/bin/python
import sys

if __name__ == '__main__':
    print """cd "C:\\Program Files\\Mozilla Firefox"\r
"C:\\Program Files\\Mozilla Firefox\\firefox.exe" "file://localhost/C:/Documents and Settings/Administrator/My Documents/%s/%s/home.html"\r
""" % (sys.argv[1],sys.argv[1])

