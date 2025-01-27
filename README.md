# DevSecOps-NYIT-VAN

Welcome to the DevSecOps-NYIT-VAN project repository! This project is part of the INCS-870-VA-2025 course and focuses on integrating security practices within the DevOps pipeline.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

This project aims to demonstrate the implementation of DevSecOps principles by incorporating security measures throughout the development and deployment processes. It includes a sample Python web application, infrastructure as code configurations, and CI/CD pipelines with integrated security checks.

## Features

- **Python Web Application**: A Flask-based web app demonstrating secure coding practices.
- **Infrastructure as Code**: Kubernetes configurations for deploying the application.
- **CI/CD Pipeline**: Automated workflows for building, testing, and deploying the application with security scans.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- **Python 3.9**: Ensure Python 3.9 is installed on your system.
- **Docker**: Required for containerization.
- **Kubernetes**: For deploying the application.
- **pip**: Python package installer.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BrenesRM/DevSecOps-NYIT-VAN.git
   cd DevSecOps-NYIT-VAN

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Set Up the Database**:
   ```bash
   python init_db.py

### Project Structure

   DevSecOps-NYIT-VAN/  
   ├── .github/           # GitHub workflows and configurations  
   ├── argo/              # Argo CD configurations  
   ├── k8s/               # Kubernetes deployment files  
   ├── static/            # Static assets (CSS, images)  
   ├── templates/         # HTML templates  
   ├── tests/             # Test cases  
   ├── Dockerfile         # Docker configuration  
   ├── README.md          # Project documentation  
   ├── app.py             # Main application code  
   ├── init_db.py         # Database initialization script  
   ├── requirements.txt   # Python dependencies  
   └── project.tex        # LaTeX project report  

### Contributing

1.Fork the repository.  
2.Create a new branch (git checkout -b feature-branch).  
3.Commit your changes (git commit -m 'Add new feature').  
4.Push to the branch (git push origin feature-branch).  
5.Open a Pull Request.  

### License
This project is licensed under the MIT License.  

### Contact
For any questions or suggestions, feel free to open an issue or contact the project maintainers.  

Thank you for checking out the DevSecOps-NYIT-VAN project! We hope this repository serves as a valuable resource for understanding and implementing DevSecOps practices.  
