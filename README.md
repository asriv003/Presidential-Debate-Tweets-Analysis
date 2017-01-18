# Data Mining Fall2016
Data Mining Project Fall 2016 for CS235

Full Report in **_final\_report.pdf_**

Poster in **_poster.pdf_**

##Pacakages Installation
Make sure you install all the requirements form **requirements.txt**
using pip just run:
**_pip install -r requirements.txt_**

After installation create a file called new.py and add below line:

**_import nltk_**

**_nltk.download()_**

save it and run it -- **_python new.py_**

It will take few minutes to install **ntlk** packages

##Files Description
Following are the files and their function

1. **stream.py** --> uses twitter streaming API to get live tweets 
    
    **_python stream.py > data_live.json_**

	Stores tweets in data_live.json

2. **parse_data.py** --> parses raw data and select necessary attributes

    **_python parse_data.py_**

	Stores parsed data in parsed_data.json

3. **sentiment_module.py** and **sentiment_trained.py** :

	**sentiment_module.py** --> trains the classifiers using positive.txt and negative.txt. It can also save the trained classifier so that we don't have to train it again and again. For time being that code is commented out.
	It also has a custom classifier which uses those trained classifier and finds the sentiment of text with confidence value.

	**sentiment_trained.py** --> same as sentiment_module.py but uses saved classifier.
	So this will not work if classifier are not already saved.

4. **sentiment_eval.py** :
	
	Uses sentiment_module or sentiment_trained to compute sentiments of all the tweets.
    
    **_python sentiment_eval.py_**

	Output is stored in sentiment_output.json

5. **count_sentiment.py** :
	
	Just calculates the count of positive and negative tweets for each candidate.
    
    **_python count_sentiment.py_**
	Just prints out the results

6. **JSON** and **text files** :
    
    **data_live.json** --> Contains sample of raw tweets collected during debate
    **parsed_data.json** --> Contains parsed information of raw tweets
    **sentiment_output.json** --> Add sentiment value and confidence value to the parsed tweets
    **positive.txt** --> Contains positive reviews for training
    **negative.txt** --> Contains negative reviews for training