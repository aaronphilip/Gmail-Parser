import csv
from lib.parse_emails import parse_emails, get_email_info
from lib.quickstart import main as get_service

def write_emails(emails, path):
    '''Write parsed emails to csv file
    
    Args:
        emails (list): list of form [(mime_msg, email_txt)]
    '''
    
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['name', 'address', 'subject', 'body'])
        
        for mime_msg, email_txt in emails:

            sender_name, sender_addr, subject = get_email_info(mime_msg)

            writer.writerow([sender_name, sender_addr, subject, email_txt])
            
def get_emails(labels = ['INBOX'], n_msgs=None):
    '''Authorize a gmail account and parse emails
    
    Args:
        labels (string[], optional): a list of labels to get emails from; default is INBOX
        n_msgs (int, optionsl): the number of messages to pull down
    
    '''
    gmail = get_service()
    emails = parse_emails(gmail, labels, n_msgs)
    
    return emails