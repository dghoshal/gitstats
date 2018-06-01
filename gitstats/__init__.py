import argparse
from gitstats.core.counts import GitStats

def get_version():
    version_file = resource_filename(Requirement.parse("gitstats"),"VERSION")
    with open(version_file) as f:
        version = f.readline().strip()
        return version

def _addDownloadsCounter(subparsers):
    parser_worker = subparsers.add_parser('downloads',
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_worker.add_argument('-t', '--tag', help="release tag")
    parser_worker.add_argument('-l', '--latest', help="get the latest release", action='store_true')
    parser_worker.set_defaults(action='downloads')

def _addClonesCounter(subparsers):
    parser_worker = subparsers.add_parser('clones',
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_worker.set_defaults(action='clones')


def _addForksCounter(subparsers):
    parser_worker = subparsers.add_parser('forks',
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_worker.set_defaults(action='forks')


def _addTotalCounter(subparsers):
    parser_worker = subparsers.add_parser('total',
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_worker.set_defaults(action='total')


def main():
    parser = argparse.ArgumentParser(description="",
                                     prog="gitstats",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()
    _addDownloadsCounter(subparsers)
    _addClonesCounter(subparsers)
    _addForksCounter(subparsers)
    _addTotalCounter(subparsers)

    parser.add_argument(dest='owner', help='owner of the github repo')
    parser.add_argument(dest='repo', help='name of the github repo')
    parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')
    parser.add_argument('-o', '--outfile', help='save the report')

    args = parser.parse_args()

    gitstats = GitStats(args.owner, args.repo, args.verbose)

    if args.action == 'downloads':
        gitstats.get_download_counts(args.tag, args.latest)
    elif args.action == 'clones':
        gitstats.get_clone_counts()
    elif args.action == 'forks':
        gitstats.get_fork_counts()
    else:
        gitstats.get_total_counts()

    if args.outfile:
        gitstats.save_report(args.outfile)
    else:
        gitstats.print_report()        

if __name__ == '__main__':
    main()
    
