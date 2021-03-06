from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from tutorial.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import *
# Create your views here.
from tutorial.helper import initialize_context, process_inbox_data, process_outbox_data


def home(request):
    context = initialize_context(request)

    return render(request, 'tutorial/home.html', context)


def sign_in(request):
    # Get the sign-in flow
    flow = get_sign_in_flow()
    # Save the expected flow so we can use it in the callback
    try:
        request.session['auth_flow'] = flow
        request.session.modified = True
    except Exception as e:
        print(e)
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(flow['auth_uri'])


def callback(request):
    # Make the token request
    result = get_token_from_code(request)

    # Get the user's profile
    user = get_user(result['access_token'])

    # Store user
    store_user(request, user)
    return HttpResponseRedirect(reverse('home'))


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))


def mailbox(request):
    context = initialize_context(request)
    email = context['user']['email']

    token = get_token(request)

    mailbox = get_mailbox_data(token)

    if mailbox:
        messages = [mail for mail in mailbox['value'] if not mail['isDraft']]
        inbox = process_inbox_data(email, messages)
        outbox = process_outbox_data(email, messages)
        draft = list()
        [draft.extend(mail['toRecipients']) for mail in mailbox['value'] if mail['isDraft']]
        drafts = {mail['emailAddress']['address'] for mail in draft}

        context['inbox'] = inbox
        context['outbox'] = outbox
        context['draft'] = drafts

    return render(request, 'tutorial/mailbox.html', context)


def inbox(request):
    context = initialize_context(request)
    email = context['user']['email']
    token = get_token(request)
    data = get_inbox_mailfolder_data(token)
    inbox = list()

    if data:
        for item in data['value']:
            temp_dict = {}
            temp_dict = {'sender': item['sender']['emailAddress']['address'], 'recipients': [m['emailAddress']['address'] for m in item['toRecipients']],
                         'subject': item['subject'], 'body': item['bodyPreview'], 'created': item['createdDateTime']}
            inbox.append(temp_dict)

    context['inbox'] = inbox

    return render(request, 'tutorial/inbox.html', context)


def outbox(request):
    context = initialize_context(request)
    email = context['user']['email']
    token = get_token(request)
    data = get_outbox_mailfolder_data(token)
    outbox = list()

    if data:
        for item in data['value']:
            temp_dict = {}
            temp_dict = {'sender': item['sender']['emailAddress']['address'], 'recipients': [m['emailAddress']['address'] for m in item['toRecipients']],
                         'subject': item['subject'], 'body': item['bodyPreview'], 'created': item['createdDateTime']}
            outbox.append(temp_dict)

    context['outbox'] = outbox

    return render(request, 'tutorial/outbox.html', context)


def drafts(request):
    context = initialize_context(request)
    email = context['user']['email']
    token = get_token(request)
    data = get_drafts_mailfolder_data(token)
    drafts = list()

    if data:
        for item in data['value']:
            temp_dict = {}
            temp_dict = {'sender': email, 'recipients': [m['emailAddress']['address'] for m in item['toRecipients']],
                         'subject': item['subject'], 'body': item['bodyPreview'], 'created': item['createdDateTime']}
            drafts.append(temp_dict)

    context['drafts'] = drafts

    return render(request, 'tutorial/drafts.html', context)
