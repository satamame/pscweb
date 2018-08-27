from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import Http404
from .models import Production, Member, Team

import httplib2
import os
import unicodedata

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class ProductionIndexView(generic.ListView):
    model = Production
    paginate_by = 10


class MemberListView(generic.ListView):
    def get_queryset(self):
        return Member.objects.filter(prod_id=self.kwargs['prod_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['production'] = Production.objects.get(pk=self.kwargs['prod_id'])
        return context


class TeamListView(generic.ListView):
    def get_queryset(self):
        return Team.objects.filter(prod_id=self.kwargs['prod_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['production'] = Production.objects.get(pk=self.kwargs['prod_id'])
        return context


def schedule(request, prod_id):
    prod = get_object_or_404(Production, pk=prod_id)
    values = get_sheet_values(prod.gs_id, 'Sheet1')

    # Padding
    maxlen = max(map(len, values))
    values = [x + ['']*(maxlen-len(x)) for x in values]

    # Transpose
    values = list(zip(*values))
    
    # Member names
    names = [s[0] for s in values[0][4:]]

    table_data = []
    for row in values[1:]:
        data = [
            unicodedata.normalize('NFKC', row[0] + '\n' + row[1]),
            unicodedata.normalize('NFKC', row[2] + '\n' + row[3])
        ]
        for s in row[4:]:
            if s.strip() == '':
                data.append(' ')
            elif s in ['○', '◯']:
                data.append('○')
            elif s == '×':
                data.append('×')
            elif s[0] in ['～', '-']:
                data.append('▼')
            elif s[-1] in ['～', '-']:
                data.append('▲')
            else:
                data.append('*')
        table_data.append(data)

    context = {
        'production': prod,
        'names': names,
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


def member(request, prod_id):
    prod = get_object_or_404(Production, pk=prod_id)
    
    idx = request.GET.get('idx')
    id = request.GET.get('id')
    if not idx and not id:
        raise Http404

    values = get_sheet_values(prod.gs_id, 'Sheet1')

    # Padding
    maxlen = max(map(len, values))
    values = [x + ['']*(maxlen-len(x)) for x in values]

    # TODO
    # Transpose する前にフィルタする事で、処理が簡潔になるはず。

    # Transpose
    values = list(zip(*values))

    # Get the person's index in sheet
    if not idx:
        try:
            member = Member.objects.get(pk=int(id))
            ps_idx = values[0].index(member.name) - 4
        except ValueError:
            raise Http404
    else:
        ps_idx = int(idx)

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
    return render(request, 'gs_schdl/member.html', context)


def team(request, prod_id, team_id):
    prod = get_object_or_404(Production, pk=prod_id)
    team = get_object_or_404(Team, pk=team_id)

    values = get_sheet_values(prod.gs_id, 'Sheet1')

    # Filter sheet by members
    mb_names = [m.name for m in team.members.all()]
    values = values[:4] + [row for row in values[4:] if row[0] in mb_names]

    # Sort Members with the order in the sheet
    members = []
    for row in values[4:]:
        member = [m for m in team.members.all() if m.name == row[0]]
        member = member[0]
        member.name = member.name[:2]
        members.append(member)

    # Padding
    maxlen = max(map(len, values))
    values = [x + ['']*(maxlen-len(x)) for x in values]

    # Transpose
    values = list(zip(*values))

    # Normalize data part
    table_data = [
        [unicodedata.normalize('NFKC', row[0] + '\n' + row[1])]
        + [unicodedata.normalize('NFKC', d) for d in row[4:]]
        for row in values[1:]
    ]

    context = {
        'production': prod,
        'team': team,
        'members': members,
        'table_data': table_data,
    }
    return render(request, 'gs_schdl/team.html', context)


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
