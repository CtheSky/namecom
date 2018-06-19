# encoding=utf-8

import os
import namecom

test_env_auth = namecom.Auth('cthesky-test', '96414285232f77557662ba9be585ba926f04dc9b', use_test_env=True)
TEST_ALL = os.environ.get('TEST_ALL')