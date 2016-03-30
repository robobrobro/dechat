#!/usr/bin/env python

import nose
import sys

if __name__ == '__main__':
    argv = ['--verbosity=2',
            '--with-coverage',
            '--cover-package=dechat',
            '--cover-branches',
            '--cover-erase',
            '--cover-html',
            '--cover-html-dir=./htmlcov',
    ]

    ret = 0 if nose.run(argv=argv) else 1
    sys.exit(ret)
