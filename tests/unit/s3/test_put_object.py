#!/usr/bin/env python
# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import os
import re
import copy

from tests.unit import BaseAWSCommandParamsTest
import six

import awscli.clidriver

# file is gone in python3, so instead IOBase must be used.
# Given this test module is the only place that cares about
# this type check, we do the check directly in this test module.
try:
    file_type = file
except NameError:
    import io
    file_type = io.IOBase


class TestGetObject(BaseAWSCommandParamsTest):

    prefix = 's3api put-object'

    def setUp(self):
        super(TestGetObject, self).setUp()
        self.file_path = os.path.join(os.path.dirname(__file__),
                                      'test_put_object_data')

    def test_simple(self):
        cmdline = self.prefix
        cmdline += ' --bucket mybucket'
        cmdline += ' --key mykey'
        cmdline += ' --body %s' % self.file_path
        result = {'uri_params': {'Bucket': 'mybucket',
                                 'Key': 'mykey'},
                  'headers': {}}
        self.assert_params_for_cmd(cmdline, result, ignore_params=['payload'])
        self.assertIsInstance(self.last_params['payload'].getvalue(), file_type)

    def test_headers(self):
        cmdline = self.prefix
        cmdline += ' --bucket mybucket'
        cmdline += ' --key mykey'
        cmdline += ' --body %s' % self.file_path
        cmdline += ' --acl public-read'
        cmdline += ' --content-encoding x-gzip'
        cmdline += ' --content-type text/plain'
        result = {'uri_params': {'Bucket': 'mybucket', 'Key': 'mykey'},
                  'headers': {'x-amz-acl': 'public-read',
                              'Content-Encoding': 'x-gzip',
                              'Content-Type': 'text/plain'}}
        self.assert_params_for_cmd(cmdline, result, ignore_params=['payload'])
        payload = self.last_params['payload'].getvalue()
        self.assertEqual(payload.name, self.file_path)


if __name__ == "__main__":
    unittest.main()
