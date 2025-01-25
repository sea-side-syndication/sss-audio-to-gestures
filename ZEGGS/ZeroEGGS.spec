# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['generate.py'],
    pathex=['C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS'],
    binaries=[],
    datas=[
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/data_pipeline.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/dataset.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/helpers.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/main.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/modules.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/optimizers.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/train.py', '.'),
        ('C:/UE/Projects/VTUBER/Python/ZeroEGGS/ZEGGS/utils.py', '.'),

     ('anim/*', 'anim'),
     ('audio/*', 'audio'),
    ],

    hiddenimports=[
    'anim', 'audio', 'torch', 'pandas', 'omegaconf', 'scipy',
    'sox', 'rich', 'tensorboard', 'pyloudnorm', 'numpy', 'python-dateutil',
    'torchvision', 'cudatoolkit', 'pytorch'],


    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='generate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
