#encoding:utf-8

import nltk
from nltk.corpus.reader import TaggedCorpusReader, PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer

chinese_pattern = ",#PU|\.#PU|，#PU|。#PU|\?#PU|\!#PU|:#PU|：#PU|？#PU|！#PU|;#PU|；#PU|\n".decode("utf-8")

class PlainChineseReader(PlaintextCorpusReader):

    def __init__(self, sep="/", 
                 # Note that . needs to be escaped
                 pattern = chinese_pattern,
                 root=None, fileids=None):
        """docstring for __init__"""
        PlaintextCorpusReader.__init__(
            self,
            sep=sep, root=root, fileids=fileids,
            sent_tokenizer = RegexpTokenizer(pattern, gaps=True),
            encoding="utf-8")

class TaggedChineseReader(TaggedCorpusReader):

    def __init__(self, sep="/", 
                 # Note that . needs to be escaped
                 pattern = chinese_pattern, 
                 root=None, fileids=None):
        """docstring for __init__"""
        TaggedCorpusReader.__init__(
            self,
            sep=sep, root=root, fileids=fileids,
            sent_tokenizer = RegexpTokenizer(pattern, gaps=True),
            encoding="utf-8")

def mask_by_stopwords(li, stopwords=[], tag = "x"):
    stopwords = set(stopwords)
    li2 = [e in stopwords and tag or '-' for e in li]
    return li2

def mask_by_tags(li, stoptags=['PU'],  tag = 'x'):
    stoptags = set(stoptags)
    li2 = [t in  stoptags and tag or '-' for (w, t) in li]
    return li2

def mask_by_puncts(li, tag='x'):
    from string import punctuation
    chinese_puncts="！？，。、“；‘".decode("utf-8")
    import re
    s = "[" + punctuation + chinese_puncts + "]"
    li2 = [re.search(s, e) and tag or '-' for e in li]
    return li2

def mask_by_frequency(li, words, tag='x'):
    infreq_words = set(words)
    li2 = [e in infreq_words and tag or '-' for e in li]
    return li2

def combine_mask(masks, tag='x'):
    final = [tag in e and tag or '-' for e in masks]

    return final

def extract_by_mask(li, mask, tag='x', exclude=True):
    """docstring for extract_by_mask"""
    li2 = []
    for i, m in enumerate(mask):
        if exclude:
            if m != tag:
                li2.append(li[i])
        else:
            if m == tag:
                li2.append(li[i])

    return li2


def test():
    stopwords = ['of', 'the']
    li = "the best of the time".split()
    print mask_by_stopwords(li,stopwords)

def test1():
    words = "the best !".decode("utf-8").split()
    tags = ['DT', 'VA', 'PU']
    li2 = zip(words, tags)

    print mask_by_tags(li2)

def test2():
    """docstring for test2"""
    li = "我们 。 大家 好，".decode("utf-8").split()
    print mask_by_puncts(li)

def test3():
    """docstring for test3"""
    mask1 = ['x', '-', 'x']
    mask2 = ['x', '-', '-']

    masks = zip(mask1, mask2)

    print combine_mask(masks)


if __name__ == '__main__':
    test()
    test1()
    test2()
    test3()
