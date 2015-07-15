"""defines Job classes:
    Job: atomic class
    JobList: Job set
    JobGroup: container which can contains JobGroups and JobLists"""

from bisect import bisect_left
from collections import Counter
from datetime import datetime
from functools import total_ordering

import constants
from misc import time_handler


@total_ordering
class Job:
    """Job class with hash and comparison based on job id"""

    def __init__(self, job_xml, args, today):
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

        self.update(today, args)

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

    def update(self, today, args):
        """update elapsed time field, using today as reference"""
        self.dct['t'], self.dct['e'] = time_handler(self.dct['t'],
                                                    args.start_format,
                                                    args.elapsed_format,
                                                    today)


class JobList:
    """JobList class which handles the width of the different
    fields and the job counting for total"""

    def __init__(self, job_list, args):
        """constructor expects a list of Job"""
        self.jobset = sorted(set(job_list))
        self.njobs = len(self.jobset)
        self.width = {}
        self.total = {}
        self.args = args
        self.count()

    def add(self, new_job):
        """add a job, update width and total, and erase the previous
        existing one with the same id if needed"""

        idx = bisect_left(self.jobset, new_job)
        old_job = self.jobset[idx]

        today = datetime.today()
        self.update(today)
        new_job.update(today, self.args)

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

    def rep(self, fmt):
        """handle the representation of the entire list"""
        # will have to work a bit on the format to put the width of the fields
        # will have to sort jobset
        # replace output.out
        for job in self.jobset:
            print(job.rep(fmt))

    def rep_tot(self, tot_list, fmt):
        """handle the representation of the totals"""
        # will need args.total -> tot_list
        # will need to group time and elapsed time
        # with same str()
        pass

    def update(self, today):
        """update elapsed times, using today as reference"""
        for job in self.jobset:
            job.update(today, self.args)
        self.count()


class JobGroup:
    pass
