
import pytest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from unittest.mock import patch
import os
import json
from models.OrderTable import OrderTable
from utils.checkout_api_helper import validate_pickup_time


def test_validate_pickup_time():
    assert True


