# GitSummary - GitHub Repository Summary
GitSummary is a web application that allows users to search for GitHub repositories and view details about them. Additionally, users can save repositories, view their saved repositories, and explore further details about each repository.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Bug](#bugs)
- [Contributing](#contributing)
- [Author](#Author)


## Features
1. **Search Repositories:** Users can search for GitHub repositories using a simple search query.

2. **View Repository Details:** Detailed information about the repository, including name, owner, description, stars, and more.

3. **Save Repositories:** Authenticated users can save repositories for future reference.

4. **View Saved Repositories:** Users can view a list of their saved repositories.

5. **Explore Repository Contents:** Users can explore the files and folders within a repository.

6. **Profile Management:** Users can upload a profile picture and update their account details.

7. **Password Reset:** Users can request a password reset via email.


## Installation

Follow the steps below to set up and run the GitSummary application:

1. Clone the repository:

```bash
git clone https://github.com/Khiingleo/GitSummary.git
```

2. Create a virtual environment (Optional but recommended):

```bash
python -m venv venv
```

3. Activate the virtual environment

* on Windows:
```bash
.\venv\Scripts\activate
```

* on Linux
```bash
source venv/bin/activate
```

## Usage 
1. set up the necessary configurations 
2. run application

```bash
python run.py
```

## Dependencies

Ensure you have the following packages installed 

- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Login
- Pillow
- pyjwt
- Flask-Mail

you can install them using;
```bash
pip install flask flask-wtf flask-sqlalchemy flask-bcrypt flask-login pillow pyjwt flask-mail
```

## Configuration
Create a .env file in the project root and set the following environment variables:

- SECRET_KEY='your_secret_key'
- SQL_URI='yoursqluri'
- MAIL_USERNAME='yourmailusername'
- MAIL_PASSWORD='yourmailpassword' or MAIL_PASSWORD=yourapppassword

## BUGS
The application has a bug of multiple instances of subfolders in a repository when you click it more than once

## Contributing
If you would like to contribute to this project, feel free to create an issue or submit a pull request. Your contributions are welcome!

## Author
This web application was created by Shalom Ogoziem
