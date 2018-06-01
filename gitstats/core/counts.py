"""
`gitstats.core.counts`
====================================
.. currentmodule:: 

:platform: Unix, Mac
:synopsis: Module to count the total downloads for a Github repository
         : [Total Downloads = Release Downloads + Clones + Forks]

.. moduleauthor:: Devarshi Ghoshal <dghoshal@icloud.com>
"""

import json
import urllib.request as urllib
import os
import sys
from tabulate import tabulate
import time

class GitStats():
    def __init__(self, owner, repo, verbose=False):
        self.owner = owner
        self.repo = repo
        self.verbose = verbose
        self.auth_token = self._get_auth_token_()
        self.base_url = self._get_base_url_()
        self.repo_info = {}
        self.headers = {'downloads': ['Count', 'Tag', 'URL', 'Publish Date'],
                        'clones': ['Count', 'Uniques', 'Last Cloned Date'],
                        'forks': ['Count', 'Forks URL']}
        self.total_downloads = -1
        self.counts = {}
        self._set_repo_info_()

    def _get_base_url_(self):
        url = "https://api.github.com/repos/{}/{}".format(self.owner, self.repo)
        return url

    def _get_auth_token_(self):
        token = None if "GITHUB_TOKEN" not in os.environ else os.environ["GITHUB_TOKEN"]
        return token

    def _set_repo_info_(self):
        url = "{}".format(self.base_url)
    
        stats = self.get_response(url)
        self.repo_info['name'] = stats['name']
        self.repo_info['url'] = stats['owner']['html_url']
        self.repo_info['type'] = 'Private' if stats['private'] else 'Public'
        self.repo_info['language'] = stats['language']

    def get_response(self, url):
        auth = {} if not self.auth_token else {"Authorization": "token "+self.auth_token}
        request = urllib.Request(url, headers=auth)
        response = '{}'
        try:
            response = urllib.urlopen(request).read().decode("utf-8")
        except Exception as e:
            print("Error {}: {}".format(e.code, e.reason))
            sys.exit(-1)

        stats = json.loads(response)
        return stats


    def _get_release_download_(self, stat):
        downloads = 0
        if "assets" in stat:
            for asset in stat["assets"]:
                downloads += asset["download_count"]

        return downloads


    def get_download_counts(self, tag=None, latest=False):
        url = "{}/releases{}".format(self.base_url, ("" if not tag else "/tags/"+tag) if not latest else "/latest")
    
        stats = self.get_response(url)
        downloads = []
        total_downloads = 0
        if isinstance(stats, dict):
            count = self._get_release_download_(stats)
            published = (time.strftime("%c", time.strptime(stats["published_at"], "%Y-%m-%dT%H:%M:%SZ"))
                         if stats["published_at"] else "Unpublished")
            downloads.append([count, stats["tag_name"], stats["html_url"], published])
            total_downloads = count
        else:
            for stat in stats:
                 count = self._get_release_download_(stat)
                 published = (time.strftime("%c", time.strptime(stat["published_at"], "%Y-%m-%dT%H:%M:%SZ"))
                              if stat["published_at"] else "Unpublished")
                 downloads.append([count, stat["tag_name"], stat["html_url"], published])
                 total_downloads += count
                 
        self.counts['downloads'] = downloads
        return total_downloads


    def get_fork_counts(self):
        url = "{}".format(self.base_url)
    
        stats = self.get_response(url)
        forks_count = stats["forks_count"]
        forks = [[forks_count, stats["forks_url"]]]

        self.counts['forks'] = forks

        return forks_count


    def get_clone_counts(self):
        """
        Need OAuth token to access clone counts
        """
        if not self.auth_token:
            print("Environment variable `GITHUB_TOKEN` is not set.")
            print("Setting Clone counts to 0.")
            print("To get correct Clone counts, set `GITHUB_TOKEN`.")
            print("\n")
            #print("\t export GITHUB_TOKEN = <Github OAuth token>")
            return 0

        url = "{}/traffic/clones".format(self.base_url)
    
        stats = self.get_response(url)
        total_clones = stats["count"]
        unique_clones = stats["uniques"]
        clone_list = stats["clones"]
        last_cloned_at = ''
        if len(clone_list) > 0:
            last_cloned_at = (time.strftime("%c", time.strptime(clone_list[-1:][0]["timestamp"],
                                                                "%Y-%m-%dT%H:%M:%SZ")))

        clones = [[total_clones, unique_clones, last_cloned_at]]

        self.counts['clones'] = clones

        return unique_clones


    def get_total_counts(self):
        downloads = self.get_download_counts()
        forks = self.get_fork_counts()
        clones = self.get_clone_counts()
        
        self.total_downloads = downloads + forks + clones
            
        return self.total_downloads

        
    def print_report(self):
        if self.verbose:
            print("\n")
            for metadata in self.repo_info:
                print("{}: {}".format(metadata.upper(), self.repo_info[metadata]))
            print("\n")
            for count_type in self.counts:
                print("{} stats:".format(count_type.title()))
                print(tabulate(self.counts[count_type], self.headers[count_type], tablefmt="grid"))
                print("\n")
        else:
            for count_type in self.counts:
                counts_detail = self.counts[count_type]
                count = 0
                for detail in counts_detail:
                    count += detail[0]
                print("{} = {}".format(count_type.title(), count))

        if self.total_downloads >= 0:
            print("Total = {}".format(self.total_downloads))

        
    def save_report(self, filename):
        sys.stdout = open(filename, 'w')
        self.print_report()
        


if __name__ == '__main__':
    owner = 'octocat'
    repo = 'linguist'
    git_stats = GitStats(owner, repo, True)
    counts = git_stats.get_total_counts()
    git_stats.print_report()

    
