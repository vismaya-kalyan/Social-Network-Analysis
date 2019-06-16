"""
Cluster data.
"""
import json
# Imports you'll need.
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import itertools 
import networkx as nx
from networkx.algorithms import community
import re
import pandas as pd

def create(name):

    summary = open('cluster.txt', 'a')  # Create file to write summary
    summary.write(name+'\n\n')
    tweets = json.loads(open('%s_tweets.json'%name).read())
    graph = nx.Graph()

    # Creating social links
    for tweet in tweets:
        if '@' in tweet['text']:
            mentions = re.findall(r'[@]\w+', tweet['text'])
            for mention in mentions:
                graph.add_node(tweet['user']['screen_name'])
                graph.add_node(mention[1:])
                graph.add_edge(tweet['user']['screen_name'], mention[1:])
    print('graph has %d nodes and %d edges' %(graph.order(), graph.number_of_edges()))
    summary.write('graph has %d nodes and %d edges' %(graph.order(), graph.number_of_edges()))
    # Clustering
    cluster = community.girvan_newman(graph)
    
    for communities in itertools.islice(cluster, 1):
        commuity_cluster = tuple(sorted(c) for c in communities)

   
    # Count number of unique users and write number of users collected to file
    users = [tweet['user']['screen_name'] for tweet in tweets]
    users = set(users)
    summary.write('\n\nNumber of users collected: ' + str(len(users)) + '\n\n')

    # write number of messages collected to file
    summary.write('Number of messages collected: ' + str(len(tweets)) + '\n\n')

    
    # Write number of communities detected
    communities_detected = len(commuity_cluster)
    user_count = 0
    for x in commuity_cluster:
        user_count += len(x)
    summary.write('Number of communities detected: ' + str(communities_detected) + '\n\n')

    # Write number of users in each community
    summary.write('Average number of users in each community: ' + str(user_count/communities_detected) + '\n\n')
    
    summary.close()

def main():
    screen_names = ["jordanbpeterson", "joerogan"]
    for i in screen_names:
        create(i)
    print("Clustering Done.\nOpen cluster.txt for more information.")

if __name__ == "__main__":
   main()