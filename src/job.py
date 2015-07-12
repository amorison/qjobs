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
    def __init__(self):
        self.jobset = set()
        self.width = {}
        for itm in constants.itms:
            self.width[itm] = 0
            # sorted list of length (will make updates easier)
            # should also be able to init with an actual list of jobs
            # to avoid making a lot of "heavy" updates just to
            # init the JobList...

    def add(self, job):
        # should remove then add
        # and update width/total datas
        self.jobset.add(job)

    def replace(self, job):
        self.jobset.discard(job)
        self.jobset.add(job)

    def rep(self, fmt):
        # will have to work a bit on the format to put the width of the fields
        # will have to sort jobset
        # replace output.out
        for job in self.jobset:
            print(job.rep(fmt))

    # need a function to replace output.total
    # total will need to be updated as the width
    # misc.get_itms: will construct the groups and JobLists? (will be renamed)

class JobGroup:
    pass
