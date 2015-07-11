"""miscellaneous functions"""


def rm_brackets(string):
    """remove [ ] if at 1st and last char"""

    if string and string[0] == '[':
        string = string[1:]
    if string and string[-1] == ']':
        string = string[:-1]

    return string


def elapsed_time(start_time, fmt):
    """return formatted elapsed time since start time"""

    from datetime import datetime

    delta = datetime.today() - \
        datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    dct = {}
    dct['d'] = delta.days
    dct['h'], rmd = divmod(delta.seconds, 3600)
    dct['m'], dct['s'] = divmod(rmd, 60)
    dct['S'] = 86400 * delta.days + delta.seconds
    dct['M'] = dct['S'] // 60
    dct['H'] = dct['S'] // 3600
    dct['D'] = dct['S'] / 86400.

    return fmt.format(**dct)


def get_itms(jobs_list, args):
    """extract data from xml job tree
    and count totals"""

    import constants

    alljobs = []
    job_counter = {}

    for j in jobs_list:
        job = {}
        for itm, itmtp in constants.itms.items():
            job[itm] = ''
            for tag in itmtp.xml_tag:
                elts = j.iter(tag)
                job[itm] = ', '.join(sorted(elt.text for elt in elts
                                            if elt.text))
                if job[itm]:
                    break

        if job['k']:
            job['q'], job['d'] = job['k'].rsplit('@')

        if job['t']:
            job['t'] = job['t'].replace('T', ' ')
            job['e'] = elapsed_time(job['t'], args.elapsed_format)
        else:
            job['t'] = 'not set'
            job['e'] = 'not set'

        for itm in set(args.total.lower()):
            if itm not in job_counter:
                job_counter[itm] = {}
            if job[itm] in job_counter[itm]:
                job_counter[itm][job[itm]].append(job)
            else:
                job_counter[itm][job[itm]] = [job]

        alljobs.append(job)

    return alljobs, job_counter
