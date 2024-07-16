# Copyright 2016 Camptocamp SA
# Copyright 2020 Hibou Corp.
# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import re


class S3Uri(object):

    _url_re = re.compile("^s3:///*([^/]*)/?(.*)", re.IGNORECASE | re.UNICODE)

    def __init__(self, uri):
        match = self._url_re.match(uri)
        if not match:
            raise ValueError("%s: is not a valid S3 URI" % (uri,))
        self._bucket, self._item = match.groups()

    def bucket(self):
        return self._bucket

    def item(self):
        return self._item
