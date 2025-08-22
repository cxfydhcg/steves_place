import json
import logging
from models.StoreCloseDateTable import StoreClosedDateTable
from flask import Blueprint, request, jsonify, Response
from models.OrderTable import OrderTable, db
from datetime import datetime, timezone
import os
from zoneinfo import ZoneInfo


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(os.path.join(log_dir, 'close_store_api.log'))
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

routes = Blueprint('close_store_api', __name__)

@routes.route('/add_close_date', methods=['POST'])
def add_close_date():
    try:
        store_auth_sid = request.form.get('store_auth_sid')
        date = request.form.get('date')

        if not store_auth_sid:
            logging.warning(f"Today's orders request missing store_auth_sid from IP: {request.remote_addr}")
            return Response(json.dumps({'error': 'Missing store_auth_sid'}), status=400, mimetype='application/json')
        if store_auth_sid != os.getenv('STORE_AUTH_SID'):
            logging.warning(f"Invalid store authentication attempt from IP: {request.remote_addr}, SID: {store_auth_sid}")
            return Response(json.dumps({'error': 'Unauthorized'}), status=401, mimetype='application/json')

        # Format should be mm/dd/yyyy, and it is in eastern time, convert to utc
        try:
            date = datetime.strptime(date, '%m/%d/%Y').replace(tzinfo=ZoneInfo("America/New_York"))
            # Convert to utc
            date = date.astimezone(timezone.utc)
        except ValueError:
            logging.warning(f"Invalid date format from IP: {request.remote_addr}, date: {date}")
            return Response(json.dumps({'error': 'Invalid date format'}), status=400, mimetype='application/json')
        
        # Date can not be in the past
        if date.date() < datetime.now(timezone.utc).date():
            logging.warning(f"Close date in the past from IP: {request.remote_addr}, date: {date}")
            return Response(json.dumps({'error': 'Date can not be in the past'}), status=400, mimetype='application/json')

        # Create a new StoreClosedDate instance
        new_close_date = StoreClosedDateTable(date=date)
        db.session.add(new_close_date)
        db.session.commit()
        logging.info(f"Close date added successfully from IP: {request.remote_addr}, date: {date}")
        return Response(json.dumps({'message': 'Close date added successfully'}), status=200, mimetype='application/json')
    except ValueError as e:
        logging.warning(f"ValueError: {e} from IP: {request.remote_addr}")
        return Response(json.dumps({'error': str(e)}), status=400, mimetype='application/json')
    except Exception as e:
        logging.error(f"Exception: {e} from IP: {request.remote_addr}")
        return Response(json.dumps({'error': 'Internal server error'}), status=500, mimetype='application/json')
