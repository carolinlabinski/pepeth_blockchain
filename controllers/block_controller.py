from utils.w3 import w3
import threading
import json


def block_number():
    return w3.eth.get_block_number()


def blocks_prop(count=1000, prop='size'):
    last = block_number()
    props = dict()
    threads = []
    for i in range(count):
        s = threading.Thread(target=get_block_data, args=(last - count + i, prop, props, i))
        s.start()
        threads += [s]
    for t in threads:
        t.join()
    return {prop: props}


def get_block_data(nth_block, prop, props, index):
    block = w3.eth.getBlock(nth_block)
    props[index] = (nth_block,  block[prop])



def block_transactions_count(count=1000, prop='transactions'):
    last = block_number()
    props = dict()
    threads = []
    for i in range(count):
        s = threading.Thread(target=get_block_data, args=(last - count + i, prop, props, i))
        s.start()
        threads += [s]
    for t in threads:
        t.join()
    return {prop: len(props)}