import numpy as np
import pandas as pd

import os
from dotenv import load_dotenv

# from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool

from pydantic import BaseModel, Field
from typing import Type

from bs4 import BeautifulSoup
import requests
import json

from langchain.schema import SystemMessage

from langchain_community.utilities import GoogleSerperAPIWrapper

from langchain.prompts import PromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper



load_dotenv()
BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 1. Tool for research
def search_news(query,tbs_time='qdr:w'):
    search = GoogleSerperAPIWrapper(type="news",
                                    tbs=tbs_time,
                                    serper_api_key=SERP_API_KEY)
    results = search.results(query)

    return results['news']


# 2. Tool for scraping
def scrape_website(objective: str, url: str):

    print('Scraping website...')  # Don't need it to be verbose
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url,
    }

    # Convert Python object to json format
    data_json = json.dumps(data)

    # Send the POST request
    post_url = f"https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}"
    response = requests.post(post_url, headers=headers, data=data_json)

    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        print('CONTENT:', text)  # Don't need this to be verbose

        output = summary(objective, text)
        return output

#         if len(text) > 10000:
#             output = summary(objective, text)
#             return output
#         else:
#             return text

    else:
        print(f"HTTP request failed with status code: {response.status_code}")


def summary(objective:str, content:str):
    llm = ChatOpenAI(api_key=OPENAI_API_KEY,
                     temperature=0,
                     model="gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"],
                                                   chunk_size=10000,
                                                   chunk_overlap=500)

    docs = text_splitter.create_documents([content])


    map_prompt = """
    As a supply chain analyst, summarize the following news to extract crucial business insights and data
    for {objective}:
    "{text}"
    If there is nothing relative to the {objective}, reply with *NOT RELEVANT*.
    SUMMARY:
    """

    map_prompt_template = PromptTemplate(template=map_prompt,
                                         input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True  # or true
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output


class ScrapeWebsiteInput(BaseModel):
    """Inputs for scrape_website tool"""
    objective: str = Field(
        description="The objective & task that users give to the agent")
    url: str = Field(description="The url of the website to be scraped")

    # Adapt code here for agent search


class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = "useful when you need to get data from a website url, passing both url and objective to the function; DO NOT make up any url"
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, objective: str, url: str):
        return scrape_website(objective, url)

    def _arun(self, url: str):
        raise NotImplementedError("error here")



def summary(objective:str, content:str):
    llm = ChatOpenAI(api_key=OPENAI_API_KEY,
                     temperature=0,
                     model="gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"],
                                                   chunk_size=10000,
                                                   chunk_overlap=500)

    docs = text_splitter.create_documents([content])


    map_prompt = """
    As a supply chain analyst, summarize the following news to extract crucial business insights and data
    for {objective}:
    "{text}"
    If there is nothing relative to the {objective}, reply with strictly with *NOT RELEVANT*.
    SUMMARY:
    """

    map_prompt_template = PromptTemplate(template=map_prompt,
                                         input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True  # or true
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

def generate_news_queries(supplier_name):
    """
    Generates a list of specific news queries along with corresponding objectives

    Args:
    supplier_name (str): The name of the supplier company.

    Returns:
    list: A list of tuples, each containing a query string and a corresponding objective related to the supplier company.
    """
    queries_with_objectives = [
        {'query': f"{supplier_name} financial reports",
         'type': 'financial reports',
         'objective': f"Analyzing financial health and performance trends of {supplier_name}"},
        {'query': f"{supplier_name} corporate announcements",
         'type': 'corporate announcements',
         'objective': f"Identifying key corporate decisions and strategic directions of {supplier_name}"},
        {'query': f"{supplier_name} supply chain",
         'type': 'supply chain',
         'objective': f"Evaluating supply chain stability and efficiency of {supplier_name}"},
        {'query': f"{supplier_name} .",
         'type': 'service updates',
         'objective': f"Gauging service improvements or changes of {supplier_name}"},
        {'query': f"{supplier_name} market analysis",
         'type': 'market analysis',
         'objective': f"Assessing market position and competitive landscape of {supplier_name}"},
        {'query': f"{supplier_name} industry trends",
         'type': 'industry trends',
         'objective': f"Identifying industry-wide shifts and trends affecting {supplier_name}"},
        {'query': f"{supplier_name} regulatory compliance",
         'type': 'regulatory compliance',
         'objective': f"Understanding compliance status and regulatory challenges of {supplier_name}"},
        {'query': f"{supplier_name} legal news",
         'type': 'legal news',
         'objective': f"Gaining insights into legal matters and potential litigations involving {supplier_name}"},
        {'query': f"{supplier_name} workforce",
         'type': 'workforce',
         'objective': f"Analyzing workforce dynamics, labor relations, and employee matters at {supplier_name}"}
    ]

    return queries_with_objectives

def test():
    print("Test: OK")
