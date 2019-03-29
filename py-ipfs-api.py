#!/bin/env python
# python2.7.16

import ipfsapi
import sys


def main():
    if len(sys.argv) < 3 :
        print "args error\nUsage:  ./py-ipfs-api.py ${ipaddress} add gettestfile.py"
        sys.exit(1)

    if sys.argv[2] == "get" :  
        api = ipfsapi.connect(sys.argv[1], 5001)
        for file in sys.argv[3:] :
            res = api.get(file)
            print res

    if sys.argv[2] == "add" :
        api = ipfsapi.connect(sys.argv[1], 5001)
        for file in sys.argv[3:] :
            res = api.add(file)
            print res

if __name__ == "__main__":
    main()
