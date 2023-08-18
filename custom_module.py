# Import necessary packages
import random
import csv
import os

# Import necessary modules
from faker import Faker
from flask import flash

# Create Faker instance with Romanian data
fake = Faker("ro_RO")


# Define function to generate data
def data_generator(*args: list) -> list:
    """
    Function that takes a list of fields, generate data for each field and return them in a list
    :parameter: *args: list of fields that serve as a schema
    :return: data_list: list that contains data for each column
    """
    # Initialize empty lists
    data_list = list()
    temp_list = list()

    # Store selected fields in temporary list
    for arg in args:
        temp_list.append(arg)
    temp_list = temp_list[0]

    # Iterate through each field in the list
    for field in temp_list:

        # Generate first name
        if field == "first_name":
            data_list.append(fake.first_name())

        # Generate last name
        if field == "last_name":
            data_list.append(fake.last_name())

        # Generate persona number
        if field == "personal_number":
            data_list.append(fake.ssn())

        # Generate birthdate
        if field == "birthdate":
            data_list.append(fake.date_of_birth())

        # Generate address
        if field == "address":
            data_list.append(fake.address().replace("\n", ", "))

        # Generate county
        if field == "county":
            data_list.append(fake.state())

        # Generate phone number
        if field == "phone_number":
            data_list.append(fake.phone_number())

        # Generate mac address
        if field == "mac_address":
            data_list.append(fake.mac_address())

        # Generate ip address
        if field == "ip_address":
            data_list.append(fake.ipv4())

        # Generate job
        if field == "job":
            data_list.append(fake.job())

        # Generate iban
        if field == "iban":
            data_list.append(fake.iban())

        # Generate currency code
        if field == "currency":
            data_list.append(fake.currency_code())

        # Generate balance
        if field == "balance":
            data_list.append(random.randint(0, 100_000_000_000))

        # Generate latitude
        if field == "latitude":
            data_list.append(fake.latitude())

        # Generate longitude
        if field == "longitude":
            data_list.append(fake.longitude())

    # Return generated data
    return data_list


# Define function that process input data for default option
def generated_default(selected_fields: list, custom_fields_name: list, rows_no: str, file_name: str) -> None:
    """
    Function that process retrieved data for default option and save them in file
    :param selected_fields: schema to be used in database
    :param custom_fields_name: database fields custom name
    :param rows_no: number of data rows to be generated
    :param file_name: database name
    :return: None
    """
    try:
        # Check if file name was provided
        if not file_name:
            raise FileExistsError()

        # Generate data for provided schema and number of rows
        raw_data = []
        for _ in range(int(rows_no)):
            raw_data.append(data_generator(selected_fields))

        # Open created file
        with open(os.path.join(os.getcwd(), file_name + ".csv"), "w",
                  encoding='utf-8', newline="") as file:
            writer = csv.writer(file)

            # Write header row
            # If custom name for field was provided write it as header, otherwise use default
            header_data = []
            for (custom_name, default_name) in zip(custom_fields_name, selected_fields):
                if custom_name:
                    header_data.append(custom_name)
                else:
                    header_data.append(default_name)
            writer.writerow(header_data)

            # Write generated data
            for row in range(int(rows_no)):
                writer.writerow(raw_data[row])

            # Display a message after complete the job
            flash(f"Successfully were written {rows_no} rows in {file_name} file.", category="success")

    # Catch errors if the number of rows to be generated is not introduced
    except ValueError:
        flash("Introduce the number of rows to be generated.", category="error")
    # Catch errors if the name of the file is not introduced
    except FileExistsError:
        flash("Introduce the name of the file.", category="error")


# Define function that process input data for custom option
def generated_custom(rows_no: str, selected_fields: list, file_name: str,
                     custom_fields_name: list) -> None:
    """
    Function that process retrieved data for custom option and save them in file
    :param rows_no: number of data rows to be generated
    :param selected_fields: schema to be used in database
    :param file_name: database name
    :param custom_fields_name: database fields custom name
    :return: None
    """
    try:
        # Check if file name was provided
        if not file_name:
            raise FileExistsError()

        # Generate data for provided schema and number of rows
        raw_data = []
        for _ in range(int(rows_no)):
            raw_data.append(data_generator(selected_fields))

        # Write data to database
        with open(os.path.join(os.getcwd(), file_name + ".csv"), "w",
                  encoding='utf-8', newline="") as file:
            writer = csv.writer(file)

            # Write header row
            # If in custom schema was provided the custom names
            # of the fields write it as header, otherwise use default
            if custom_fields_name is None:
                writer.writerow(selected_fields)
            else:
                if custom_fields_name[0] != "":
                    writer.writerow(custom_fields_name)
                else:
                    writer.writerow(selected_fields)
            # Write generated data
            for row in range(int(rows_no)):
                writer.writerow(raw_data[row])

            # Display a message after complete the job
            flash(f"Successfully were written {rows_no} rows in {file_name} file.", category="success")

    # Catch errors if the number of rows to be generated is not introduced
    except ValueError:
        flash("Introduce the number of rows to be generated.", category="error")
    # Catch errors if the name of the file is not introduced
    except FileExistsError:
        flash("Introduce the name of the file.", category="error")


# Define function that render preview section
def preview_data(file_name: str) -> tuple:
    """
    Function that render data Preview section
    :parameter file_name: file from where read data to be displayed
    :return: header data and all rows
    """
    try:
        # Open the submitted file and display it in browser
        file = open(os.path.join(os.getcwd(), file_name + ".csv"), "r", newline='',
                    encoding='utf-8')
        # Display header and all lines
        reader = csv.reader(file)
        header = next(reader)

    # Catch error when the file is not provided and display empty value
    except FileNotFoundError:
        # Display empty values
        reader = ""
        header = ""

    # Return tuple with header and data lists
    return header, reader
