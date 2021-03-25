import pymongo


def get_mongo_connection(db_name=None):
    client = pymongo.MongoClient('localhost', 27017)
    if db_name is not None:
        db = client[db_name]
        return db, client
    return client


def get_db_name(email):
    assert email, "Email required"
    # email = email if isinstance(email, str) else email.username
    return email.replace('@', '').replace('.', '')


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error is not None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def process_inbox_data(email, messages):
    inbox = list()
    for msg in messages:
        if email not in (msg['sender']['emailAddress']['address'], msg['sender']['emailAddress']['address']):
            temp_dict = {}
            temp_dict = {'sender': msg['sender']['emailAddress']['address'], 'recipients': email,
                         'subject': msg['subject'], 'body': msg['bodyPreview'], 'created': msg['createdDateTime']}
            inbox.append(temp_dict)
    return inbox


def process_outbox_data(email, messages):
    outbox = list()
    for msg in messages:
        if email in (msg['sender']['emailAddress']['address'], msg['sender']['emailAddress']['address']):
            temp_dict = {}
            temp_dict = {'sender': email, 'recipients': [m['emailAddress']['address'] for m in msg['toRecipients']],
                         'subject': msg['subject'], 'body': msg['bodyPreview'], 'created': msg['createdDateTime']}
            outbox.append(temp_dict)
    return outbox
