"""output module"""

import constants
from misc import elapsed_time


def out(alljobs, args):
    """produces output of jobs list"""

    for itm in args.sort:
        rvs = itm in constants.reversed_itms
        itm = itm.replace('e', 't')
        if itm in constants.itms:
            alljobs.sort(key=lambda job: job[itm],
                         reverse=rvs)
    mlitm = {}
    for itm in args.out:
        mlitm[itm] = max(len(job[itm]) for job in alljobs)

    for job in alljobs:
        print(*(job[itm].ljust(mlitm[itm]) for itm in args.out),
              sep=args.sep)


def total(alljobs, job_counter, args):
    """produces output of totals"""

    from itertools import zip_longest as ziplgst
    from math import ceil

    print('tot: {}'.format(len(alljobs)))
    for itm in args.total:
        rvs = itm.lower() in constants.reversed_itms
        tot_elaps = False
        if itm.lower() == 'e':
            tot_elaps = True
            itm = itm.replace('e', 't').replace('E', 'T')
        dct = job_counter[itm.lower()]
        if '' in dct:
            dct['not set'] = dct.pop('')

        dct = sorted(dct.items(),
                     key=lambda x: x[0],
                     reverse=rvs)
        if itm.isupper():
            dct = sorted(dct,
                         key=lambda x: x[1],
                         reverse=True)

        if tot_elaps:
            dct = list((elapsed_time(k, args.elapsed_format), v)
                       for k, v in dct)
        mlk = max(len(k) for k, _ in dct)
        mlv = max(len(str(v)) for _, v in dct)
        nfld = (args.width_tot+len(args.sep_tot)) // \
               (mlk+mlv+2+len(args.sep_tot))
        if nfld == 0:
            nfld = 1

        dct = ziplgst(*(iter(dct), ) * int(ceil(len(dct)/float(nfld))),
                      fillvalue=(None, None))
        dct = zip(*dct)

        print()
        for line in dct:
            print(*('{}: {}'.format(k.ljust(mlk), str(v).rjust(mlv))
                    for k, v in line if (k, v) != (None, None)),
                  sep=args.sep_tot)
