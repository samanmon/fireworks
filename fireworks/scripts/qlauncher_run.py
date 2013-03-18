#!/usr/bin/env python

"""
A runnable script for launching rockets (a command-line interface to queue_launcher.py)
"""

from argparse import ArgumentParser
import os
from fireworks.core.fworker import FWorker
from fireworks.core.launchpad import LaunchPad
from fireworks.queue.queue_adapter import QueueParams
from fireworks.queue.queue_launcher import rapidfire, launch_rocket_to_queue

__author__ = "Anubhav Jain"
__copyright__ = "Copyright 2013, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Anubhav Jain"
__email__ = "ajain@lbl.gov"
__date__ = "Jan 14, 2013"


def qlauncher_run():
    m_description = 'This program is used to submit jobs to a queueing system. Details of the job and queue \
    interaction are handled by the mandatory queue params file parameter. The "rapidfire" option can be used \
    to maintain a certain number of jobs in the queue by specifying the n_loops parameter to a large number. \
    If n_loops is set to 1 (default) the queue launcher will quit after submitting the desired number of jobs. \
    For more help on rapid fire options, use qlauncher.py rapidfire -h'
    
    parser = ArgumentParser(description=m_description)
    subparsers = parser.add_subparsers(help='command', dest='command')
    single_parser = subparsers.add_parser('singleshot', help='launch a single rocket to the queue')
    rapid_parser = subparsers.add_parser('rapidfire', help='launch multiple rockets to the queue')
    
    parser.add_argument('--launch_dir', help='directory to launch the job / rapid-fire', default='.')
    parser.add_argument('--logdir', help='path to a directory for logging', default=None)
    parser.add_argument('--loglvl', help='level to print log messages', default='INFO')
    parser.add_argument('--silencer', help='shortcut to mute log messages', action='store_true')
    parser.add_argument('-r', '--reserve', help='reserve a fw', action='store_true')
    parser.add_argument('-l', '--launchpad_file', help='path to launchpad file', default=None)
    parser.add_argument('-w', '--fworker_file', help='path to fworker file', default=None)
    parser.add_argument('-q', '--queueparams_file', help='path to queueparams file', default=None)
    parser.add_argument('-c', '--config_dir', help='path to a directory containing the config file (used if -l, -w, -q unspecified)',
                        default='.')

    rapid_parser.add_argument('-m', '--maxjobs_queue', help='maximum jobs to keep in queue for this user', default=10, type=int)
    rapid_parser.add_argument('-b', '--maxjobs_block', help='maximum jobs to put in a block', default=500, type=int)
    rapid_parser.add_argument('--nlaunches', help='num_launches (int or "infinite")')
    rapid_parser.add_argument('--sleep', help='sleep time between loops', default=60, type=int)

    args = parser.parse_args()

    if not args.launchpad_file and os.path.exists(os.path.join(args.config_dir, 'my_launchpad.yaml')):
        args.launchpad_file = os.path.join(args.config_dir, 'my_launchpad.yaml')

    if not args.fworker_file and os.path.exists(os.path.join(args.config_dir, 'my_fworker.yaml')):
        args.fworker_file = os.path.join(args.config_dir, 'my_fworker.yaml')

    if not args.queueparams_file and os.path.exists(os.path.join(args.config_dir, 'my_queueparams.yaml')):
        args.queueparams_file = os.path.join(args.config_dir, 'my_queueparams.yaml')

    launchpad = LaunchPad.from_file(args.launchpad_file) if args.launchpad_file else None
    fworker = FWorker.from_file(args.fworker_file) if args.fworker_file else FWorker()
    queue_params = QueueParams.from_file(args.queueparams_file)
    args.loglvl = 'CRITICAL' if args.silencer else args.loglvl

    # TODO: the number of arguments here is crazy!
    if args.command == 'rapidfire':
        rapidfire(queue_params, args.launch_dir, args.njobs_queue, args.njobs_block, args.loglvl, args.nlaunches, args.sleep, launchpad, fworker, args.reserve)
    else:
        launch_rocket_to_queue(queue_params, args.launch_dir, args.loglvl, launchpad, fworker, args.reserve)


if __name__ == '__main__':
    qlauncher_run()