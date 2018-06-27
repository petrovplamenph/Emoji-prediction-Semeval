# Emoji-prediction-Semeval
Solution for the ML competition https://competitions.codalab.org/competitions/17344  
The data for the task consist of 500k tweets in English labeled with 20 emojis.
Analyzed 500k tweets labeled with 20 different emojis. Performed spelling correction on the corpus with TextBlob and Enchant.  
Applied 2 different models. The first model is based on Bag of Words. A system of  “one-versus-all” Support Vector Machines were trained   on tf-idf weighted words. The conflicts between classifiers were resolved with a global classifier trained on 20% most informative words,  where the most informative words were selected with chi-square statistics and ID3 decision tree.   
For the second model recurrent neural network architecture was used with input pertained word embeddings from Stanford with the GloVe   algorithm. In order to acquire embeddings for the missing words in the Stanford Corpus, embeddings were learned for all words in the   corpus. Then a Multilayered Perceptron was trained in order to learn transformation of the embeddings from the coordinate system of   trained the corpus to the pre-trained Stanford embeddings. 
