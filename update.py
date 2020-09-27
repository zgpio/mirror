# -*- coding: utf-8 -*-
import os
import time

# https://update.gitter.im/osx/latest
# https://update.gitter.im/win/latest
# https://update.gitter.im/linux64/latest

# https://macos.telegram.org/
# https://github.com/macvim-dev/macvim/releases
# https://software.intel.com/en-us/articles/intel-power-gadget/
# Alacritty: https://github.com/jwilm/alacritty/releases


def get():
    os.system('mkdir repo')
    GITEE_TOKEN = os.environ['GITEE_TOKEN']
    # Issue: 需要定期清理gitee仓库悬空文件(管理>存储库GC), 查看仓库大小(统计>仓库大小)
    # Solution: 自动clear仓库
    clear_repo = ['linpkg', 'macpkg', 'winpkg']
    for repo in clear_repo:
        cmd = f"""
        curl -X PUT --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/repos/zgpio/{repo}/clear' -d '{{"access_token":"{GITEE_TOKEN}"}}'
        """
        os.system(cmd)

    github_releases = [
        {
            'mac': 'https://github.com/neovim/neovim/releases/download/nightly/nvim-macos.tar.gz',
            'win': 'https://github.com/neovim/neovim/releases/download/nightly/nvim-win64.zip',
            'lin': 'https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage',
        },
        {
            'mac': 'https://github.com/kovidgoyal/kitty/releases/download/v0.18.3/kitty-0.18.3.dmg',
        },
        # {
        #     'mac': 'https://github.com/qinyuhang/ShadowsocksX-NG-R/releases/download/1.4.4-r8/ShadowsocksX-NG-R8.dmg',
        # },
        {
            'mac': 'https://github.com/archagon/sensible-side-buttons/releases/download/1.0.6/SensibleSideButtons-1.0.6.dmg',
        },
        # {
        #     'mac': 'https://github.com/citra-emu/citra-nightly/releases/download/nightly-1619/citra-osx-20200906-e97ecdc.tar.gz',
        # },
        # {
        #     'win': 'https://github.com/citra-emu/citra-canary/releases/download/canary-1848/citra-windows-mingw-20200906-c997347.7z'
        #     'win': 'https://github.com/citra-emu/citra-nightly/releases/download/nightly-1619/citra-windows-mingw-20200906-e97ecdc.7z'
        # },
    ]
    # TODO: version detect
    for i in github_releases:
        for j, url in i.items():
            os.system(f'wget -P repo-{j} {url}')


if __name__ == "__main__":
    get()
