#! /usr/bin/python3

import sys
import random
import argparse
import os

parser= argparse.ArgumentParser ()
parser.add_argument ('--host', action='append', dest='hosts', metavar='HOST',
                     required=True, help='Repeat as needed.')
# sometimes someone offers to bring starters...
parser.add_argument ('--starter')
# ... or to be the cook...
parser.add_argument ('--cook')
# ... or even dessert!
parser.add_argument ('--desserter')
parser.add_argument ('coming', nargs='+', help='This list MUST include ALL the people in the order the answered the invitation.')

options= parser.parse_args (sys.argv[1:])

dinners= [ line.strip () for line in open ('list.txt').readlines () ]
print ("original list:", dinners)

print ("hosts:", options.hosts)

if options.cook is None:
    # the cook is the first dinner in the list that comes
    for dinner in dinners:
        if dinner in options.coming:
            options.cook= dinner
            break
print ("cook:", options.cook)

# comers who don't have a task yet (except hosting, which could end up bringing dessert)
taskless= [ dinner for dinner in options.coming
                   if dinner!=options.cook
                      and dinner!=options.desserter
                      and dinner!=options.starter ]

if options.desserter is None:
    # the dessert goes to who answered last (except cook and host(s))
    # note that this discards non-stable dinners
    options.desserter= taskless[-1]
    taskless.remove (options.desserter)
print ("dessert:", options.desserter)

# On Mon, Feb 22, 2016 at 02:11:38PM +0000, Matteo Dell'Amico wrote:
# > I generally except host(s) from starters.
taskless= [ dinner for dinner in taskless if dinner not in options.hosts ]
if options.starter is None:
    # finally, starters is chosen randomly among the remaining dinners
    options.starter= random.choice (taskless)
    taskless.remove (options.starter)
print ("starters:", options.starter)

print ("others:", taskless)

print ("count:", len (options.coming))

# now update the list
# the cook goes to the bottom
try:
    dinners.remove (options.cook)
    dinners.append (options.cook)
except ValueError:
    # the cook could be an invitee!
    try:
        ans= input ('looks like the cook (%s) is an invitee! confirm [Y/n]?' % options.cook)[0].upper ()
    except (KeyboardInterrupt, EOFError):
        ans= 'N'

    if ans=='N':
        print (os.linesep+'aborted, lists.txt not updated...')
        sys.exit (1)
# print (dinners)

# hosts drop one position
for host in options.hosts:
    index= dinners.index (host)
    # now, the problem is that more than one hosts are together in the list
    # say, A and B in positions 5 and 6
    # if I remove A, B becomes 5 and I add A after, becomes 6
    # so basically I swapped them
    # and if then I try to do the same with B, I swap them again, ending with the original list
    # so we iterate over the rest of the list till we find a non host
    for i in range (index, len (dinners)):
        # print (index, host, i, dinners[i])
        if dinners[i] not in options.hosts:
            # swapping is enough
            # print (index, i)
            dinners[i], dinners[index]= dinners[index], dinners[i]
            break
print ("list for next week:", dinners)

f= open ('list.txt', 'w+')
for dinner in dinners:
    f.write (dinner+os.linesep)
f.close ()
