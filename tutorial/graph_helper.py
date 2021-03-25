import requests

graph_url = 'https://graph.microsoft.com/v1.0'


def get_user(token):
    # Send GET to /me
    user = requests.get(
        '{0}/me'.format(graph_url),
        headers={
            'Authorization': f'Bearer {token}'
            },
        params={
            '$select': 'displayName,mail,mailboxSettings,userPrincipalName'
            })

    return user.json()


def get_mailbox_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
        }
    # Send GET to /me/messages
    mailbox = requests.get(f'{graph_url}/me/messages', headers=headers)

    return mailbox.json()


def get_inbox_mailfolder_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
        }
    # Send GET to /me/mailFolders/inbox/messages
    mailfolder_inbox = requests.get(f'{graph_url}/me/mailFolders/inbox/messages', headers=headers)

    return mailfolder_inbox.json()


def get_outbox_mailfolder_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
        }
    # Send GET to /me/mailFolders/outbox/messages
    mailfolder_outbox = requests.get(f'{graph_url}/me/mailFolders/sentitems/messages', headers=headers)

    return mailfolder_outbox.json()


def get_drafts_mailfolder_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
        }
    # Send GET to /me/mailFolders/drafts/messages
    mailfolder_drafts = requests.get(f'{graph_url}/me/mailFolders/drafts/messages', headers=headers)

    return mailfolder_drafts.json()
