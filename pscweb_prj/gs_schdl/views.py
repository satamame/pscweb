from django.shortcuts import render, get_object_or_404
from django.views import generic
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

    values = get_sheet_values(prod.gs_id, 'Sheet1!A1:K')

    """
    if not values:
        data = 'No data found.'
    else:
        data = 'Name, Major:'
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            data += '%s, %s<br>' % (row[0], row[4])
    """

    context = {
        'values': values,
    }
    return render(request, 'gs_schdl/schedule.html', context)


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