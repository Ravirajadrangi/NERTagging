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

    f = open('./test/testing_file_with_tags.tsv', 'w')
    try:

        # for i in range(10):
        #     writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
        for list_sentence in list_test_data:
            for word_tag in list_sentence:
                print word_tag[0], word_tag[1]
                f.write(str(word_tag[0]+'\t'+'\t'+word_tag[1]+'\n'))
    finally:
        f.close()

    f = open('./test/testing_file_without_tags.tsv', 'w')
    try:
        for list_sentence in list_test_data:
            for word_tag in list_sentence:
                print word_tag[0]
                f.write(word_tag[0]+'\n')
    finally:
        f.close()

    print open('./test/testing_file_without_tags.tsv', 'r').read()

def write_train_file(list_train_data):
    if not os.path.exists('./train'):
        os.makedirs('./train')

    f = open('./train/train_data.tsv', 'w')
    try:

        # for i in range(10):
        #     writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
        for list_sentence in list_train_data:
            for word_tag in list_sentence:
                print word_tag[0], word_tag[1]
                f.write(str(word_tag[0]+'\t'+word_tag[1]+'\n'))
    finally:
        f.close()



def partition(lst, n):
    q, r = divmod(len(lst), n)
    indices = [q*i + min(i, r) for i in xrange(n+1)]
    return [lst[indices[i]:indices[i+1]] for i in xrange(n)]


def create_partitions_for_crossvalidation(list_train_data):
    list_partitions = []
    list_index_values = partition(range(0, len(list_train_data)), 7)
    if not os.path.exists('./train'):
        os.makedirs('./train')
    i = 1
    print "List train data", len(list_train_data)
    for list_partition_index in list_index_values:
        print i, len(list_partition_index)
        print list_partition_index[0], list_partition_index[len(list_partition_index)-1]


        print list_train_data[list_partition_index[0]], list_train_data[list_partition_index[len(list_partition_index)-1]]

        f = open('./train/train_partition_'+str(i)+'.tsv', 'w')
        try:
            writer = csv.writer(f)
            for sentence_index in list_partition_index:
                for word in list_train_data[sentence_index]:
                    print i, sentence_index, word
                    f.write(str(word[0]+'\t'+word[1]+'\n'))
        finally:
            f.close()

        i += 1

def create_crossvalidation_sets():
    if not os.path.exists('./cross_validation'):
        os.makedirs('./cross_validation')
    for i in range(1,8):
        list_train_cv = []
        list_test_cv = []
        print type(list_test_cv)
        print type(list_test_cv)
        if not os.path.exists('./cross_validation/cv_set_'+str(i)):
            os.makedirs('./cross_validation/cv_set_'+str(i))
        for j in range(1,8):
            if i == j:
                with open('./train/train_partition_'+str(i)+'.tsv', 'r') as file:
                    for line in file:
                        list_test_cv.append(line)

                with open('./cross_validation/cv_set_'+str(i)+'/test.tsv', 'w') as test_file:
                    for line in list_test_cv:
                        list_line = line.strip().split('\t')
                        test_file.write(str(list_line[0]+'\t'+'\t'+list_line[1]+'\n'))


            else:
                with open('./train/train_partition_'+str(j)+'.tsv', 'r') as file:
                    for line in file:
                        list_train_cv.append(line)

        with open('./cross_validation/cv_set_'+str(i)+'/train.tsv', 'w') as train_file:
            for line in list_train_cv:
                train_file.write(line)






def main():
    read_file_and_populate_list_sentences()
    shuffle_array()
    list_test_data, list_train_data = split_training_test()
    write_test_file(list_test_data)
    write_train_file(list_train_data)
    create_partitions_for_crossvalidation(list_train_data)
    create_crossvalidation_sets()
main()






