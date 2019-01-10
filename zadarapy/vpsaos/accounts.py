# Copyright 2018 Zadara Storage, Inc.
# Originally authored by Jeremy Brown - https://github.com/jwbrown77
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.


import json
from zadarapy.validators import is_valid_field
from zadarapy.validators import is_valid_vpsaos_account_id


def get_all_accounts(session, start=None, limit=None, return_type=None):
    """
    Get details on all VPSAOS accounts.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying accounts from.  Optional.

    :type: limit: int
    :param limit: The maximum number of accounts to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/zios/accounts.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_account(session, account_id, return_type=None):
    """
    Get details of a single account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vpsaos_account_id(account_id):
        raise ValueError('{0} is not a valid VPSAOS account id.'
                         .format(account_id))

    method = 'GET'
    path = '/api/zios/accounts/{0}.json'.format(account_id)

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def create_account(session, account_name, return_type=None):
    """
    Create a VPSAOS account.  An object storage account is a collection of
    containers. Typically an account is associated with a tenant.  Access
    rights can be granted for users per account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_name: str
    :param account_name: A text label assigned to the VPSAOS account name.
        For example, 'accounting' or 'sales'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_field(account_name):
        raise ValueError('{0} is not a valid VPSA Object Store account name.'
                         .format(account_name))

    body_values['name'] = account_name

    method = 'POST'
    path = '/api/zios/accounts.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def delete_account(session, account_id, force='NO', return_type=None):
    """
    Delete a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSAOS to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_vpsaos_account_id(account_id):
        raise ValueError('{0} is not a valid VPSAOS account id.'
                         .format(account_id))

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'DELETE'
    path = '/api/zios/accounts/{0}.json'.format(account_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def cleanup_account(session, account_id, return_type=None):
    """
    Cleanup a VPSAOS account's details.  This will remove billing information
    after an account was deleted.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vpsaos_account_id(account_id):
        raise ValueError('{0} is not a valid VPSAOS account id.'
                         .format(account_id))

    method = 'DELETE'
    path = '/api/zios/accounts/{0}/cleanup.json'.format(account_id)

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def disable_account(session, account_id, return_type=None):
    """
    Disable a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vpsaos_account_id(account_id):
        raise ValueError('{0} is not a valid VPSAOS account id.'
                         .format(account_id))

    method = 'POST'
    path = '/api/zios/accounts/{0}/disable.json'.format(account_id)

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def enable_account(session, account_id, return_type=None):
    """
    Enable a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vpsaos_account_id(account_id):
        raise ValueError('{0} is not a valid VPSAOS account id.'
                         .format(account_id))

    method = 'POST'
    path = '/api/zios/accounts/{0}/enable.json'.format(account_id)

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def get_all_users_in_account(session, account_id, return_type=None):
    """
    Get details for all users in a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vpsaos_account_id(account_id):
        raise ValueError('{0} is not a valid VPSAOS account id.'
                         .format(account_id))

    method = 'GET'
    path = '/api/zios/accounts/{0}/users.json'.format(account_id)

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)
