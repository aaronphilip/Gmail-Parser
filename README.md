# Gmail-Parser

This tool allows you to eaisly pull down your gmail messages, scrape them for plain text, and save them in a csv. I personally use it to make email datasets for training machine learning models.

## Setup

1. install the dependencies found in `requirements.txt`
2. click on **enable the gmail api** [here](https://developers.google.com/gmail/api/quickstart/python) to download you credentials.json 
3. place credentials.json at the root
4.  when you first run the parser, you will be asked to authenticate your account, which will also create a pickle file with your account details

## Running the Parser

`python gmail_parser.py` will by default pull down all of your emails and save it in `emails.csv`

### Options

`-n n_msgs` pulls down the number of messages specified by `n_msgs`

`-o path` saves the emails to the file specified by `path`

## CSV Format

Each line of the csv is formatted name,address,subject,body

The body is lowercase and space delimitted. All non-ascii characters are removed.
