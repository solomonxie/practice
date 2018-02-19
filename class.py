#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():

    issue = Issue('hello')
    issue.update()




class Issue:
    config = ''
    title = 'init title'
    index = ''
    comments_url = ''
    counts = 0
    path = ''

    def __init__(self, tt):
        self.title = tt


    def update(self):
        print 'udate title:%s' % self.title


if __name__ == "__main__":
    main()
