# File Parsing
This section focuses on the data analysis of the Common Crawl Corpus

## Functional Scripts
* This directory contains the scripts to be used with extracting onions and counting the sites.
* To use, simply copy these scripts to a directory that contains your Common Crawl files.

## onion_data
* This directory contains all data related to onions
    * final_counts.csv is a CSV that has all the onions and how often they were found on the clearweb
    * onions.csv is a CSV file that contains __ONLY__ the onions found on the clearweb.
    * onions_fixed.txt was a test file that failed to meet the expectations of Mr. King

## site_data
* This directory contains all data related to the sites onions were found on
    * initialized_site_data.csv is a CSV that has each site and a list of onions that were on the site
    * initial_site_counts.csv is a CSV file that took each site and counted the number of __UNIQUE__ onions that were on the site. (i.e. if blah.onion was found 4 times on blah.com, it only counts as 1. But if it was found on a different site, it counted for both sites (blah.com has 1 and blah2.com has 1))
    * final_sites_counts.CSV is a CSV file that has the sites and their counts in descending order

## test_files
* This directory has the files I used to test the scripts

## darkweb.pptx
* Mid-point presentation