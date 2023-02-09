# -*- coding: utf-8 -*-
"""
Created on 3/19/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


error_logger = setup_logger('error_log', 'error_log.log')
info_logger = setup_logger('info_log', 'info_log.log')
