from collections import Counter 
from nltk.corpus import stopwords
from nltk import word_tokenize
import numpy as np
from metapub import PubMedFetcher
from wordcloud import WordCloud

class MyKMeans(object):

    def __init__(self, number_of_clusters, number_iterations):
        self.k = number_of_clusters
        self.num_iter = number_iterations

    def kmeans(self, data):
        self.data = data

        centroids = self.get_start_centroids()



        for i in range(self.num_iter):
                labels = self.getLabels(centroids)
                centroids = self.getCentroids(labels)

        self.centroids = centroids 
        self.labels = labels

    def getLabels(self, centroids):
        
        '''
        gets labels based on defined centroids
        
        Paramters
        ---------
        centroids : numpy array
            shape (number of clusters, number of features) defines 
            location of centrods that classify datapoints
            
        Returns
        -------
        labels : numpy array
            shape (number of observations, 1), contains predictions 
            for datapoints based on closest location to centroids
        '''

        distances = []

        for row in range(centroids.shape[0]):
            
            centroid = centroids[row, :]
            
            dis = np.power(np.sum(np.power(self.data - centroid, 2), axis = 1), 0.5)
            distances.append(dis)

        out = np.vstack(distances)
        labels = np.argmin(out, axis = 0)
        
        return(labels)

    def getCentroids(self, labels):
        
        '''
        get centroids based on new labels
        
        Parameters
        ----------
        labels : numpy array
            shape (number of observations, 1), contains predictions 
            for datapoints based on closest location to centroids
        
        Returns
        -------
        centroids : numpy array
            shape (number of clusters, number of features) defines 
            location of centrods that classify datapoints
        '''


        centroids = np.zeros(shape=(self.k, self.data.shape[1]))

        for label in range(self.k):


            centroids[label, :] = np.mean(self.data[labels == label, :], axis =0)
            
        try:    
            #if there are nans because no observations are assigned to a given label then reinitialise centroid
            centroids[np.isnan(centroids)] = np.mean(self.data, axis = 0)
        except:
            pass

        return(centroids)
    
    def get_start_centroids(self):
        
        '''
        generates random coordinates of centroids sampling from 
        normal distribution with same mean and standard 
        deviation as feature data
        
        parameters
        ----------
        None
        
        Returns
        -------
        starting : numpy array   
            shape (number of clusters, number of features) defines 
            location of random centroids   
            
        '''
        average = np.mean(self.data)
        std = np.std(self.data)
        
        starting = np.zeros(shape = (self.k, self.data.shape[1]))
        
        for row in range(self.k):
            
            noise = np.random.normal(average, std, (1, self.data.shape[1]))
            
            starting[row, :] = noise
            
        return(starting)
    
    

class ClusterAbstract(object):
    
    """
    class for clustering abstracts
    
    Attributes
    ----------
    
    stop_words: list, contains stop words from nltk library
    IDs: list, contains pubmed IDs for papers associated with keyword search term
    abstracts: list, contains abstract text fetched from pubmed
    titles: list, contains title text fetched from pubmed
    global_bow: list, bag of words comprising of mathematical set of words from all abstracts
    tokens_data: list, contains tokenized abstracts
    encodings: nmpy array, contains abstracts in numerical form encoded using bag of words representation
    model: kmeans model of class MyKMeans
    word_clouds: list, contains word clouds of most frequent terms of each cluster
    most_frequent: list, contains most frequent words for each cluster
    
    Methods
    -------
    """
    
    def __init__(self):
        
        """
        constructor
        """
 
        self.stop_words = stopwords.words('english')
    
    def get(self, query, limit):
        
        """
        carries out api call using metapub
        
        Paramaters
        ----------
        
        query : string, keyword search term
        limit : string, number of abstracts to fetch
        """
 
        fetch = PubMedFetcher()
        
        #call API to look for IDs associated with keyword search term
        self.IDs = fetch.pmids_for_query(query, retmax = limit)
        
        self.abstracts = []
        self.titles = []
        
        #loop through IDs and try to fetch associated abstracts
        for c, i_d in enumerate(self.IDs):
            
            print(f'fetching {c}')
            try:
                article = fetch.article_by_pmid(i_d)

            except:
                print(f'id {i_d} doesnt exist')
                continue
            if article.abstract is not None:
                
                #add abstracts and titles to lists 
                self.abstracts.append(article.abstract)
                self.titles.append(article.title)
            else:
                #if cant fetch abstract then just skip
                continue
        
    def count_tokens(self):
        
        """
        method for counting tokens in each abstract to create global bag of words
        """

        global_bow = {}
        for abstract in self.tokens_data:
            for token in abstract:
                if token in list(global_bow.keys()):
                    global_bow[token] +=1
                else: 
                    global_bow[token] = 1
        self.global_bow = global_bow

    
    def __encode(self, tokenized):
        
        """
        method for encoding abstracts using bag of word representation
        
        Parameters
        ----------
        tokenized: list, contains tokenized words for a given abstract
        
        Returns
        -------
        feature: numpy array, bag of words encoded abstract 
        """
        
        feature = np.array([])
        #loop through each token and associated corpus frequency
        for key, value in self.global_bow.items():
            
            #check if token in abstract
            if key in tokenized:
                #if token in abstract encode with occurence
                feature = np.append(feature, value)
            else:
                #if token not in abstract, encode with 0
                feature = np.append(feature, 0)

        return(feature)

    def process_data(self):
        
        """
        Method for processing string data, 
        converts strings to lowercase, 
        removes stop words and checks that they are alpha characters
        """
        self.abstracts = [c for c in self.abstracts if c != None]
        
        tokens_data = []
        for abstract in self.abstracts:
            tokens = word_tokenize(abstract)
            tokens = [c.lower() for c in tokens if c not in self.stop_words and c.isalpha()]
            tokens_data.append(tokens)
        
        self.tokens_data = tokens_data
        
    def encode_data(self):
        
        """
        methid that encodes abstracts by calling __encode() methode
        """
        self.count_tokens()
        self.encodings = []
        for bow in self.tokens_data:
            self.encodings.append(self.__encode(bow))
        self.encodings = np.vstack(self.encodings)


   
    def cluster_data(self, number_clusters):
        
        """
        clusters data
        
        Paramaters
        ----------
        number_clusters: int, number of clusters to derive
        
        """
        
        clusters = list(range(number_clusters))
        
        self.model = MyKMeans(number_clusters, 10000)

        self.model.kmeans(self.encodings)
        

        
        
    def generate_word_clouds(self):
        
        """
        generates word clouds using most frequent terms in each cluster
        """
        self.word_clouds = []
        
        for i in self.most_frequent:
            wordcloud = WordCloud()
            self.word_clouds.append(wordcloud.generate(' '.join(i)))
            


    def analyse_clusters(self):
        
        """
        Checks for most common terms in each cluster
        """
        
        self.most_frequent = []
     
        
        for label in set(self.model.labels):
            
        
            data = [self.tokens_data[i] for i in range(len(self.tokens_data)) if self.model.labels[i] == label]

            all_words_for_label = []
            for observation in data:

                all_words_for_label.extend(observation)


            mf = self.get_frequent_words(all_words_for_label, 10)
            
            self.most_frequent.append(mf)
    
    def get_frequent_words(self, List, top_n): 
        
        """
        Method for checking for most frequent words 
        
        Parameters
        ----------
        List: list, list of words to count
        top_n: int, defines how many in top_n of most common terms to find
        """
        
        occurence_count = Counter(List) 
        ans = occurence_count.most_common(top_n)
        ans = [c[0] for c in ans]

        return(ans)
  

            
            
            

            
            
        
        
        


            


        