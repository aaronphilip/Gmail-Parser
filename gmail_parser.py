import sys
import argparse
from lib.utils import get_emails, write_emails

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse emails from a Gmail account')
    
    parser.add_argument('-n', type=int, help='number of emails to parse')
    parser.add_argument('-o', help='path to output csv file')
    
    args = parser.parse_args()
    
    n_msgs = args.n
    path = args.o
    if path is None:
        path = 'emails.csv'
    
    emails = get_emails(n_msgs=n_msgs)
    write_emails(emails, path)