from distutils.core import setup

setup(
    name='ush',
    description='A One-stop configuration tool for Unity',
    url='https://github.com/freyja-dev/ush',
    version='0.0.1',
    author='Barneedhar Vigneshwar',
    author_email='barneedhar@ubuntu.com',
    license='GPLv3+',
    packages=['ush'],
    scripts=['ush-gtk'],
    package_data={'ush': ['data/*.ui','data/*.png',
                                'data/icons/24/*.svg','data/icons/36/*.svg']},
    data_files=[
        ('share/applications',
            ['ush.desktop']
        ),
    ]
)
