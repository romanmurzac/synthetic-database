# Import necessary packages
import os

# Import necessary functions
from flask import Flask, flash, redirect, render_template, url_for, request, send_file
from gcloud import storage, exceptions

# Import internal utilities
from custom_module import generated_default, generated_custom, preview_data

# Define variables and constants
# Available fields in schema
columns = [{"field": "first_name"}, {"field": "last_name"}, {"field": "personal_number"}, {"field": "birthdate"},
           {"field": "address"}, {"field": "county"}, {"field": "phone_number"}, {"field": "mac_address"},
           {"field": "ip_address"}, {"field": "job"}, {"field": "iban"}, {"field": "currency"}, {"field": "balance"},
           {"field": "latitude"}, {"field": "longitude"}]
# Name of the saved file
file_name = ""
# Name the of the uploaded file
uploaded_file = ""
# Fields chosen from UI
selected_fields = []
# Fields detected in schema from uploaded file
custom_fields = []
# Custom name of the fields provided by the user
custom_fields_name = []

# Create Flask instance
app = Flask(__name__)
app.secret_key = 'fake-db-generator'


# Define function that render Home page
@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    """
    Function that render Home page
    :arg: None
    :return: render Home page
    """

    # Return rendered page
    return render_template("home.html")


# Define function that render Documentation page
@app.route('/documentation', methods=["GET", "POST"])
def about():
    """
    Function that render Documentation page
    :arg: None
    :return: render Documentation page
    """

    # Return rendered page
    return render_template("documentation.html")


# Define function that render Default Generator page
@app.route('/default-generator', methods=["GET", "POST"])
def generator_default():
    """
    Function that render Default Generator page
    :arg: None
    :return: render Default Generator page
    """
    # Change value for a global variable
    global file_name
    global selected_fields
    global custom_fields_name

    # Check if user submit data
    if request.method == "POST":
        # Retrieve user inputs and store them in variables
        raw_fields = request.form.getlist("field[]")
        rows_no = request.form.get("rows_select")
        file_name = request.form.get("name_select")
        # Process default and custom fields name
        selected_fields = [raw_fields[i] for i in range(len(raw_fields)) if i % 2 == 0]
        custom_fields_name = [raw_fields[i] for i in range(len(raw_fields)) if i % 2 == 1]

        # Generate data
        generated_default(selected_fields, custom_fields_name, rows_no, file_name)

    # Preview generated data
    header = preview_data(file_name)[0]
    reader = preview_data(file_name)[1]

    # Render default generator page with specified options
    return render_template("generator_default.html", columns=columns, header=header, reader=reader)


# Define function that render Custom Generator page
@app.route('/custom-generator', methods=["GET", "POST"])
def generator_custom():
    """
    Function that render Custom Generator page
    :arg: None
    :return: render Custom Generator page
    """
    # Change value for a global variable
    global file_name
    global custom_fields
    global custom_fields_name

    # Check if user submit data
    if request.method == "POST":
        # Retrieve user inputs and store them in variables
        rows_no = request.form.get("rows_select")
        file_name = request.form.get("name_select")

        # Generate data
        generated_custom(rows_no, custom_fields, file_name, custom_fields_name)

    # Preview generated data
    header = preview_data(file_name)[0]
    reader = preview_data(file_name)[1]

    # Render custom generator page with specified options
    return render_template("generator_custom.html", header=header, reader=reader)


# Define function to use Uploaded Schema
@app.route("/upload-schema", methods=["GET", "POST"])
def upload_schema():
    """
    Function that process Upload Schema in csv format
    :arg: None
    :return: redirect to the same page after success process
    """
    # Change value for a global variable
    global custom_fields_name
    global uploaded_file
    global custom_fields

    try:
        # Check if user submit data
        if request.method == "POST":
            # Retrieve uploaded file and store it
            uploaded_file = request.files["upload_file"]

            # Check if file is uploaded and save it
            if not uploaded_file:
                raise FileNotFoundError()
            uploaded_file.save(os.path.join(os.getcwd(), uploaded_file.filename))

            # Read uploaded file
            with open(os.path.join(os.getcwd(), uploaded_file.filename), "r", encoding='utf-8', newline="") as file:
                # Read first line from the file and process it, use for selected fields
                raw_list = file.readline().split(",")
                custom_fields = [field.replace("\r\n", "") for field in raw_list]
                # Read second line from the file and process it, use for fields custom name
                custom_fields_name = file.readline().replace("\r\n", "").split(",")

    # Catch error when file for uploading not selected
    except FileNotFoundError:
        flash("Select a file to upload schema.", category="error")

    # Redirect to the current page
    return redirect(url_for("generator_custom"))


# Define function that download data on Local
@app.route('/download', methods=["GET", "POST"])
def download_file():
    """
    Function that download to Local generated file
    :arg: None
    :return: download file to the Local storage
    """
    # Define the path from where take the file
    path = os.path.join(os.getcwd(), file_name + ".csv")

    try:
        # Download the file
        return send_file(path, as_attachment=True)

    # Catch error if the file doesn't exist
    except FileNotFoundError:
        flash(f"Unable to download the file.", category="error")

    # Redirect to the current page
    return redirect(request.referrer)


# Define function that upload data to GCP Storage
@app.route('/upload-cloud', methods=["GET", "POST"])
def upload_cloud():
    """
    Function that upload generated file to Cloud Storage
    :arg: None
    :return: Upload generated file to the Cloud Storage
    """
    try:
        # Define the path from where take the file and where to store it
        if request.method == "POST":
            client = storage.Client(project='YOUR-PROJECT-ID')
            bucket = client.get_bucket('YOUR-BUCKET-NAME')
            blob = bucket.blob(file_name + '.csv')
            if not file_name:
                raise ValueError()
            blob.upload_from_filename(os.path.join(os.getcwd(), file_name + ".csv"))
            flash(f"Successfully uploaded the database to the Cloud Storage.", category="success")

    # Catch error if the file doesn't exist
    except FileNotFoundError:
        flash(f"The file doesn't exists.", category="error")
    except ValueError:
        flash(f"The file wasn't generated.", category="error")

    # Redirect to the current page
    return redirect(request.referrer)


# Define function that download data from GCP Storage
@app.route('/download-cloud', methods=["GET", "POST"])
def download_cloud():
    """
    Function that download generated file from Cloud Storage
    :arg: None
    :return: Download generated file from the Cloud Storage
    """
    download_data = request.form.get("name_select")

    try:
        # Define the path from where take the file and where to store it
        if request.method == "POST":
            client = storage.Client(project='YOUR-PROJECT-ID')
            bucket = client.bucket('YOUR-BUCKET-NAME')
            blob = bucket.blob(download_data + '.csv')
            if not download_data:
                raise ValueError()
            blob.download_to_filename(os.path.join(os.getcwd(), download_data + ".csv"))

            # Download the file from Cloud to local disk
            path = os.path.join(os.getcwd(), download_data + ".csv")
            return send_file(path, as_attachment=True)

    # Catch error if the file name doesn't exist
    except exceptions.NotFound:
        flash(f"File with name {download_data} doesn't exist in Cloud.", category="error")
    # Catch error if the file doesn't exist
    except FileNotFoundError:
        flash(f"File with name {download_data} doesn't exist in Cloud.", category="error")
    # Catch error if the file name is empty
    except ValueError:
        flash("Introduce file name to be downloaded from Cloud.", category="error")

    # Redirect to the current page
    return redirect(request.referrer)


# Define execution for current file
if __name__ == '__main__':
    app.run(port=5000, debug=True)
