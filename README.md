# CloudSchool-PythonRestApi

Welcome to my Flask-restful API.
As part of participation in the CloudSchool Devops course by Fyber, our final project is to create Application that serves by tools like Terraform, Chef, Consul, Vault, Grafana, Jenkins, and more…

In order to use a complete environment:
you need to use this github project and apply all the prerequisites as written in README.md:
https://github.com/EliranKasif/CloudSchool-DEVOPS.git

If you want just run the application so:
1. git clone https://github.com/EliranKasif/CloudSchool-PythonRestApi.git
2. cd CloudSchool-PythonRestApi/
3. pip install -r requirements.txt
4. create app.conf the template is:
   * LOG_LEVEL = "INFO"
    * END_POINT = "free-to-play-games-database.p.rapidapi.com"
    * RAPID_API_KEY = <"your_rapid_api_key">
    * MYSQL_ENDPOINT = <your_mysql_endpoint>
    * SCHEMA_NAME = <"your_schema_in_database">
    * VAULT_ENDPOINT = <your_vault_endpoint>
    * VAULT_TOKEN = <"your_vault_token">
    * VAULT_PATH_TO_CREDS = <your_vault_path_to_cred>
    * APPLICATION_VERSION = <your_version>
5. python3 app.py

This application use Flask-restful API, MySql, Vault, AWS Cloudwatch as logger and Rapid API endpoint.





