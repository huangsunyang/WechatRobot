import threading
import multiprocessing
import Queue
import time
import sys
from Utils.Timer import time_manager


class ThreadPool:
    def __init__(self, thread_limit=10):
        self.tasks = {}
        self.task_queue = Queue.Queue()
        self.thread_limit = thread_limit

        for i in range(thread_limit):
            self.tasks[i] = None

        self.tasks[thread_limit] = threading.Thread(target=self._queue_inspector, name="Timer and Queue Thread")
        self.tasks[thread_limit].start()

    def _run_task(self, no):
        func, time_limit = self.task_queue.get()
        new_thread = threading.Thread(target=func, name=str(no))
        self.tasks[no] = new_thread
        self.tasks[no].time_limit = time.time() + time_limit
        new_thread.start()


    def remove_task(self, no):
        #self.tasks[no].join()
        self.tasks[no] = None

    def _find_spare_thread(self):
        for i in range(self.thread_limit):
            if self.tasks[i] is None:
                return i
        return None

    def add_task(self, func, time_limit=1000):
        self.task_queue.put((func, time_limit))

    def _queue_inspector(self):
        while True:
            if not self.task_queue.empty():
                name = self._find_spare_thread()
                if name is not None:
                    self._run_task(name)
            self._check_timeout_tasks()
            time.sleep(0.2)

    def _check_timeout_tasks(self):
        for i in range(self.thread_limit):
            task = self.tasks[i]
            if task is not None:
                if task.time_limit < time.time():
                    print "task time out"


thread_pool = ThreadPool(8)
