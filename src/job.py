"""defines Job classes:
    Job: atomic class
    JobList: Job set
    JobGroup: container which can contains JobGroups and JobLists"""

import constants

class Job:
    """Job class with hash and comparison based on job id"""

    def __init__(self, dct):
        """dct must contains a 'i' key for hash and comparison"""
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
        """constructor expect a list of Job"""
        self.jobset = set(job_list)
        self.width = {}
        self.total = {}
        for itm in constants.itms:
            self.width[itm] = sorted(len(job.get(itm))
                                     for job in self.jobset)
        for job in self.jobset:
            for itm in constants.itms:


    def add(self, job):
        """add a job, update width and total, and erase the previous
        existing one with the same id if needed"""
        self.jobset.discard(job)
        self.jobset.add(job)


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
