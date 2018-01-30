"""defines Job classes:
    Job: atomic class
    JobList: Job set
    JobGroup: container which can contains JobGroups and JobLists"""

from bisect import bisect_left
from collections import Counter
from datetime import datetime
from functools import total_ordering

from . import conf, constants
from .misc import time_handler


@total_ordering
class Job:
    """Job class with hash and comparison based on job id"""

    def __init__(self, job_xml, today):
        """create a job with the xml 'joblist' tree"""

        self.dct = {}
        for itm, itmtp in constants.itms.items():
            self.dct[itm] = ''
            for tag in itmtp.xml_tag:
                elts = job_xml.iter(tag)
                self.dct[itm] = ', '.join(sorted(elt.text for elt in elts
                                                 if elt.text))
                if self.dct[itm]:
                    break

        self.dct['i'] = int(self.dct['i'])
        self.idt = self.dct['i']

        if self.dct['k']:
            self.dct['q'], self.dct['d'] = self.dct['k'].rsplit('@')

        self.update(today)

    def __hash__(self):
        """hash based on job id"""
        return hash(self.idt)

    def __eq__(self, other):
        """comparison based on job id"""
        return isinstance(other, self.__class__) and self.idt == other.idt

    def __lt__(self, other):
        """comparison based on job id"""
        return isinstance(other, self.__class__) and self.idt < other.idt

    def get(self, itm):
        """get job propriety"""
        return self.dct[itm]

    def rep(self, fmt):
        """representation of job based on format fmt"""
        return fmt.format(**self.dct)

    def update(self, today):
        """update elapsed time field, using today as reference"""
        self.dct['t'], self.dct['e'] = time_handler(self.dct['t'],
                                                    conf.jobs.start_format,
                                                    conf.jobs.elapsed_format,
                                                    today)


class JobList:
    """JobList class which handles the width of the different
    fields and the job counting for total"""

    def __init__(self, job_list):
        """constructor expects a list of Job"""
        self.jobset = sorted(set(job_list))
        self.njobs = len(self.jobset)
        self.width = {}
        self.total = {}
        self.count()

    def add(self, new_job):
        """add a job, update width and total, and erase the previous
        existing one with the same id if needed"""

        idx = bisect_left(self.jobset, new_job)
        old_job = self.jobset[idx]

        today = datetime.today()
        self.update(today)
        new_job.update(today)

        if new_job == old_job:
            for itm in constants.itms:
                jitm = old_job.get(itm)
                lgt = len(str(jitm))
                wlist = self.width[itm]
                del wlist[bisect_left(wlist, lgt)]

                self.total[itm] -= Counter([jitm])
            del self.jobset[idx]

        for itm in constants.itms:
            jitm = new_job.get(itm)
            lgt = len(str(jitm))
            wlist = self.width[itm]
            wlist.insert(bisect_left(wlist, lgt), lgt)

            self.total[itm] += Counter([jitm])

        self.jobset.insert(idx, new_job)

    def count(self):
        """determine width of fields and count total"""
        for itm in constants.itms:
            self.width[itm] = sorted(len(str(job.get(itm)))
                                     for job in self.jobset)
            self.total[itm] = Counter(job.get(itm)
                                      for job in self.jobset)

    def rep(self):
        """handle the representation of the entire list"""

        jobset_out = sorted(self.jobset)
        for itm in conf.jobs.sort:
            jobset_out.sort(key=lambda job: job.get(itm),
                            reverse=itm in conf.jobs.reversed_itms)

        wdt = {}
        for itm in constants.itms:
            wdt[itm] = self.width[itm][-1]

        fmt = conf.jobs.out_format.format(**wdt)
        if fmt:
            for job in jobset_out:
                yield job.rep(fmt)

    def rep_tot(self):
        """handle the representation of the totals"""

        from itertools import zip_longest as ziplgst
        from math import ceil

        yield 'tot: {}'.format(len(self.jobset))
        for itm in conf.total.total:
            dct = self.total[itm.lower()]
            if '' in dct:
                dct['not set'] = dct.pop('')

            dct = sorted(dct.items(),
                         key=lambda x: x[0],
                         reverse=itm.lower() in conf.jobs.reversed_itms)
            if itm.lower() in 'te':
                dct_tmp = ((str(k), v) for k, v in dct)
                dct = [next(dct_tmp)]
                for k, v in dct_tmp:
                    if dct[-1][0] == k:
                        dct[-1] = k, dct[-1][1] + v
                    else:
                        dct.append((k, v))

            if itm.isupper():
                dct = sorted(dct,
                             key=lambda x: x[1],
                             reverse=True)

            mlk = max(len(str(k)) for k, _ in dct)
            mlv = max(len(str(v)) for _, v in dct)
            nfld = (conf.total.width_tot+len(conf.total.sep_tot)) // \
                   (mlk+mlv+2+len(conf.total.sep_tot))
            if nfld == 0:
                nfld = 1

            dct = ziplgst(*(iter(dct), ) * int(ceil(len(dct)/float(nfld))),
                          fillvalue=(None, None))
            dct = zip(*dct)

            yield ''
            for line in dct:
                yield conf.total.sep_tot.join(
                    ('{}: {}'.format(str(k).ljust(mlk), str(v).rjust(mlv))
                     for k, v in line if (k, v) != (None, None)))

    def update(self, today):
        """update elapsed times, using today as reference"""
        for job in self.jobset:
            job.update(today)
        self.count()


class JobGroup:
    pass
