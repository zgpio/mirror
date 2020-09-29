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
    GITEE_TOKEN = os.environ['GITEE_TOKEN']
    USER_PASSWORD = os.environ['USER_PASSWORD']
    # Issue: 需要定期清理gitee仓库悬空文件(管理>存储库GC), 查看仓库大小(统计>仓库大小)
    # Solution: 自动clear仓库
    clear_repo = ['linpkg', 'macpkg', 'winpkg']
    for repo in clear_repo:
        cmd = f"""
        curl -X PUT --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/repos/zgpio/{repo}/clear' -d '{{"access_token":"{GITEE_TOKEN}"}}'
        """
        os.system(cmd)

    github_releases = {
        'mac': [
            'https://github.com/neovim/neovim/releases/download/nightly/nvim-macos.tar.gz',
            'https://github.com/kovidgoyal/kitty/releases/download/v0.18.3/kitty-0.18.3.dmg',
            'https://github.com/archagon/sensible-side-buttons/releases/download/1.0.6/SensibleSideButtons-1.0.6.dmg',
            # 'https://github.com/qinyuhang/ShadowsocksX-NG-R/releases/download/1.4.4-r8/ShadowsocksX-NG-R8.dmg',
            # 'https://github.com/citra-emu/citra-nightly/releases/download/nightly-1619/citra-osx-20200906-e97ecdc.tar.gz',
        ],
        'win': [
            'https://github.com/neovim/neovim/releases/download/nightly/nvim-win64.zip',
            # 'https://github.com/citra-emu/citra-canary/releases/download/canary-1848/citra-windows-mingw-20200906-c997347.7z'
            # 'https://github.com/citra-emu/citra-nightly/releases/download/nightly-1619/citra-windows-mingw-20200906-e97ecdc.7z'
        ],
        'lin': [
            'https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage',
        ],
    }
    # TODO: version detect
    for system, pkgs in github_releases.items():
        path = f'{system}pkg'
        for url in pkgs:
            os.system(f'wget -q -P {path} {url}')

        os.system(f'git -C {path} init')
        os.system(f'git -C {path} add .')
        os.system(f'git -C {path} commit -m "init"')
        os.system(f'git -C {path} remote add origin https://{USER_PASSWORD}@gitee.com/zgpio/{path}.git > /dev/null 2>&1')
        os.system(f'git -C {path} push origin master')


if __name__ == "__main__":
    get()
