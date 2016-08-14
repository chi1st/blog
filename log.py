# import inspect
# from termcolor import colored
#
#
# def log(*args):
#     try:
#         frame = inspect.getframeinfo(inspect.currentframe().f_back)
#         line_number = frame[1]
#         for line in frame[3]:
#             begin = line.find('(') + 1
#             end = line.rfind(')')
#             nameList = line[begin:end].split(',')
#             for name, value in zip(nameList, args):
#                 print(''.join([colored("debug ", "blue"), colored("{}".format(name), attrs=['bold']),
#                                colored(" ---> ", "white"), colored('{}    {}  {}'.format(value, type(value), line_number))]))
#     except:
#         print(colored("debug ", "red") + "something wrong")  # 我不知道会有哪些可能的错误

#-*- coding: utf-8 -*-
import time
def log(*args):
    t = time
    tt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(tt, *args)