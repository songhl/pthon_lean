#!/usr/local/bin/python
import GetMysqlStruct
import sys
import getopt
import json

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "h:P:S", ["verbose",'json'])
    opts = dict(opts)
    if not opts.has_key('-P'):
        opts['-P'] = 3358
    m = GetMysqlStruct.main(opts['-h'], opts['-P'])
    struct = m.Print()
    #print dir(m)
    print json.dumps(struct, indent=2)
    GetMysqlStruct.bin_tree(m)
