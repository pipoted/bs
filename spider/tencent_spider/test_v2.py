from multiprocessing import Queue
import time

queue = Queue()
dict_test = {'name': 'xiao', 'age': 18}

queue.put(dict_test)
queue.put(dict_test)
time.sleep(2)
while True:
    if queue.empty():
        break
    print(type(queue.get()))

print('this is end')
