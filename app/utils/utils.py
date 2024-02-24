def jaccard_similarity(text1:str, text2:str, n=3):
    # Generate n-grams for text1
    ngrams1 = set()
    for i in range(len(text1)-n+1):
        ngrams1.add(text1[i:i+n])

    # Generate n-grams for text2
    ngrams2 = set()
    for i in range(len(text2)-n+1):
        ngrams2.add(text2[i:i+n])

    # Calculate the Jaccard similarity coefficient
    intersection = len(ngrams1.intersection(ngrams2))
    union = len(ngrams1.union(ngrams2))

    similarity = intersection / union
    return similarity
