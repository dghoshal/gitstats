******************************************************************************
GitStats: Python package to count the total downloads for a Github repository

* Author: Devarshi Ghoshal    	                       		      
* v1.0.0
* Created: May 31, 2018
******************************************************************************



PRE-REQUISITES
--------------
* Python (>= 2.7)
* pip (>= 9.0)

Build
------
Download the [repository](https://github.com/dghoshal/gitstats/releases/download/v1.0.0/gitstats-1.0.0.zip)

To build GitStats, run the setup script:

        python setup.py install

Usage
-----

        gitstats downloads [-t TAG] [-l] owner repo [-v] [-o OUTFILE]
        gitstats clones owner repo [-v] [-o OUTFILE]
        gitstats forks owner repo [-v] [-o OUTFILE]
        gitstats total owner repo [-v] [-o OUTFILE]

* Positional arguments:

        owner: user/owner of the repository
        repo: name of the repository

* Options:

        -v/--verbose: verbose output/detailed download count report
        -o OUTFILE: save the download count report to <OUTFILE>

* Additional options for getting release downloads:

        -t TAG: release tag
        -l/--latest: latest release 

For clone counts and private repositories, the environment variable GITHUB_TOKEN must be set.

Examples
--------

        gitstats downloads -t <TAG> owner repo    : get download counts for the release <TAG>
        gitstats clones owner repo                : get clones counts for the repository `repo`
        gitstats forks owner repo                 : get forks counts for the repository `repo`
        gitstats total owner repo -v -o <OUTFILE> : save the detailed report of the total count

        