# procuro_agent

## FastAPI Backend with Supabase Integration

This project demonstrates how to build a scalable backend API using FastAPI and integrate it with Supabase for handling relational data operations, authentication, and real-time data updates. It includes functionalities for scraping news, summarizing content, and storing data securely in a Supabase database.

## Features

- **API for News Scraping**: Automated scraping of news articles from predefined sources.
- **Data Summarization**: Summarizes scraped news content using AI techniques.
- **CRUD Operations**: Complete CRUD capabilities for managing data.
- **User Authentication**: Integrated user authentication using Supabase Auth.
- **Deployment on Render**: Configured for deployment on Render with high availability.

## Technologies Used

- **FastAPI**: For creating the backend API.
- **Supabase**: As the backend database and for authentication.
- **Python**: Primary programming language.
- **BeautifulSoup & Requests**: For scraping websites.
- **Pydantic**: For data validation and settings management.
- **Render**: For deployment and hosting.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```bash
python -m pip install fastapi uvicorn supabase-py beautifulsoup4 requests pydantic
```

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

Clone the repository:

```bash
git clone https://github.com/yourusername/yourprojectname.git
cd yourprojectname
```

Set up your environment variables:

Copy the .env.example to a new file called .env and fill in the necessary Supabase credentials and other configurations.


Run the server:

```bash
uvicorn main:app --reload
```

This will start the FastAPI server in development mode and reload automatically for any changes you make.

### Usage

Here's a brief example of how to use the API once it's up and running:

```bash
curl -X POST http://127.0.0.1:8000/scrape/ -H "Content-Type: application/json" -d '{"company_name": "Example Company"}'
```

This command would initiate the scraping and summarization process for the specified company.

## Deployment

Instructions on how to deploy this on a live system like Render:

- Set up your project on Render - Follow the instructions from Render's documentation to deploy a Python application.
- Configure your environment variables on Render to match your .env settings.



## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
