import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python pagerank.py corpus")
    directory = "/Users/kingsley/Documents/cs50-ai/uncertainty/uncertainty-projects/pagerank/corpus0"
    #corpus = crawl(sys.argv[1])
    corpus = crawl(directory)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # initialize a starting dict:
    result = {}

    # for each page choose any random page and update probability accordingly
    for link, v in corpus.items():
        result[link] = (1-damping_factor)/len(corpus)

    # now check for the page and update the probability of the next page
    for link, v in corpus.items():
        if link == page:
            if v or len(v) != 0:
                for value in v:
                    result[value] = result[value] + damping_factor/len(v)

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {}

    # initial sample page
    for page in corpus:
        page_rank[page] = 0

    sample = None

    for i in range(n):
        # get first sample
        if sample == None:
            # randomly get a page:
            pages = list(corpus.keys())
            sample = random.choice(pages)
            page_rank[sample] += 1/n

        else:
            # get dsitribution from transition model for next sample
            next_sample = transition_model(corpus, sample, damping_factor)
            weights = list(next_sample.values())

            # get sample by choosing the from the distribution model
            sample = random.choices(pages, weights)[0]
            page_rank[sample] += 1/n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # initially set page_rank to be equally likely
    page_rank = {k: 1/len(corpus) for k, v in corpus.items()}
    temp = page_rank.copy()
    delta = 0.001

    count = 0  # counter for how many deltas are within 0.001
    iter = 0

    # while abs(delta) > 0.001:
    # continue tomorrow with a for loop.
    # just try it out before you start the loop:

    while True:
        # if this is the first iteration
        for page, values in corpus.items():
            sum_page = 0
            # sum the pages in a link
            for value in values:
                n = len(corpus[value])  # length of links of that value
                if n == 0:
                    sum_page += 1/len(corpus)
                else:
                    sum_page += page_rank[value]/n
            page_rank[page] = ((1 - damping_factor)/len(corpus)
                               ) + (sum_page * damping_factor)

        # check delta after 2+ iterations
        if iter > 1:
            for k, v in page_rank.items():
                if abs(temp[k]-page_rank[k]) < delta:
                    count += 1

        # if counter is 4 then all are within 0.001
        if count == len(corpus):
            print("iter", iter)
            return page_rank

        # else store previous value of page_rank and countinue loop
        else:
            temp = page_rank.copy()
            count = 0  # reset count
            iter += 1
            continue


if __name__ == "__main__":
    main()
