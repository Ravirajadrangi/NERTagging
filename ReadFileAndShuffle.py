from babel.localedata import exists

__author__ = 'pratik'
from __builtin__ import open
import random
import os
import sys
import csv

list_sentences = []
list_values = []
list_train_data = []
list_test_data = []


print "This program should read a file and shuffle it"




def read_file_and_populate_list_sentences():
    index = 0
    with open("./train-v2.iob") as file:
        sentence = []
        for line in file:
            print index
            list_line = line.strip().split()
            print list_line
            print len(list_line)
            if len(list_line)>0:
                sentence.append(list_line)
                if list_line[0] == '.':
                    list_sentences.append(sentence)
                    sentence = []
            index+=1

    for line in list_sentences:
        print line
    print index
    print len(list_sentences)

def shuffle_array():
    print list_sentences[0]
    random.shuffle(list_sentences)
    print list_sentences[0]

def split_training_test():
    test_length = int(0.30*len(list_sentences))

    test_data = list_sentences[:test_length]
    print len(test_data)
    train_data = list_sentences[test_length:]
    print len(train_data)
    return (test_data, train_data)


def write_test_file(list_test_data):
    if not os.path.exists('./test'):
        os.makedirs('./test')

    f = open('./test/testing_file_with_tags.csv', 'wt')
    try:
        writer = csv.writer(f)
        # for i in range(10):
        #     writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
        for list_sentence in list_test_data:
            for word_tag in list_sentence:
                print word_tag[0], word_tag[1]
                writer.writerow((word_tag[0], word_tag[1]))
    finally:
        f.close()

    f = open('./test/testing_file_without_tags.csv', 'wt')
    try:
        for list_sentence in list_test_data:
            for word_tag in list_sentence:
                print word_tag[0]
                f.write(word_tag[0]+'\n')
    finally:
        f.close()

    print open('./test/testing_file_without_tags.csv', 'rt').read()



def partition(lst, n):
    q, r = divmod(len(lst), n)
    indices = [q*i + min(i, r) for i in xrange(n+1)]
    return [lst[indices[i]:indices[i+1]] for i in xrange(n)]


def create_partitions_for_crossvalidation(list_train_data):
    list_partitions = []
    list_index_values = partition(range(0, len(list_train_data)), 7)
    """
    for list_partition in list_index_values:
        list_temp = []
        for index in list_partition:
            list_temp.append(list_sentences[index])
        list_partitions.append(list_temp)
        list_temp = []
    for list_sentences_partition in list_partitions:
        print len(list_sentences_partition)

    print "list partitions", list_partitions[0]
    print "list_values", list_index_values[0]

    """

    if not os.path.exists('./train'):
        os.makedirs('./train')
    i = 1
    print "List test data", len(list_train_data)
    for list_partition_index in list_index_values:
        print i, len(list_partition_index)
        print list_partition_index[0], list_partition_index[len(list_partition_index)-1]


        print list_train_data[list_partition_index[0]], list_train_data[list_partition_index[len(list_partition_index)-1]]

        f = open('./train/train_partition_'+str(i)+'.csv', 'wt')
        try:
            writer = csv.writer(f)
            for sentence_index in list_partition_index:
                for word in list_train_data[sentence_index]:
                    print i, sentence_index, word
                    writer.writerow((word[0], word[1]))
        finally:
            f.close()

        i += 1




def main():
    read_file_and_populate_list_sentences()
    shuffle_array()
    list_test_data, list_train_data = split_training_test()
    write_test_file(list_test_data)
    create_partitions_for_crossvalidation(list_train_data)
main()






