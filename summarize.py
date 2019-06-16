"""
Summarize data.
"""
import json 

def main():
    summary = open('summary.txt', 'a')  # Create file to write summary
    summary.write('Summary\n\n\n')

    summary.write('Collection\n\n')
    # Read collect.txt
    collect = open('collect.txt', 'r')      # open file in read mode
    collect_data = collect.read()      # copy to a string
    collect.close()     # close the file
    summary.write(collect_data)          # print the data

    summary.write('\n\n\nClustering\n\n')
    # Read cluster.txt
    cluster = open('cluster.txt', 'r')
    cluster_data = cluster.read()
    cluster.close()
    summary.write(cluster_data)

    summary.write('\n\nClassification\n\n')
    # Read classify.txt
    classify = open('classify.txt', 'r')
    classify_data = classify.read()
    classify.close()
    summary.write(classify_data)


    summary.close()
    print('\n Summary saved in summary.txt\n')

if __name__ == "__main__":
    main()