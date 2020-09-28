# -*- coding: utf-8 -*-
import os
import pickle
from typing import List
import json


class Plugin(object):
    def __init__(self, uri=None, rev='master', **kwargs):
        """
        :uri: '{user}/{name}'
        :rev: revision number or branch/tag name
        """
        self.uri = uri
        self.rev = rev
        for k, v in kwargs.items():
            setattr(self, k, v)


def get_info():
    # 可以直接在命令行中执行的命令
    cmd = "curl -X GET --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/users/zgpio/repos?type=all&sort=full_name&page=1&per_page=100'"
    r = os.popen(cmd)
    info: str = r.readlines()[0]  # 读取命令行的输出到一个list
    conf: List = json.loads(info)
    return conf


# TODO: 测试信息的准确性
# TODO: 当user不同, repo name相同时, 镜像到zgpio仓库中如何解决name冲突.
# TODO: 一些仓库默认不是master分支
config = {
    'neoclide/coc.nvim': {
        'rev': 'release'
    },
    'vim-airline/vim-airline': {
        'patch': True
    },
    'plasticboy/vim-markdown': {
        'patch': True
    },
}


def update_gitee_mirror_repo():

    fn = 'cache.pkl'
    try:
        with open(fn, 'rb') as f:
            conf = pickle.load(f)
    except Exception as e:
        print(e)
        conf = get_info()
        with open(fn, 'wb') as f:
            pickle.dump(conf, f)

    # 为了获取原仓库地址, 在仓库描述信息中填入 Mirror: 源仓库uri
    # {uri: config}
    conf = [{
        'uri': dic['description'][8:]
    } for dic in conf if dic['description'].find('Mirror:') != -1]

    for cfg in conf:
        if cfg['uri'] in config:
            cfg.update(config[cfg['uri']])
    # print(json.dumps(conf, sort_keys=True, indent=4, separators=(',', ':')))

    objs = map(lambda x: Plugin(**x), conf)
    # for o in objs:
    #     print(o.uri, o.rev, o.patch if hasattr(o, 'patch') else '')
    return objs


if __name__ == "__main__":
    update_gitee_mirror_repo()
