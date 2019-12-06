## Document Clustering
As my first project in data mining and clustering, clustering Etheruem tokens was interesting for me, it gave me more insight on how a simple clustering algorithm would work and how different methods can be used in order to cluster them and visualize them. 

in the following, I will explain the methods used and my insight on this clustering.

## My insight
the goal for this project is to find the similarity of different platforms of Ethereum Token based on their whitepapers. 
To do so, we should use an unsupervised learning method. The reason why I am mentioning unsupervised is because our data sets do not have labels.
This makes this procedure an unsupervised learning process. 
The first method I could think of was clustering the Documents based on their words frequency. 
we break the documents into text files, and the text files into word, separately from each document, and find the papers which have the similar frequency of words. 

In this manner we could have multiple clusters of papers, containing similar word frequencies.

## tools used
To cluster these papers, I preferred to use _**GoogleColab**_ as my platform. It was really convenient and easy to work and manage the workplace, and it has already satisfied the requirements. 

in addition, I have added the `requirements.txt` on this repository which includes all the libraries used in order to deploy such project. 

## The sequence of jobs
1. Read all the documents and store them into lists.
2. Tokenizing the texts
3. Extracting features
4. Clustering 
5. Visualization

### Read all the documents
the titles of these documents are stored in a list and based on their titles, their texts would be appended to a list.
`SnowballStemmer` was in order to break the words into their root.
### Tokenizing the texts
here we define 2 functions `tokenize_and_stem` and `tokenize_only`. The first one breaks the text into words and then filters any token (list members) that does not contain letter and then stem them. This is done in order to prevent symbols such as ", . ! ? ..." to be included. 
The next function is just trying to tokenize the text only and not stemming them. 
### Extracting features
having the `tokenize_and_stem` and `tokenize_only` we create a pandas Dataframe with `tokenize_and_stem` as its index and `tokenize_only` as its column.
Then we use the TD-idf. TD-idf is a numerical static that is intended to reflect how important a word is to a document in a collection. 

To create the Tf-idf matrix we first count the words occurrence by document. This would be transformed into a document-term matrix.

to apply the TF-idf weighting we have to keep in mind that, the words occurring frequently in a single document but not in all of the documents will get a higher weight. This happens because the feature is unique.

### Clustering
In order to cluster the documents I chose the K-means algorithm. we can choose how many clusters do we want in the k-means method. In my case I chose 10 clusters in order to cluster similar documents into one of these 10 clusters.
Initially k number of so called centroids are chosen.

In this method the goal is to Cluster *n* observations into *k* clusters such that each observation belongs to the cluster with nearest mean.

The mean for each of the documents is calculated and then each is assigned to a cluster.

We can then group them by their *title*, or their *index*  and other features. 

### Visualization
There are many different methods in order to visualize the results. In this case I chose the *Dot plout* diagram.

## Results
As my result, I managed to Cluster 94 whitepapers into 10 clusters(it can be less or more depending on how precise you want your clusters to be).
The result is added to the repository. 

## For The Future
As we know, some platforms for sharing whitepapers and documents add tags to each document. 
These tags can be used in order to train our supervised learning models to detect the similarity of papers and documents for the future. 

With more data available our accuracy will rise and makes this prediction more accurate and precise. 