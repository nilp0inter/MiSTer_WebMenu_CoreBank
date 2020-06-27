from fnmatch import fnmatch
from os.path import splitext
import argparse
import json
import os
import requests
import sys
import traceback
import xml.etree.ElementTree as ET

from github import Github, UnknownObjectException

try:
    token = os.environ['GITHUB_TOKEN']
except KeyError:
    print(('GITHUB_TOKEN environment variable must be '
           'defined with a valid Github Personal Access Token'),
          file=sys.stderr)
    sys.exit(1)


def get_mra_data(content):
    root = ET.fromstring(content)
    return {
        'name': root.findtext('./name'),
        'rbf': root.findtext('./rbf'),
        'zips': list(filter(None, (r.get('zip', None) for r in root.findall('./rom'))))
    }


def get_repo_releases(repo, paths):
    for path in paths:
        try:
            for release in repo.get_contents(path):
                if release.type == 'file':
                    _, ext = splitext(release.name.lower())
                    common = {
                        'name': release.name,
                        'sha': release.sha,
                        'url': release.download_url
                    }
                    if ext == '.rbf':
                        yield {**common,
                               'type': 'RBF',
                               }
                    elif ext == '.mra':
                        extra = None
                        try:
                            extra = get_mra_data(requests.get(release.download_url).content)
                        except:
                            print(f'Error processing MRA {repo.html_url}|{path}|{release.name}',
                                  file=sys.stderr)
                            traceback.print_exc(file=sys.stderr)

                        yield {**common,
                               'type': 'MRA',
                               'extra': extra
                               }
                    else:
                        yield {**common,
                               'type': 'OTHER',
                               }
                elif release.type == 'dir':
                    yield from get_repo_releases(repo, [os.path.join(path, release.name)])
                else:
                    # Symlink??
                    pass
        except UnknownObjectException:
            continue


def get_repos_data(user, repos, folders):
    for repo in user.get_repos():
        if not any(fnmatch(repo.name, pattern) for pattern in repos):
            continue
        try:
            readme = repo.get_readme().decoded_content.decode('utf-8')
        except:
            readme = None

        try:
            releases = list(get_repo_releases(repo, folders))
        except UnknownObjectException:
            print(f'No releases in {repo.html_url}. Skip', file=sys.stderr)
            continue

        yield {
            'name': repo.name,
            'description': repo.description,
            'readme': readme,
            'archived': repo.archived,
            'url': repo.html_url,
            'releases': releases
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user', nargs=1, help='Github user')
    parser.add_argument('-r', '--repo',
                        type=str,
                        action='append',
                        default=['*MiSTer*'],
                        help='Repository pattern')
    parser.add_argument('-f', '--folder',
                        type=str,
                        action='append',
                        default=['/releases'],
                        help='Folders to search for releases')

    args = parser.parse_args()
    username = args.user[0]

    user = Github(token).get_user(username)
    print(
        json.dumps({
            'name': username,
            'image': user.avatar_url,
            'url': user.html_url,
            'type': user.type,
            'repos': list(get_repos_data(user, repos=args.repo, folders=args.folder))
        },
        indent=2)
    )
