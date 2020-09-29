from subprocess import PIPE, Popen
import os
import json
from typing import List
import multiprocessing
import datetime
import argparse
from update_gitee_mirror_repo import update_gitee_mirror_repo
mirror_list = update_gitee_mirror_repo()


def get_github_branch_info(uri):
    cmd = f"curl --silent -X GET --header 'Content-Type: application/json;charset=UTF-8' 'https://api.github.com/repos/{uri}/branches/master'"
    r = os.popen(cmd)
    info: str = r.readlines()
    conf: List = json.loads(''.join(info))
    return conf

def get_gitee_branch_info(uri):
    cmd = f"curl --silent -X GET --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/repos/{uri}/branches/master'"
    r = os.popen(cmd)
    info: str = r.readlines()
    conf: List = json.loads(''.join(info))
    return conf

def check_update(uri):
    user, repo = uri.split('/')
    github = get_github_branch_info(uri)
    gitee = get_gitee_branch_info(f'zgpio/{repo}')
    github_sha = github['commit']['sha']
    gitee_sha = gitee['commit']['sha']
    if github_sha == gitee_sha:
        return True
    else:
        return False

def update_repo(uri: str, branch, dest):
    # TODO: git repo 完整性检查
    user, name = uri.split('/')
    if check_update(uri):
        return
    dest = os.path.join(dest, name)
    cmd1 = f'git clone -b {branch} https://gitee.com/zgpio/{name} {dest}'
    cmd2 = f'git -C {dest} remote add upstream https://github.com/{uri}.git'
    cmd3 = f'git -C {dest} pull upstream {branch}'
    cmd4 = f'git -C {dest} push origin {branch}'
    rev = f'git -C {dest} rev-parse HEAD'

    p1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
    p1.wait()

    p0 = Popen(rev, stdout=PIPE, stderr=PIPE, shell=True)
    p0.wait()
    pre = p0.stdout.read()

    p2 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
    p2.wait()

    p3 = Popen(cmd3, stdout=PIPE, stderr=PIPE, shell=True)
    p3.wait()

    p4 = Popen(cmd4, stdout=PIPE, stderr=PIPE, shell=True)
    p4.wait()

    p5 = Popen(rev, stdout=PIPE, stderr=PIPE, shell=True)
    p5.wait()
    after = p5.stdout.read()
    # print(pre, after)
    if pre != after:
        print(f'{uri:>40} update')


def update(dest, uri=None):
    global mirror_list
    if uri:
        mirror_list = [i for i in mirror_list if i.uri in uri]
        _ = [i.uri for i in mirror_list]
        print(_)
    # Multiprocessing 3 times faster than Single.
    start_tim = datetime.datetime.now()
    print("~" * 40)
    print('Start time:', start_tim.strftime('%Y-%m-%d %H:%M:%S'))
    pool = multiprocessing.Pool(processes=4)

    for plug in mirror_list:
        uri = plug.uri
        branch = plug.rev
        # 维持执行的进程总数为processes, 当一个进程执行完毕后会添加新的进程进去
        pool.apply_async(update_repo, (uri, branch, dest, ))

    pool.close()
    # 调用join之前, 先调用close函数, 否则会出错.
    # 执行完close后不会有新的进程加入到pool, join函数等待所有子进程结束
    pool.join()
    print("Sub-process(es) done.")

    end_tim = datetime.datetime.now()
    print('End time:', end_tim.strftime('%Y-%m-%d %H:%M:%S'))
    total_tim = end_tim - start_tim  # timedelta
    print('Total time:', str(total_tim))
    print("~" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update Scripts')
    parser.add_argument('--uri', type=str, nargs='+', help='specific update uri')
    parser.add_argument('--dest', type=str, default='~/Documents/dev/', help='destination')
    args = parser.parse_args()
    update(args.dest, args.uri)
