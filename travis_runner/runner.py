import glob
import json
import subprocess

from . import generate


def main():
    generate.main()
    for env in glob.glob('.travis-runner-*.sh'):
        links = json.load(open(env + '.links'))
        link_arg = ''
        if links:
            subprocess.check_call(
                'docker run --name {name} {args} -d {image}'.format(**links),
                shell=True)
            link_arg = '--link {name}:{link}'.format(**links)
        try:
            subprocess.check_call(
                'docker run {} --rm -e http_proxy=$http_proxy -v $(pwd):/work'
                '  ubuntu:precise bash -ex /work/{}'.format(
                    link_arg, env), shell=True)
        except subprocess.CalledProcessError:
            if links:
                subprocess.check_call(
                    'docker rm -f {name}'.format(**links), shell=True)