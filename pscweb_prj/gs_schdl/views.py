from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import Http404
from .models import Production

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class ProductionIndexView(generic.ListView):
    model = Production
    paginate_by = 10


def schedule(request, prod_id):
    prod = get_object_or_404(Production, pk=prod_id)
    values = get_sheet_values(prod.gs_id, 'Sheet1')
    
    """
    if not values:
        data = 'No data found.'
    else:
        data = 'Name, Major:'
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            data += '%s, %s<br>' % (row[0], row[4])
    """

    # Padding
    maxlen = max(map(len, values))
    values = [x + ['']*(maxlen-len(x)) for x in values]

    # Transpose
    values = list(zip(*values))
    
    table_data = []
    for row in values[1:]:
        attend = row[4:].count('○') + row[4:].count('◯')
        absent = row[4:].count('×')
        other = len(row) - 4 - attend - absent
        data = [
            row[0] + '\n' + row[1],
            row[2] + '\n' + row[3],
            "◯ : {0}人\n× : {1}人\n他 : {2}人".format(attend, absent, other)
        ]
        table_data.append(data)

    context = {
        'production': prod,
        'table_data': table_data,
    }
    return render(request, 'gs_schdl/schedule.html', context)


def rehearsal(request, prod_id, rh_idx):
    prod = get_object_or_404(Production, pk=prod_id)
    values = get_sheet_values(prod.gs_id, 'Sheet1')

    # Padding
    maxlen = max(map(len, values))
    values = [x + ['']*(maxlen-len(x)) for x in values]

    # Extract the rehearsal's data
    try:
        table_data = [(row[0], row[1 + rh_idx]) for row in values[4:]]
    except IndexError:
        raise Http404

    context = {
        'production': prod,
        'datetime': values[0][1 + rh_idx] + ' ' + values[1][1 + rh_idx],
        'place': values[2][1 + rh_idx] + ' ' + values[3][1 + rh_idx],
        'table_data': table_data,
    }
    return render(request, 'gs_schdl/rehearsal.html', context)


def person(request, prod_id, ps_idx):
    prod = get_object_or_404(Production, pk=prod_id)
    values = get_sheet_values(prod.gs_id, 'Sheet1')

    # Padding
    maxlen = max(map(len, values))
    values = [x + ['']*(maxlen-len(x)) for x in values]

    # Transpose
    values = list(zip(*values))
    
    # Extract the person's data
    try:
        table_data = [
            (row[0] + '\n' + row[1], row[4 + ps_idx])
            for row in values[1:]
        ]
    except IndexError:
        raise Http404

    context = {
        'production': prod,
        'name': values[0][4 + ps_idx],
        'table_data': table_data,
    }
    return render(request, 'gs_schdl/person.html', context)


def get_sheet_values(sheet_id, range_name):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    return values


def get_credentials():
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
    """

    flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credential_dir = os.path.join(current_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
