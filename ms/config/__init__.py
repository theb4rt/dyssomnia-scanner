# -*- coding: utf-8 -*-
"""
Created on 08/02/23
@author: b4rt
@mail: root.b4rt@gmail.com
"""

from dotenv import load_dotenv
from ms import app
from ms.config.app_config import app_config
from ms.config.db_config import db_config

load_dotenv()

app.config.update(**app_config)
app.config.update(**db_config)
