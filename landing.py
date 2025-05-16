

app = FastAPI()




@app.post("/create/")
def create_user(username: str = Form(...), website: str = Form(...)):
    # Call your create_auto_gen or similar here
    password = create_auto_gen(username, website)
    return {"username": username, "website": website, "password": password}
