from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agent import generate_news_queries, search_news, scrape_website

app = FastAPI()

# Dummy function
def scrape_and_summarize(company_name: str):
    # Replace the following line with your actual scraping and summarizing logic
    return f"News summary for {company_name}"

# ensure correct data format str
class CompanyRequest(BaseModel):
    company_name: str

@app.post("/scrape/")
async def scrape(request: CompanyRequest):
    # Call the dummy function with the company name from the request
    result = scrape_and_summarize(request.company_name)
    query=generate_news_queries(request.company_name)
    market_news = search_news(query[4]['query']) # query[4] is the financial news query
    # should use a for loop to get all the news but for now just get the first one
    market_news_1 = scrape_website(query[4]['objective'],market_news[1]['link'])
    return {"company": request.company_name, "summary": market_news_1}

@app.get("/scrape/")
async def scrape_default():
    return {"company": "test default company", "summary": "today is a good day"}

# Run the server only if this file is executed directly
if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    '''
    acg_query=generate_news_queries('AGC Incorporated')
    acg_financial_news = search_news(acg_query[4]['query'])
    acg_f_news_1 = scrape_website(acg_query[4]['objective'],acg_financial_news[1]['link'])
    print(acg_f_news_1)
    print(acg_financial_news[1]['link'])
    '''

# test
