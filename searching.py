
import os

def searching(word, file):

    initial = open(file, 'r+')
    if word in initial:
         print('Это уже есть')
    else:
         initial.write(word)
         print('записали ')





