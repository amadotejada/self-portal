# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('resources', 'resources'), ('conf', 'conf')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Self Portal',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

darwin = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main' )

# Build a .app if on OS X
if sys.platform == 'darwin':
    app = BUNDLE(darwin,
            name='Self Portal.app',
            icon='appicon.ico',
            bundle_identifier=None,
            version='0.7.0',
            info_plist={
                'NSPrincipalClass': 'NSApplication',
                'NSAppleScriptEnabled': False,
                'NSHumanReadableCopyright': '2021 Amado Tejada',
                'NSHighResolutionCapable': 'True',
                'CFBundleDocumentTypes': [
                    {
                        'CFBundleTypeName': 'app',
                        'CFBundleTypeIconFile': 'appicon.ico',
                        'LSItemContentTypes': ['com.amadotejada.selfportal'],
                        'LSHandlerRank': 'Owner',
                        'CFBundleTypeRole': 'None'
                        }
                    ]
                },
            )

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Self Portal',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          icon='appicon.ico',
          codesign_identity=None,
          entitlements_file=None)
