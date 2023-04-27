import Magi
import multiprocessing as mp
import time
import numpy as np

def dummy(text = "None"):
    import time
    index = 0
    print("this is the dummy function")
    with open("dummy.txt","w") as f:
        for i in range(10):
            f.write(f"{text} {index}\n")
            index += 1
            time.sleep(1)

def dummy2(magi_queue):
    import time
    import Magi
    magi = Magi.Magi()
    for i in range(10):
        print("hello")
        magi.queue_put(magi_queue, f"message from remote system {i}")
        time.sleep(1)


def local_test1(queue_deets):
    iters = 1000
    magi = Magi.Magi()
    start = time.time()
    data = np.random.random((10,10))
    for i in range(iters):
        magi.queue_put(queue_deets, data)
    mid = time.time()
    for i in range(iters):
        rcvd = magi.queue_get(queue_deets)
    end = time.time()
    p1 = (mid-start)/iters
    p2 = (end - mid)/iters
    print(f"put = {p1*1000}ms/conn get = {p2*1000}ms/conn\nfinished")        

def master_test1():
    magi = Magi.Magi()
    magi.register_network_thread('192.168.0.6')
    print(magi.network_threads) 

def master_test2():
    magi = Magi.Magi()
    magi.register_network_thread('192.168.0.6')    
    magi.process(target = dummy, args = ("hey there!"))

def master_test3():
    magi = Magi.Magi()
    magi_queue = magi.queue()
    magi.register_network_thread('192.168.0.6')   
    magi.process(target = dummy2, args=(magi_queue,))
    while 1:
        data = magi.queue_get(magi_queue)
        if data != None:
            print(data)

if __name__ == '__main__':
    # magi = Magi.Magi()
    # queue_deets = magi.queue()
    # test1(queue_deets)
    # magi.kill_queues()
    # ports = []
    # for i in range(8):
    #     ports.append(magi.Queue())
    
    master_test3()