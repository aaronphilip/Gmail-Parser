import base64
from email import message_from_bytes

def get_message_ids(service, labels=["INBOX"], n_msgs=10):
    '''Get message IDs matching the provided label 
    
    Args:
        service (gmail sercive): a gmail service associated with a user
        labels (string[], optional): list of labels to get emails from; full list here
                               https://developers.google.com/gmail/api/guides/labels
                               Defaults to "INBOX"
        n_msgs (int, optional): number of messages to het. Defaults to 10
    
    Returns:
        messages (dict[]): list of dicts containing message IDs and thread IDs of 
                         the form [{'id': 'a_message_id_value', 'threadId': 'a_thread_id'}]
    '''
    
    results = service.users().messages().list(userId='me', labelIds = labels, maxResults=n_msgs).execute()
    messages = results.get('messages', [])

    return messages

def get_mime_msg(service, message):
    '''Get a python email obj from a message id
    Args:
        service (gmail service): a gmail service associated with a user
        message (dict): a dict of the form retrieved from the users().messages().list method
        
    Returns:
        mime_msg (Email Object): email object containing MIME info for message
    '''
    
    msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = message_from_bytes(msg_str)
    
    return mime_msg