
import time
import multiprocessing
import threading
import concurrent.futures 


def dosomthing():
    print("sleep one seconde....")
    time.sleep(1)
    print("done sleeping!")

start = time.perf_counter()
proc = []
thread = []
number = 5

for _ in range(number):
    m = multiprocessing.Process(target=dosomthing)
    t = threading.Thread(target=dosomthing)
    proc.append(m)
    thread.append(t)
    m.start()
    t.start()

for x,pro in enumerate(proc):
    thread[x].join()
    pro.join()


end = time.perf_counter()

print(f"the application took {round(end-start,3)} secondes")