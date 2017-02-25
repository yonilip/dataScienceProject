from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "lipton green tea"
doc_b = "is green tea good for you?"
doc_c = "lipton soup best"
doc_d = "tomato soup recipe"
doc_e = "best tea brand"

doc_x = "westworld explained, westworld season 2 theory, westworld nerdwriter, MSE, linear relation, linear relation symbol, perplexity translatr, perplexity translate, naive bayes, radiohead live, myxomatosis radiohead, myxomatosis,norm, log linear model regularization, radiohead wiki"

# compile sample documents into a list
#doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
doc_set = [s for s in doc_x.split(",")]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
