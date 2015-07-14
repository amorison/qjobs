"""defines Job classes:
    Job: atomic class
    JobList: Job set
    JobGroup: container which can contains JobGroups and JobLists"""

from bisect import bisect_left

import constants


class Job:
    """Job class with hash and comparison based on job id"""

    def __init__(self, dct):
        """create a job class with the xml 'joblist' tree"""
        self.dct = dct
        if 'i' not in dct:
            raise ValueError("dct must contains a 'i' key")
        self.idt = dct['i']

    def __hash__(self):
        """hash based on job id"""
        return hash(self.idt)

    def __eq__(self, other):
        """comparison based on job id"""
        return isinstance(other, self.__class__) and self.idt == other.idt

    def __ne__(self, other):
        """comparison based on job id"""
        return not self.__eq__(other)

    def get(self, itm):
        """get job propriety"""
        return self.dct[itm]

    def rep(self, fmt):
        """representation of job based on format fmt"""
        return fmt.format(**self.dct)


class JobList:
    """JobList class which handle the width of the different
    fields and the job counting for total"""

    def __init__(self, job_list):
        """constructor expects a list of Job"""
        self.jobset = set(job_list)
        self.width = {}
        self.total = {}
        for itm in constants.itms:
            self.width[itm] = sorted(len(job.get(itm))
                                     for job in self.jobset)
            self.total[itm] = {}
            for value in set(job.get(itm) for job in self.jobset):
                self.total[itm][value] = set(job for job in self.jobset
                                             if job.get(itm) == value)

    def add(self, new_job):
        """add a job, update width and total, and erase the previous
        existing one with the same id if needed"""

        old_job = None
        for job in self.jobset:
            if new_job == job:
                old_job = job

        if old_job:
            for itm in constants.itms:
                jitm = old_job.get(itm)
                lgt = len(jitm)
                wlist = self.width[itm]
                wlist.pop(bisect_left(wlist, lgt))

                tlist = self.total[itm]
                tlist[jitm].remove(old_job)
                if not tlist[jitm]:
                    tlist.pop(jitm)
            self.jobset.remove(old_job)

        for itm in constants.itms:
            jitm = new_job.get(itm)
            lgt = len(jitm)
            wlist = self.width[itm]
            wlist.insert(bisect_left(wlist, lgt), lgt)

            self.total[itm][jitm].add(new_job)

        self.jobset.add(new_job)

    def rep(self, fmt):
        """handles the representation of the entire list"""
        # will have to work a bit on the format to put the width of the fields
        # will have to sort jobset
        # replace output.out
        for job in self.jobset:
            print(job.rep(fmt))

    def rep_tot(self, tot_list, fmt):
        """handles the representation of the totals"""
        # will need args.total -> tot_list
        pass


class JobGroup:
    pass
