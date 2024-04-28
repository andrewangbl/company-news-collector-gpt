from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from ai_agent import generate_news_queries, search_news, scrape_website

from supabase import create_client, Client


app = FastAPI()


SUPABASE_URL = 'https://zssvyrzmkiactcjpplef.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpzc3Z5cnpta2lhY3RjanBwbGVmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQyMjU4NTYsImV4cCI6MjAyOTgwMTg1Nn0.epg726eSwk1mJBiMjYDunKpU8B47iEllbLAxk2vjYUg'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class CompanyRequest(BaseModel):
    company_name: str

async def fetch_suppliers() -> list:
    data = supabase.table('supplier').select('id,supplier_name').execute()
    return data.data

def insert_summary(supabase_client: Client, supplier_id: str, summary_content: str, news_url: str, news_title: str):
    result = supabase_client.table('summary').insert({
        'content': summary_content,
        'supplier_id': supplier_id,  # Ensure this matches a valid UUID of a supplier in the supplier table
        "news_url": news_url,
        "news_title": news_title
    }).execute()
    return result

def scrape_and_summarize(supabase_client: Client, supplier):
    supplier_id = supplier['id']  # Use the UUID
    supplier_name = supplier['supplier_name']
    query = generate_news_queries(supplier_name)
    market_news = search_news(query[4]['query']) # query[4] is the financial news query
    # check the function of generate_news_queries for more queries options

    # Use a for loop to get all the news and summarize
    for news in market_news:
        market_news_summary = scrape_website(query[4]['objective'], news['link'])
        insert_summary(supabase_client, supplier_id, market_news_summary, news['link'], news['title'])


@app.post("/scrape/")
async def scrape(background_tasks: BackgroundTasks):
    suppliers = await fetch_suppliers()
    for supplier in suppliers:
        background_tasks.add_task(scrape_and_summarize, supabase, supplier)
    return {"message": suppliers} # might need to change to "scraping started" or something similar









# Run the server only if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    '''
    acg_query=generate_news_queries('AGC Incorporated')
    acg_financial_news = search_news(acg_query[4]['query'])
    acg_f_news_1 = scrape_website(acg_query[4]['objective'],acg_financial_news[1]['link'])
    print(acg_f_news_1)
    print(acg_financial_news[1]['link'])
    '''

# test
