import copy
import os
import re
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    redirect,
    url_for,
    session,
)
import json
import time
import pandas as pd
import bcrypt
import subprocess
import numpy as np
from dateutil.parser import isoparse
from pprint import pprint

from flask_jwt_extended import JWTManager

from system.print_logger import PrintLogger
from datetime import timedelta, datetime, timezone
from system.mongo_connector import MongoConnector

#from data_processing.import_modules.import_devices_from_csv import import_csv_to_table
from audit.infra_audit.tag_template_assignment_table import (
    return_cfg_audit_config_template_db,
    update_cfg_audit_template_tag_db,
    build_tag_template_db
)

from cognition_frontend.remove_collections import remove_collection_table
from audit.infra_audit.cfg_audit_cfg import CfgAudit
from cognition_frontend.cognition_menu import read_html_file, TEMPLATE_DICT
from cognition_frontend.cognition import (upload_static_devices,
                                          protect_view,
                                          remove_static_devices,
                                          cfg_audit_cfg_var,
return_db_table,
query_finder,
cfg_audit_template,
remove_from_row_cfg_template,
api_login,
prepare_df_for_return,
apply_highlight,
update_infra_scheduler_table_db,
test_credential
                                          )

import urllib3

urllib3.disable_warnings()


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


@app.route("/login", methods=["GET"])
def landing_page():
    return render_template("login.html")

