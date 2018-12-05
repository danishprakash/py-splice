"Benchmark comparison bw read/write and splice(2)"

import splice

from time import sleep
from time import perf_counter as pc


def traditional_copy():
    t0 = pc()
    with open('read.txt') as f:
        with open('write.txt', 'w+') as f1:
            for line in f:
                f1.write(line)
    return (pc() - t0)


def splice_copy():
    t0 = pc()
    f1 = open('read.txt')
    f2 = open('write2.txt', 'w+')
    splice.splice(f1.fileno(), f2.fileno())
    return (pc() - t0)


def _get_numbers():
    _trad = traditional_copy()
    _splice = splice_copy()
    sleep(5)
    return (_trad, _splice, abs(_trad - _splice))


# TODO: add file size column on the left
# TODO: add benchmark tests for different file sizes
print('Benchmarks\n')
print('{:20} | {:<20} | {:<20}'.format('Traditional', 'Splice', 'Diff'))
print('{:20} + {:<20} + {:<20}'.format('-'*20, '-'*20, '-'*20))
for _ in range(5):
    print('{:<20} | {:<20} | {:<20}'.format(*_get_numbers()))
