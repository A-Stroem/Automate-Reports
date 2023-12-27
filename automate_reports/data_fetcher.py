# Fetch Data - Almost done

# Generic API Call for main Endpoint - DONE

# Replace Customer name in pptx - DONE

# Get devices the customer currently has onboarded (LR) - DONE

# Get MPS level from last week till now (LR) - DONE

# Get missing log sources - DONE

# CFCS Log Source Recommendations (CFCS)
#https://www.cfcs.dk/da/forebyggelse/vejledninger/logning
#https://www.cfcs.dk/globalassets/cfcs/dokumenter/vejledninger/vejledning-logning-2023.pdf

# Customers Alarm Contacts (From OneNote) (Maybe DB)

# Table with usecases and riskassesement from Ledelsesrapport
import logging
import requests
from urllib.parse import urlencode
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Disable insecure request warnings
urllib3.disable_warnings(InsecureRequestWarning)

class APIHandler:

    #######################################################################################################################################################################
    #######################################################################################################################################################################

    def __init__(self):
        #Harcoded values
        self.BASE_ADMIN_URL = ""
        self.BASE_METRICS_URL = ""
        self.BASE_ALARM_URL = ""
        self.API_KEY = ""
        pass

    def make_api_call(self, endpoint, method='GET', params=None):
        url = f"{self.BASE_ADMIN_URL}/{endpoint}"
        headers = {'Authorization': f'Bearer {self.API_KEY}'}
        response = None

        try:
            logging.info(f"Making API call to {url}")
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, verify=False)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=params, verify=False)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e}"
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection Error: {e}"
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout Error: {e}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Request Error: {e}"
        except ValueError as e:
            error_msg = str(e)
        
        logging.error(error_msg)
        if response:
            logging.error("Response content: %s", response.content)
        
        return None, error_msg

    def make_metrics_api_call(self, endpoint, method='GET', params=None):
        url = f"{self.BASE_METRICS_URL}/{endpoint}"
        headers = {'Authorization': f'Bearer {self.API_KEY}'}
        response = None

        try:
            logging.info(f"Making API call to {url}")
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, verify=False)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=params, verify=False)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e}"
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection Error: {e}"
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout Error: {e}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Request Error: {e}"
        except ValueError as e:
            error_msg = str(e)
        
        logging.error(error_msg)
        if response:
            logging.error("Response content: %s", response.content)
        
        return None, error_msg


    def make_alarm_api_call(self, endpoint, method='GET', params=None):
        url = f"{self.BASE_ALARM_URL}/{endpoint}"
        headers = {'Authorization': f'Bearer {self.API_KEY}'}
        response = None

        try:
            logging.info(f"Making API call to {url}")
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, verify=False)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=params, verify=False)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e}"
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection Error: {e}"
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout Error: {e}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Request Error: {e}"
        except ValueError as e:
            error_msg = str(e)
        
        logging.error(error_msg)
        if response:
            logging.error("Response content: %s", response.content)
        
        return None, error_msg


    #######################################################################################################################################################################
    #######################################################################################################################################################################

    def fetch_with_pagination(self, base_endpoint, params, method='GET'):
        all_data = []
        count = 1000
        offset = 0
        error_message = None  # Initialize error message

        logging.info(f"Fetching data with pagination from {base_endpoint}")
        while True:
            pagination_params = {'count': count, 'offset': offset, **params}
            endpoint = f'{base_endpoint}?{urlencode(pagination_params)}' if method.upper() == 'GET' else base_endpoint
            response, error = self.make_api_call(endpoint, method, pagination_params if method.upper() == 'POST' else None)

            if error:
                logging.error(f"Error fetching data: {error}")
                error_message = error  # Store the error message
                break

            if not response:
                logging.warning("No response received from API.")
                break

            data_batch = response
            all_data.extend(data_batch)

            if len(data_batch) < count:
                break

            offset += count

        if error_message:
            return None, error_message  # Return None for data and the error message
        return all_data, None  # Return the data and None for the error message


    def fetch_metrics_with_pagination(self, base_endpoint, params, method='GET'):
        all_data = []
        count = 1000
        offset = 0
        error_message = None  # Initialize error_message

        logging.info(f"Fetching data with pagination from {base_endpoint}")
        while True:
            pagination_params = {'count': count, 'offset': offset, **params}
            endpoint = f'{base_endpoint}?{urlencode(pagination_params)}' if method.upper() == 'GET' else base_endpoint
            response, error = self.make_metrics_api_call(endpoint, method, pagination_params if method.upper() == 'POST' else None)

            if error:
                logging.error(f"Error fetching data: {error}")
                error_message = error  # Assign the error message
                break

            if not response:
                logging.warning("No response received from API.")
                break

            data_batch = response.get('data', [])
            if not data_batch:
                logging.warning("Data batch is empty or not present")
                break

            all_data.extend(data_batch)

            if len(data_batch) < count:
                break

            offset += count

        if error_message:
            return None, error_message  # Return None for data and the error message
        return all_data, None  # Return the data and None for the error message


    def fetch_alarms_with_pagination(self, base_endpoint, params, method='GET'):
        all_data = []
        count = 1000
        offset = 0
        error_message = None  # Initialize error_message

        logging.info(f"Fetching data with pagination from {base_endpoint}")
        while True:
            pagination_params = {'count': count, 'offset': offset, **params}
            endpoint = f'{base_endpoint}?{urlencode(pagination_params)}' if method.upper() == 'GET' else base_endpoint
            response, error = self.make_alarm_api_call(endpoint, method, pagination_params if method.upper() == 'POST' else None)

            if error:
                logging.error(f"Error fetching data: {error}")
                error_message = error  # Store the error message
                break

            if not response:
                logging.warning("No response received from API.")
                break

            # The data is under 'alarmsSearchDetails', not 'data'
            data_batch = response.get('alarmsSearchDetails', [])
            if not data_batch:
                print("Data batch is empty or not present")
                break

            all_data.extend(data_batch)

            # Pagination check
            if len(data_batch) < count:
                break

            offset += count

        if error_message:
            return None, error_message  # Return None for data and the error message
        return all_data, None  # Return the data and None for the error message


    #######################################################################################################################################################################
    #######################################################################################################################################################################


    def fetch_entity_hosts(self, entity):
        """Method to handle specific API call with customized parameters"""
        count = 1000
        status = "active"
        endpoint = f'hosts/?count={count}&entity={entity}&recordStatus={status}'

        logging.info(f"Fetching Entity Hosts for {entity}")
        response, error = self.make_api_call(endpoint)
        if error:
            logging.error(f"Error fetching entity hosts: {error}")
            return None
        return response

    def fetch_entities(self):
        params = {        
            
        }
        logging.info(f"Fetching entities")
        response, error = self.fetch_with_pagination('entities/', params)
        if error:
            logging.error(f"Error fetching entities: {error}")
            return None
        return response

    def fetch_entity_log_source_overview(self, entityId):
        params = {        
            'recordStatus': 'active',
            'orderBy': 'logSourceType',
            'entityId': entityId
        }
        logging.info(f"Fetching Log Sources")
        response, error = self.fetch_with_pagination('logsources/', params)
        if error:
            logging.error(f"Error fetching log sources: {error}")
            return None
        return response

    def fetch_entity_pending_log_sources(self):
        params = {
            'logSourceAcceptanceStatus': 'Pending',
            'orderBy': 'name'
        }
        logging.info(f"Fetching Pending Log Sources")
        response, error = self.fetch_with_pagination('logsources-request/', params)
        if error:
            logging.error(f"Error fetching pending log sources: {error}")
            return None
        return response
    
    def fetch_entity_log_volume(self, entityId):
        # Calculate dates
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        # Format dates to 'YYYY-MM-DD'
        max_date = today.strftime('%Y-%m-%d')
        min_date = week_ago.strftime('%Y-%m-%d')

        # Prepare parameters
        params = {
            'minDate': min_date,
            'maxDate': max_date,
            'groupBy': {
                'fieldName': 'Entity',
                'Ids': [entityId]
            }
        }
        logging.info(f"Fetching Log Volume for Entity ID: {entityId}")
        response, error = self.fetch_metrics_with_pagination('logvolume/', params, method='POST')
        if error:
            logging.error(f"Error fetching log volume: {error}")
            return None
        return response
    
    def fetch_alarms(self, entity):
        today = datetime.now().strftime('%Y-%m-%d')  # Full timestamp format

        params = {
            'alarmRuleName': 'DBX: LogRhythm Silent Log Source Error',
            'dateInserted': today,
            'entityName': entity,
            'count': 1000  # Adjust based on how many results you want per page
        }
        logging.info(f"Fetching Alarms")
        response, error = self.fetch_alarms_with_pagination('alarms/', params, method='GET')
        if error:
            logging.error(f"Error fetching alarms: {error}")
            return None
        return response

    def fetch_alarm_details(self, alarm_ids):
        alarm_details = []

        logging.info("Fetching alarm details")
        for alarm_id in alarm_ids:
            resource = f"/alarms/{alarm_id}/events"
            response, error = self.make_alarm_api_call(resource, method='GET')

            if error:
                logging.error(f"Error fetching alarm details for alarm ID {alarm_id}: {error}")
                continue

            if not response:
                logging.warning(f"No response received for alarm ID {alarm_id}.")
                continue

            alarm_details.append(response)

        return alarm_details


    #######################################################################################################################################################################
    #######################################################################################################################################################################
