

import threading

print('...部分代码...')
threading.Event().wait(5)
print('...剩下的代码...')


import threading

class Checker(threading.Thread):
    def __init__(self, event):
        super().__init__()
        self.event = event

    def run(self):
        while not self.event.is_set():
            print('检查 redis 是否有数据')
            self.event.wait(60)

trigger_task() # 异步任务
event = threading.Event()
checker = Checker(event)
checker.start()
if user_cancel_task(): # 可以马上停止
    event.set()