import requests
import gunicorn

def get_auth_token(secret, client_id, login_url):
    # Returns an Authentication Token from PowerBI API.
    body = {
        'grant_type': 'client_credentials',
        'resource': r'https://analysis.windows.net/powerbi/api',
        'client_id': client_id,
        'client_secret': secret,
        'client_info': 1
    }


    response = requests.post(url=login_url, data=body)
    if response.status_code == 400:
        return "Failed to retrieve token"
    else:
        return response.json().get('access_token')


def get_embed_url(auth_token, group_id, report_id):
    # returns the embed URL of the specified report
    data = {}
    headers = {
        'Authorization': 'Bearer ' + auth_token
    }
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}"
    response = requests.get(url=url, headers=headers, data=data)

    if response.status_code == 400:
        return "Failed to retrieve embed URL"
    else:
        return response.json().get('embedUrl')


def get_embed_token(auth_token, group_id, report_id):
    # Returns the embed token of a given group
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken"
    data = {
        'access_level': 'view'
    }
    headers = {
        'Authorization': 'Bearer ' + auth_token
    }
    response = requests.post(url=url, headers=headers, data=data)

    if response.status_code == 400:
        return "Failed to retrieve embed Token"
    else:
        return response.json().get('token')
