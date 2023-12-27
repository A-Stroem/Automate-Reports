import os
from datetime import datetime
from data_fetcher import APIHandler
from data_processor import DataProcessor
from powerpoint_operations import PowerPointProcess

    #######################################################################################################################################################################
    #######################################################################################################################################################################

# NOTE: Right now it is filtering fetches on entity. In final verison remove that, so it fetches everything at once.

import os

import csv

def print_csv_contents(csv_path):
    """
    Reads a CSV file and prints out its contents.

    :param csv_path: Path to the CSV file.
    """
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)  # Print each row
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

# Example usage
csv_file_path = "Z:/Final Project/Data_export_tests/Scandlines Danmark/Scandlines Danmark_missing_logs.csv"
print_csv_contents(csv_file_path)


""" def clear_screen():
    # Clear the console screen.
    os.system('cls' if os.name == 'nt' else 'clear')

def display_entities_and_select(processed_entities):
    #clear_screen()
    print("Select an option:")
    print("[1] Single entity")
    print("[2] Multiple entities")
    print("[3] All entities")

    choice = input("Enter your choice: ")
    selected_entities = []

    # Clear the screen after the choice is made
    clear_screen()

    # Sort entities alphabetically by name after the choice is made
    processed_entities.sort(key=lambda x: x['Entity Name'])

    if choice == "1":  # Single entity
        for index, entity in enumerate(processed_entities, start=1):
            print(f"[{index}] {entity['Entity Name']}")
        entity_index = int(input("Enter the number of the entity: ")) - 1
        selected_entities = [processed_entities[entity_index]]

    elif choice == "2":  # Multiple entities
        for index, entity in enumerate(processed_entities, start=1):
            print(f"[{index}] {entity['Entity Name']}")
        entity_indices = input("Enter the numbers of the entities (comma-separated): ")
        selected_indices = [int(idx.strip()) - 1 for idx in entity_indices.split(',')]
        selected_entities = [processed_entities[idx] for idx in selected_indices]

    elif choice == "3":  # All entities
        selected_entities = processed_entities

    return selected_entities


def ensure_directory_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

def main():

    # Create instances of classes
    api_handler = APIHandler()
    data_processor = DataProcessor()
    powerpoint_processor = PowerPointProcess()

    print("Connecting to API...\n Please Wait :)")
    # Fetch entities from API
    entities = api_handler.fetch_entities()

    # Process entities and display for user selection
    processed_entities = data_processor.process_entities(entities)
    selected_entities = display_entities_and_select(processed_entities)

    # Now you can loop over each selected entity and perform actions
    for entity_info in selected_entities:
        entity = entity_info['Entity Name']
        entity_id = entity_info['Entity ID']

        # Set relevant variables
        csv_ext = ".csv"
        #entity = ""
        #entityId = 0
        ppt_name = "Q3DIRTogMDR"
        replacements = {
            "<Kunden>": entity,
            "<Dato>": datetime.now().strftime("%d/%m/%Y")
        }

        # Set relevant paths
        # Set the base directory and entity name
        base_directory = "Z:/Final Project/Data_export_tests"

        # Create the entity-specific directory
        entity_directory = os.path.join(base_directory, entity)
        ensure_directory_exists(entity_directory)

        template_path = "Z:/Final Project/Powerpoint Template/Statusmøde, Q3DIRTogMDR.pptx"  # Update with your actual template path

        # Set slide numbers for PowerPoint
        slide_number1 = 17  # Log Source Overview
        slide_number2 = 18  # MPS/Log Volume
        slide_number3 = 19  # Missing Logs/SLS Alarms
        slide_number4 = 20  # Pending Logs

        # Set filenames and filepaths
        filename1 = f"{entity}_log_source_overview{csv_ext}"
        csv_path1 = os.path.join(entity_directory, filename1)

        filename2 = f"{entity}_log_volume{csv_ext}"
        csv_path2 = os.path.join(entity_directory, filename2)

        filename3 = f"{entity}_missing_logs{csv_ext}"
        csv_path3 = os.path.join(entity_directory, filename3)

        filename4 = f"{entity}_pending_log_sources{csv_ext}"
        csv_path4 = os.path.join(entity_directory, filename4)

#######################################################################################################################################################################
#######################################################################################################################################################################

        # API calls for fetching data
        log_source_overview = api_handler.fetch_entity_log_source_overview(entity_id)
        log_volume = api_handler.fetch_entity_log_volume(entity_id)
        alarms = api_handler.fetch_alarms(entity)
        alarm_ids = DataProcessor.extract_alarm_ids(alarms)
        missing_logs = api_handler.fetch_alarm_details(alarm_ids)
        pending_log_sources = api_handler.fetch_entity_pending_log_sources()

#######################################################################################################################################################################
#######################################################################################################################################################################

        # Process data from API calls
        processed_log_source_overview = DataProcessor.process_log_source_overview(log_source_overview, entity)
        processed_log_volume = DataProcessor.process_log_volume(log_volume)
        processed_missing_logs = DataProcessor.extract_alarm_details(missing_logs, entity)
        processed_pending_log_sources = DataProcessor.process_pending_log_sources(pending_log_sources, entity)

#######################################################################################################################################################################
#######################################################################################################################################################################

        # Write processed data from API calls to csv files
        DataProcessor.write_to_csv(processed_log_source_overview, csv_path1)
        DataProcessor.write_to_csv(processed_log_volume, csv_path2)
        DataProcessor.write_to_csv(processed_missing_logs, csv_path3)
        DataProcessor.write_to_csv(processed_pending_log_sources, csv_path4)

#######################################################################################################################################################################
#######################################################################################################################################################################


        # Copy a PowerPoint template and rename it
        copied_ppt_path = PowerPointProcess.copy_and_rename_ppt(template_path, entity_directory, entity, ppt_name)
        # Replace placeholder text in PowerPoint
        PowerPointProcess.replace_text_in_ppt(copied_ppt_path, replacements)

        # Set arguments for adding data into PowerPoint
        ppt_path = copied_ppt_path # Update with your actual path
        table_details = [
            (slide_number1, csv_path1, 0.5, 1.6),
            (slide_number2, csv_path2, 1.2, 1.2),
            (slide_number3, csv_path3, 0.5, 1.2),
            (slide_number4, csv_path4, 1.2, 1.2)
            # Add more as needed
        ]
        PowerPointProcess.add_tables_to_powerpoint(ppt_path, table_details)


#######################################################################################################################################################################
#######################################################################################################################################################################

if __name__ == "__main__":
    main() """
