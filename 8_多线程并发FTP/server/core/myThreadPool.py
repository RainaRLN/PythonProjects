#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2019/1/16

import queue
from threading import Thread


class ThreadPool:
    def __init__(self, max_tasks=None,):
        if max_tasks <= 0:
            raise ValueError("max_tasks must be greater than 0")
        self.task_queue = queue.Queue(max_tasks)
        for i in range(max_tasks):
            self.task_queue.put(Thread)

    def task_down(self):
        self.task_queue.put(Thread)

    def get_thread(self):
        return self.task_queue.get()
