from threading import Thread


def work(id, start, end, result):
    total = 0
    for i in range(start, end):
        total += i
        # print(i)
    result.append(total)
    print(total,end=" ")
    return

if __name__ == "__main__":
    START, END = 0, 1000
    result = list()
    th1 = Thread(name="th1", target=work, args=(1, START, END, result))
    th2 = Thread(target=work, args=(2, START, END, result))
    print(th1.name)
    print(th2.name)
    th1.start()
    th2.start()

    th1.join()
    th2.join()

print(f"Result: {sum(result)}")