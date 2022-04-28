import os
import random
import re
import sys
from pagerank import *

DAMPING = 0.85
SAMPLES = 10000
directory = "/Users/kingsley/Documents/cs50-ai/uncertainty/uncertainty-projects/pagerank/corpus0"

corpus = crawl(directory)
page = "3.html"

print(corpus)
#print(transition_model(corpus, page, DAMPING))
# initialize a starting dict:
result = {}

# for each page choose any random page
# for link, v in corpus.items():
#     result[link] = (1-DAMPING)/len(corpus)

# for link, v in corpus.items():
#     if link == page:
#         if v or len(v) != 0:
#             for value in v:
#                 result[value] = result[value] + DAMPING/len(v)

# print(result)

#print(sample_pagerank(corpus, DAMPING, 10000))
