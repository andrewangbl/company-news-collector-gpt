import uvicorn

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
    return {"company": request.company_name, "summary": result}

@app.get("/scrape/")
async def scrape_default():
    return {"company": "test default company", "summary": "today is a good day"}

# Run the server only if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# test
