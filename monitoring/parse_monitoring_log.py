import sys


def parse_task_log(file_iterator):
    """ identify allocated and used memory and disk space within a cromwell task

    :param iterator file_iterator: output generated by monitoring.sh script run via
      cromwell on a google compute VM. Most often called 'monitoring.log', and found in
      a task's cromwell directory within cromwell executions.
    :return int max_memory: maximum memory usage within task
    :return int total_memory: memory allocated for task
    :return int max_disk: maximum disk usage within task
    :return int total_disk: disk space allocated for task
    :return bool robust_estimate: True if there were 5 or more estimates across the
      task's run.

    """
    total_memory = 0
    total_disk = 0
    max_memory = 0
    max_disk = 0
    i = 0
    for i, line in enumerate(file_iterator):
        if line.startswith('Total Memory (MB):'):
            total_memory = int(line.split()[-1])
        elif line.startswith('Total Disk Space (KB):'):
            total_disk = int(line.split()[-1])
        elif line.startswith('* Memory usage (MB):'):
            max_memory = max(max_memory, int(line.split()[-1]))
        elif line.startswith('* Disk usage (KB):'):
            max_disk = max(max_disk, int(line.split()[-1]))
    robust_estimate = True if i >= 5 else False

    return {
        'max_memory': max_memory,
        'total_memory': total_memory,
        'max_disk': max_disk,
        'total_disk': total_disk,
        'robust_estimate': robust_estimate
    }

if __name__ == "__main__":
    if any(arg in {'-h', '--help', 'h'} for arg in sys.argv):
        print('usage: python3 parse_monitoring_log.py')
    for file_ in sys.argv[1:]:
        with open(file_, 'r') as f:
            print('file %s' % file_)
            results = parse_task_log(f)
            print('max memory usage (MB): %d' % results['max_memory'])
            print('available memory (MB): %d' % results['total_memory'])
            print('max disk usage (KB): %d' % results['max_disk'])
            print('available disk space (KB): %d' % results['total_disk'])
