# Overview
This is a script to gather all the etymologies and their relevant information from [etymonline](https://www.etymonline.com/).

# Makin it work
This uses Scrapy which is not (s)crappy to crawl the website and grab the word,the part of speech, the actual etymology description and finally the link to the word a source citation is needed.

The Spider Crawls the website and extract these fields via **Xpath**.

The results are saved in a jsonl format for readability that you can check out in the repo (over **52k** entries !) , normally we should have created an item processing pipeline ,but getting exact origins abd dates is very convoluted and varied per entry so the extraction of what we actually need will be done independently of this project which focuses mainly on getting the data.

## To run the spider use this:
`scrapy crawl etym_all -o etymology.jsonl -s JOBDIR=crawls/etym_job`

*and run the exact command again to resume a crawl if needed*

## What is next?
- [ ] Fashion an NLP processing pipeline.
- [ ] Extract the relevant dates and points of origin.
- [ ] Make an API.

*aye im scrappin 'ere*
