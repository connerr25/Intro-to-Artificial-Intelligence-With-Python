import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
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
    n = len(corpus)
 
    result = dict()
    page_length = len(corpus[page])
    for i in corpus:
        if len(corpus[page]) != 0:
            if i in corpus[page]:
                result[i] = (1 - damping_factor) / n + damping_factor / page_length
            else:
                result[i] = (1 - damping_factor) / n
        else:
            result[i] = 1 / n
            
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    result = dict()
    for i in corpus:
        result[i] = 0
    page = np.random.choice(list(corpus.keys()))
    for i in range(n):
        result[page] += 1
        probability = transition_model(corpus, page, damping_factor)
        key = list(probability.keys())
        value = list(probability.values())
        page = np.random.choice(key, p=value)
    
    for i in corpus:
        result[i] /= n
        
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
  
    number_of_links = dict()
    corpus2 = dict()
    for i in corpus:
        corpus2[i] = set()
       
        if (len(corpus[i]) == 0):
            corpus[i] = set(corpus.keys())
        
    for i in corpus:
        for j in corpus[i]:
            corpus2[j].add(i)
        number_of_links[i] = len(corpus[i])
                
    n = len(corpus)
  
    result = dict()
    for i in corpus:
        result[i] = 1 / n
    while True:
        seperatep = dict()
        for i in corpus:
            seperatep[i] = (1 - damping_factor) / n
            for j in corpus2[i]:
                seperatep[i] += damping_factor * result[j] / number_of_links[j]
        s = 0      
        cond = True
        for i in corpus:
            difference = abs(seperatep[i] - result[i])
            if difference > 0.001:
                cond = False
            result[i] = seperatep[i]
            s += result[i]
        
        if cond:
            break
    
    return result



if __name__ == "__main__":
    main()
