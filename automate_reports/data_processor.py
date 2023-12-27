import csv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessor:

    @staticmethod
    def process_host_data(data):
        """Process raw API data to extract specific fields"""
        if not data:
            logging.warning("No data provided to process host data.")
            return []

        processed_data = []
        for item in data:
            host_identifiers = item.get('hostIdentifiers', [])
            ip_addresses = [identifier['value'] for identifier in host_identifiers if identifier.get('type') == 'IPAddress']
            host_info = {
                'ID': item.get('id'),
                'Entity ID': item.get('entity', {}).get('id'),
                'Entity Name': item.get('entity', {}).get('name'),
                'Hostname': item.get('name'),
                'IP Addresses': ip_addresses
            }
            processed_data.append(host_info)

        logging.info(f"Processed {len(processed_data)} host data items.")
        return processed_data

    @staticmethod
    def process_entities(data):
        """Process raw API data to extract specific fields, excluding entities starting with 'zzz'"""
        if not data:
            logging.warning("No data provided to process entities.")
            return []

        processed_data = []
        for item in data:
            entity_name = item.get('name', '')
            if not entity_name.startswith('zzz') and not entity_name.startswith('NYKUNDE'):
                host_info = {
                    'Entity ID': item.get('id'),
                    'Entity Name': entity_name
                }
                processed_data.append(host_info)

        logging.info(f"Processed {len(processed_data)} entity data items.")
        return processed_data

    @staticmethod
    def process_log_source_overview(data, entity):
        """Process raw API data to count occurrences of each log source type for a specific entity"""
        if not data:
            logging.warning("No data provided to process log source overview.")
            return []

        log_source_counts = {}
        for item in data:
            entity_name = item.get('entity', {}).get('name')
            if entity_name != entity:
                continue

            log_source_name = item.get('logSourceType', {}).get('name')
            if log_source_name and not log_source_name.startswith('LogRhythm'):
                log_source_counts[log_source_name] = log_source_counts.get(log_source_name, 0) + 1

        grand_total = sum(log_source_counts.values())
        processed_data = [{'Log Source Type': log_source, 'Count': count} for log_source, count in log_source_counts.items()]
        processed_data.append({'Log Source Type': 'Total Log Sources', 'Count': grand_total})

        logging.info(f"Processed log source overview for entity {entity}.")
        return processed_data

    @staticmethod
    def process_pending_log_sources(data, entity):
        """Process raw API data to extract specific fields and calculate the grand total."""
        if not data:
            logging.warning("No data provided to process pending log sources.")
            return []

        processed_data = []
        total_count = 0
        for item in data:
            collection_host_info = item.get('collectionHost', '')
            entity_name = collection_host_info.split(', ')[0].split(': ')[1] if ': ' in collection_host_info else ''
            
            if entity_name == entity:
                host_info = {
                    'Log Source Name': item.get('name'),
                    'IP Addresses': item.get('ip')
                }
                processed_data.append(host_info)
                total_count += 1

        processed_data.append({'Log Source Name': 'Total Pending Log Sources', 'IP Addresses': total_count})
        logging.info(f"Processed {total_count} pending log sources for entity {entity}.")
        return processed_data

    @staticmethod
    def process_log_volume(api_result):
        if not api_result:
            logging.warning("No data provided to process log volume.")
            return []

        processed_data = []
        seconds_per_day = 86400
        days_per_week = 7

        for item in api_result:
            log_source_info = item.get('logSourceTypeInfo', [])
            for log_info in log_source_info:
                log_source_type = log_info.get('logSourceType')
                if log_source_type.startswith("LogRhythm"):
                    continue

                logs_count = int(log_info.get('logsCount', 0))
                logs_per_day = round(logs_count / days_per_week)
                logs_per_sec = round(logs_count / (days_per_week * seconds_per_day))
                processed_entry = {
                    'Log Source Type': log_source_type,
                    'Logs Count': f"{logs_count:,}",
                    'Logs/D': f"{logs_per_day:,}",
                    'Logs/S': f"{logs_per_sec:,}"
                }
                processed_data.append(processed_entry)

        processed_data.sort(key=lambda x: x['Log Source Type'])
        total_logs = int(api_result[-1].get('totalLogs', 0))
        total_logs_per_day = round(total_logs / days_per_week)
        total_logs_per_sec = round(total_logs / (days_per_week * seconds_per_day))
        processed_data.append({'Log Source Type': 'Total Logs', 'Logs Count': f"{total_logs:,}", 'Logs/D': f"{total_logs_per_day:,}", 'Logs/S': f"{total_logs_per_sec:,}"})

        logging.info("Processed log volume data.")
        return processed_data

    @staticmethod
    def extract_alarm_ids(alarms):
        alarm_ids = []
        for alarm in alarms:
            alarm_id = alarm.get('alarmId')
            if alarm_id is not None:
                alarm_ids.append(alarm_id)

        logging.info(f"Extracted {len(alarm_ids)} alarm IDs.")
        return alarm_ids

    @staticmethod
    def extract_alarm_details(alarm_details, entity):
        if not alarm_details:
            logging.warning("No alarm details provided for extraction.")
            return []

        extracted_data = []
        total_alarms_count = 0  # Initialize counter for total number of alarms

        for detail in alarm_details:
            alarm_event = detail['alarmEventsDetails'][0]
            entity_name = alarm_event.get('entityName', 'N/A')
            if entity_name != entity:
                continue  # Skip this detail if entity does not match

            # Extract the required information
            log_source_name = alarm_event.get('logSourceName', 'N/A')
            log_date = alarm_event.get('logDate', 'N/A')
            log_source_host_name = alarm_event.get('logSourceHostName', 'N/A')
            
            # Append the extracted information to the list, without the entity name
            extracted_data.append({
                'Log Source Name': log_source_name,
                'Log Source Host Name': log_source_host_name,
                'Log Date': log_date
            })
            total_alarms_count += 1  # Increment the alarm counter

        # Optionally, append the total alarms count at the end if needed
        extracted_data.append({
            'Log Source Name': 'Total Alarms',
            'Log Source Host Name':'',
            'Log Date': total_alarms_count
        })

        logging.info(f"Processed {total_alarms_count} alarm details for the specified entity.")
        return extracted_data

    @staticmethod
    def write_to_csv(data, filename):
        if not data:
            logging.warning(f"No data to write to {filename}.")
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

            logging.info(f"Data successfully written to {filename}")
        except Exception as e:
            logging.error(f"Error writing to CSV file {filename}: {e}")
