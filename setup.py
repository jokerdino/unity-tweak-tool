from distutils.core import setup

setup(
    name='unity-tweak-tool',
    description='A One-stop configuration tool for Unity',
    url='https://github.com/freyja-dev/unity-tweak-tool',
    version='0.0.2',
    author='Barneedhar Vigneshwar',
    author_email='barneedhar@ubuntu.com',
    license='GPLv3+',
    packages=['unitytweak'],
    scripts=['unity-tweak-tool'],
    package_data={'unitytweak': ['data/*.ui','data/*.png',
                                'data/icons/24/*.svg','data/icons/36/*.svg']},
    data_files=[
        ('share/applications',
            ['unity-tweak-tool.desktop']
        ),
    ]
)
