
from setuptools import setup

from webspider import version


setup(
    name="WebSpider",
    version=version,
    description="Web Spider Library",
    url="https://github.com/liuyug/WebSpider",
    license="BSDv3",
    author="Yugang LIU",
    author_email="liuyug@gmail.com",
    packages=[
        'webspider',
        'webspider.spider',
        'webspider.tests',
        'webspider.searchengine',
        'webspider.scripts',
    ],
    entry_points={
        'console_scripts': [
            'websearch = webspider.scripts.websearch:main',
        ],
    },
    zip_safe=False,
)
