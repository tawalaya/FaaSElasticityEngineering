#! /usr/env python

import sys
import os
from functools import reduce

def main(params):
    tmp = params.split(",")
    p0      = int(tmp[0])
    p1      = int(tmp[1])
    sloap   = float(tmp[2])
    target=int(p1+(60*sloap))

    template=""

    with open("template.yml") as f:
        template = reduce(lambda x,a:x+a,f.readlines())

    template = template % (p0,p1,target,target)

    print(template)


if __name__ == "__main__":
    main(sys.argv[1])