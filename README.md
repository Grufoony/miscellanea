# miscellanea
Collection of miscellaneous things

## Table of contents
1. [YouTube Downloader](#youtube)
2. [pip Updater](#pip)
3. [doctest installer](#doctest)
4. [Article Template - LaTeX](#template)
5. [GitHub tricks](#github)

## downloader.py <div id='youtube'/>
A python script which help you to download and convert to mp3 from YouTube.

## updater.py <div id='pip'/>
A python script which help you to update all python's installed packages with pip.

## install_doctest.sh <div id='doctest'/>
A simple installer for the C++ library of doctest.
It will install the library into `usr/doctest/`, so it will be accessible with:
```c++
#include <doctest/doctest.h>
```
The script is executed with the command:
```shell
./install_doctest.sh
```

## article.tex <div id='template'/>
A LaTeX template for a scientific article, e.g. a lab report.

## GitHub tricks <div id='github'/>
If you want to delete in local all deleted branches of the git just do:
```shell
git fetch -p && for branch in $(git for-each-ref --format '%(refname) %(upstream:track)' refs/heads | awk '$2 == "[gone]" {sub("refs/heads/", "", $1); print $1}'); do git branch -D $branch; done
```

If you want to remove a file from git history you can do:
```shell
git filter-branch --index-filter 'git rm -rf --cached --ignore-unmatch path_to_file' HEAD
git push --force
```
