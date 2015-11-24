# Copyright 2015 Zadara Storage, Inc.
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
from zadarapy.validators import is_valid_volume_id


def get_all_drives(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all drives attached to the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying drives from.  Optional.

    :type: limit: int
    :param limit: The maximum number of drives to return.  Optional.

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
    path = '/api/drives.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_free_drives(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all drives that are available for use (not
    particpating in a RAID group).

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying drives from.  Optional.

    :type: limit: int
    :param limit: The maximum number of drives to return.  Optional.

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
    path = '/api/drives/free.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_drive(session, drive_id, return_type=None):
    """
    Retrieves details for a single drive.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    method = 'GET'
    path = '/api/drives/{0}.json'.format(drive_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def rename_drive(session, drive_id, newname, return_type=None):
    """
    Sets the "display_name" drive parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type newname: str
    :param newname: The new "display_name" to set.  May not contain a single
        quote (') character.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    body_values = {}

    newname = newname.strip()

    if not is_valid_field(newname):
        raise ValueError('{0} is not a valid drive display name.'
                         .format(newname))

    body_values['newname'] = newname

    method = 'POST'
    path = '/api/drives/{0}/rename.json'.format(drive_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def remove_drive(session, drive_id, return_type=None):
    """
    Removes a drive from the VPSA.  Only drives that aren't participating in a
    RAID group may be removed.  A ValueError will be raised if an invalid or
    non-removeable drive ID is passed.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    method = 'POST'
    path = '/api/drives/{0}/remove.json'.format(drive_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def replace_drive(session, drive_id, toname, return_type=None):
    """
    Replaces a drive, identified by drive_id variable with a new unallocated
    drive, identified by toname variable, in a RAID group.  The replacement
    drive must not be currently allocated to a RAID group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive to be replaced.  This is the drive 'name' value
        as returned by get_all_drives.  For example: 'volume-00002a73'.
        Required.

    :type toname: str
    :param toname: The replacement drive.  This is the drive 'display_name'
        value as returned by get_drive_list.  For example, 'drive-000'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    body_values = {}

    toname = toname.strip()

    if not is_valid_field(toname):
        raise ValueError('{0} is not a valid drive display name.'
                         .format(toname))

    body_values['toname'] = toname

    method = 'POST'
    path = '/api/drives/{0}/rename.json'.format(drive_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def shred_drive(session, drive_id, return_type=None):
    """
    Initializes drive shredding for an individual drive.  Drive must not be
    participating in a RAID group.  CAUTION: This procedure will permanently
    destroy data and is irreversiable.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    method = 'POST'
    path = '/api/drives/{0}/shred.json'.format(drive_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def cancel_shred_drive(session, drive_id, return_type=None):
    """
    Cancels a drive shred that is currently in process.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    method = 'POST'
    path = '/api/drives/{0}/cancel_shred.json'.format(drive_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_drive_performance(session, drive_id, interval=1, return_type=None):
    """
    Retrieves metering statistics for the drive for the specified interval.
    Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/drives/{0}/performance.json'.format(drive_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)