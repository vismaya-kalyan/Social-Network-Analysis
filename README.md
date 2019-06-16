# Social Network Analysis

The main goals of this project are to:
1. **Collect** raw data from some online social networking site (Twitter)
2. Perform **community detection** to cluster users into communities.
3. Perform **supervised classification** to annotate messages and/or users according to some criterion.
4. Analyze the results and **summarize** your conclusions.

To Run the project, You will run the following commands:
```
python collect.py
python cluster.py
python classify.py
python summarize.py
```

## Background

Jordanbpeterson and Joerogan are two on youtuber whose content is very different.
Jordanbpeterson  clinical psychologist and a professor of psychology at the University of Toronto. 
Jerogan is an American stand-up comedian, mixed martial arts (MMA) color commentator, podcast host, businessman and former television host and actor. 

As these 2 people are in 2 different fields it would be easy to pick up on words that they use hence choose them for my analysis.

## Here is what each script does:

###### collect.py : 
Running this script should create files containing the data that you need for the subsequent phases of analysis. Here we collect 2 types of data

1. First we collect all the tweets of the user Jordanbpeterson and Joerogan using GET Statuses/user_timeline. This method can only return up to 3,200  of a user's most recent Tweets. Native retweets of other statuses by the user is included in this total, regardless of whether include_rts is set to false when requesting this resource. For our analysis we have set include_rts to false as those tweets don't belong to the user of interest.

2. Second we collect all tweets which include Jordanbpeterson and Joerogan using Standard search API which returns  a collection of relevant Tweets matching a specified query. A count of 100 of for each is collected.

###### cluster.py : 
This script read the data collected in the previous step and use a community detection algorithm to cluster users into communities. 
The data collected in which all tweets of Jordanbpeterson and Joerogan is used for this step. Here I have used Girvan Newman algorithm from Networkx for clustering. 
From the tweets I have collected I get the user of all those who have mentioned the Person of interest. Using these users we form clusters with Girvan Newman algorithm.

###### classify.py : 

This uses the user_timeline and  preprocesses the data. Example lowers the characters, removes punctuation, escape characters, remove urls, emoji, smiley, mention and quotes. I use TfidfVectorizer to vectorize and to detect similar tweets ngrams_range(2,5) is used. Using the preprocessed data I train it on a logistic regression algorithm. Cross Validation is used to avoid over specialization. The data is also shuffled before we train it. Accuracy of train and test is reported.

###### summarize.py : 

This should read the output of the previous methods to write a textfile called summary.txt
containing the following entries:
  - Number of users collected:
  - Number of messages collected:
  - Number of communities discovered:
  - Average number of users per community:
  - Number of instances per class found:
  - One example from each class:


Non-standard libraries, are included as a list of the library names in a file requirements.txt`. To install use the command `pip install -r requirements.txt`.

######  Note:You may have to use the pre-processor zip file to install preprocessor library.