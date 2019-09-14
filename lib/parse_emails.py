from lib.gmail_api import get_message_ids, get_mime_msg
from email.header import decode_header
from email.utils import parseaddr
from bs4 import BeautifulSoup
from warnings import warn
import re

def get_email_info(mime_msg):
    '''Get information about the email sender
    
    Args: 
        mime_msg (Email object): email object containing MIME info for message
        
    Returns:
        sender_set (EXtractResult Object): parsed wevsite of sinder using tldextract library
        sender_name (str): The name associated with sender email
    '''
    
    sender_addr = None
    sender_name = None
    subject = None
    
    from_header = decode_header(mime_msg['from'])
    sender_str = from_header[0][0]
    
    subject = mime_msg['Subject']
    
    if len(from_header) == 2:
        sender_str += from_header[1][0]
        
    if type(sender_str) is not str:
        sender_str = sender_str.decode('utf-8')
        
    sender = parseaddr(sender_str)
    sender_name = sender[0]
    
    sender_addr = sender[1]
            
    return sender_name, sender_addr, subject

def parse_body(mime_msg):
    '''Convert email body to plain text
    
    Args:
        mime_msg (Email Object): email object containing MIME info for message
        
    Raises:
        Warning if body content is not plain text or HTML
        Warning if Beautiful Soup fails to parse the HTML
        
    Returns:
        txt (string): the txt parsed from the email body
    '''
    
    txt = mime_msg.get_payload(decode=True)
    
    try:
        #decode bytes according to its charset
        encoding = mime_msg.get_content_charset()
        
        if encoding is None:
            encoding = 'utf-8'
            
        txt = txt.decode(encoding)
    except:
        #warn if content is not plain text or html (image, pdf, etc.)
        warn('Skipping' + mime_msg.get_content_type(), stacklevel=2)
        return 1, -1
    
    if mime_msg.get_content_type() == 'text/html':
        soup = BeautifulSoup(txt, 'html5lib')
        try:
            #remove unnecessary tags
            for elem in soup(['style', 'script', 'meta', '[document]', 'head', 'title']):
                elem.decompose()
                    
            txt = soup.get_text(separator=u' ')
            
        except:
            warn('Could not parse email')
            return 2, -1
    
    #remove links
    txt = re.sub(r'<?http\S+', ' ', txt)
    
    #remove non ascii characters
    txt = re.sub(r'[^\x00-\x7F]+','', txt)
    
    #remove new lines, whitespace and seperate each word wih a space
    txt = ' '.join([line.strip() for line in txt.split() if line.strip() != '']).lower()
    
    return txt

def parse_emails(service, label='INBOX', n_msgs=None):
    '''Get the first n_msgs emails
    
    Args:
        service (gmail service): a gmail service associated with a user
        label (str, optional): label to get emails from; full list here
                                https://developers.googe.com/gmail/api/guides/labels
                                Defaults to 'INBOX'
        n_msgs (int): the number of emails to retrieve
        
    Returns:
        emails (list): each tuple in the list contains an email oject and the associated parsed
                       text
    '''
    
    messages = get_message_ids(service, label, n_msgs)

    if n_msgs is None:
        n_msgs = len(messages)
    else:
        n_msgs = min(len(messages), n_msgs)
    
    emails = []
    
    for i in range(n_msgs):
        
        message = messages[i]
        mime_msg = get_mime_msg(service, message)
        txt = ""
        messageMainType = mime_msg.get_content_maintype()
        
        #some emails have many nested parts
        if messageMainType == 'multipart':
            
            #create a stack of all the email parts
            s = []
            for part in mime_msg.get_payload():
                s.append(part)
                
            #parse each part
            while len(s):
               
                part = s.pop()
                
                #some parts are made of more parts
                if (part.get_content_maintype() == 'multipart'):
                    for p in part.get_payload():
                        s.append(p)
                    continue
                    
                part_txt = parse_body(part)
                
                #content was not plain text of HTML
                if type(part_txt) is not str:
                    continue
                
                #concat all of the email parts
                txt += part_txt + ' '
                
        elif messageMainType == 'text':
            txt = parse_body(mime_msg)

            #content was not plain text or HTML
            if type(txt) is not str:
                continue
        
        emails.append((mime_msg, txt))

    return emails