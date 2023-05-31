# -*- coding: utf-8 -*-
"""
Created on 3/19/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""

import os
import logging.config

# Get the absolute path to the logging.conf file
config_file = os.path.join(os.getcwd(), 'ms/utils/logging.conf')

# Load the logging configuration from the file
logging.config.fileConfig(config_file)

# Continue with logging statements after loading the config
# logger.info("After loading logging configuration")

error_logger = logging.getLogger('error_log')
info_logger = logging.getLogger('info_log')
nikto_logger = logging.getLogger('nikto_log')

