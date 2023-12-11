<h2>ACI Terraform Server</h2><br>
Project Overview:

Several years ago, I was actively involved in the design and implementation of multiple Cisco ACI networks.
The central automation framework for this project was established using Terraform.
As the project progressed and reached completion, we found ourselves dealing with a considerable number of 
files and an even larger array of resources. The challenge of locating specific information within these files 
became increasingly complex. To address this, I decided to devise a solution to import Terraform files into a 
structured table format. Once the data was organised into a table structure, additional functionalities such as 
diffs and resource diagrams were seamlessly incorporated.

In summary, this project aims to provide structure, searchability, and visibility to Terraform files,
offering an organized and efficient approach to managing complex network configurations.

The aciTFServer is a Python package that offers the following capabilities:

Functionality:
- Import TF Files into MongoDB:
- Facilitates the seamless importation of Terraform files into a MongoDB database.

Dynamic Diff Outputs:
- Generates differential outputs each time the database is updated, allowing users to track changes efficiently.
- Comparisons and Diff Generation:
- Enables users to compare versions and generate detailed diff outputs for enhanced visibility.

Dependency Diagrams:
- Creates dependency diagrams for a given resource, showcasing its dependencies within the network architecture.
- Project Prerequisites and Dependencies
- Before getting started, ensure that you have the following prerequisites and dependencies in place:

Prerequisites:

- Python 3.9 (or higher): The project is built on Python, and it requires version 3.9 or higher to run successfully.
- MongoDB: A MongoDB instance is essential for storing and managing the imported Terraform data.
- Poetry: Poetry should be utilized to set up package dependencies.
- Git: Git is required for installing the code.

1) Clone Repository: Clone this repository to your local environment.
2) Install Dependencies: From the root of this repository, run "poetry install" to install the project library dependencies.
3) Start MongoDB: Ensure MongoDB is up and running.
4) set PYTHONPATH: From the root of this repository, run ". set_python_path.sh" 
5) Start Web Server: Run "make start" to start the web server.
6) Access Web Interface: Open a web browser and enter http://127.0.0.1:5020/acitfserver to access the project's web interface.

For detailed guidance, please refer to the how-to guides available in the "howTo" folder.












