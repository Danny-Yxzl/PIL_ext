from setuptools import setup, find_packages

setup(
    name='musicapi',
    version='0.1',
    description='Some extend methods for Pillow(PIL)',
    url="https://github.com/Danny-Yxzl/PIL_ext",
    author="Yixiangzhilv",
    author_email="mail@yixiangzhilv.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    keywords="image PIL",
    install_requires=["Pillow"],
    packages=find_packages(),
    project_urls={
        "Bug Reports": "https://github.com/Danny-Yxzl/PIL_ext/issues",
        "Say Thanks!": "https://www.yixiangzhilv.com/",
        "Source": "https://github.com/Danny-Yxzl/PIL_ext",
    },
)
