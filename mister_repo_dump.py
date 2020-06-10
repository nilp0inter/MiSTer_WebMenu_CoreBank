from os.path import splitext
import json
import os
import sys
import traceback
import xml.etree.ElementTree as ET

from github import Github, UnknownObjectException

try:
    token = os.environ['GITHUBAPI_TOKEN']
except KeyError:
    print(('GITHUBAPI_TOKEN environment variable must be '
           'defined with a valid Github Personal Access Token'),
          file=sys.stderr)
    sys.exit(1)

try:
    username = sys.argv[1]
except IndexError:
    print(f'Usage: {sys.argv[0]} [github-user]', file=sys.stderr)
    sys.exit(1)

def get_mra_data(content):
    root = ET.fromstring(content)
    return {
        'name': root.findtext('./name'),
        'rbf': root.findtext('./rbf'),
        'zips': list(filter(None, (r.get('zip', None) for r in root.findall('./rom'))))
    }


def get_repo_releases(repo, path):
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
                    extra = get_mra_data(release.decoded_content)
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
            yield from get_repo_releases(repo, os.path.join(path, release.name))
        else:
            # Symlink??
            pass


def get_repos_data(user):
    for repo in user.get_repos():
        try:
            readme = repo.get_readme().decoded_content.decode('utf-8')
        except:
            readme = None

        try:
            releases = list(get_repo_releases(repo, '/releases'))
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
    user = Github(token).get_user(username)
    print(
        json.dumps({
            'name': username,
            'image': user.avatar_url,
            'url': user.html_url,
            'type': user.type,
            'repos': list(get_repos_data(user))
        })
    )
