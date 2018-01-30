"""defines constants for qjobs"""

from collections import OrderedDict, namedtuple

Itmtp = namedtuple('Itmtp', ['dscr', 'xml_tag'])

itms = OrderedDict((
    ('i', Itmtp('job id', ['JB_job_number'])),
    ('p', Itmtp('job priority', ['JAT_prio'])),
    ('n', Itmtp('job name', ['JB_name'])),
    ('o', Itmtp('job owner', ['JB_owner'])),
    ('s', Itmtp('job state', ['state'])),
    ('t', Itmtp('job start/submission time', ['JAT_start_time',
                                              'JB_submission_time'])),
    ('e', Itmtp('elapsed time since start/submission', [])),
    ('q', Itmtp('queue name without domain', [])),
    ('d', Itmtp('queue domain', [])),
    ('k', Itmtp('queue name with domain', ['queue_name'])),
    ('r', Itmtp('requested queue(s)', ['hard_req_queue'])),
    ('l', Itmtp('number of slots used', ['slots']))
))
