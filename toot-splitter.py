#!/usr/bin/env python3

import sys, re, zlib

MAX_LENGTH = 500 - 30 # 470, both as a courtesy, and to fit the ident

def toot_split(string):
    # Hat tip to Stack Overflow answer <https://stackoverflow.com/a/2136580>
    # by Commodore Jaeger
    # <https://stackoverflow.com/users/4659/commodore-jaeger> to question
    # "In Python, how do I split a string and keep the separators?"
    # <https://stackoverflow.com/q/2136556> by Ken Kinder
    # <https://stackoverflow.com/users/170431/ken-kinder> (CC-BY-SA 3.0). Wow,
    # the attribution required makes the code comments obnoxious.
    words = re.split('([ \t\r\n.,?!:;(-)-[\]{}"\'])', string)
    toots = []
    toot = ''
    for i in words:
        new_toot = toot + i
        if len(new_toot) > MAX_LENGTH:
            toot = toot + '*'
            toot_hash = hex(zlib.adler32(toot.encode("UTF-8")) & 0xffffffff)[2:]
            # left-pad the hexadecimal hash to 8 hexts
            LEFT_PAD = '0' * 8
            toot_hash = LEFT_PAD[len(toot_hash):] + toot_hash
            toot = toot + '(' + toot_hash + ')'
            toots.append(toot)
            toot = '(continued from ' + toot_hash + ')*' + i
        else:
            toot = new_toot
    toots.append(toot)
    return toots

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Split a long string into shorter ones with checksums.',
        epilog='''\
Notes:
  - If infile or outfile are omitted or -, input/output come through their
  respective standard I/O channels.

Authored by @zyabin101@botsin.space. Source code is available at
<https://github.com/schas002/toot-splitter>.'''
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin, help='File with string to split')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
        default=sys.stdout, help='File to contain split string')
    parser.add_argument('--divider', default='* * *', help='Divider '
        'between output strings, surrounded by newlines. Default is `* * *`')
    args = parser.parse_args()
    string = args.infile.read()
    for i in toot_split(string):
        print(i, end=('\n' + args.divider + '\n'), file=args.outfile)
