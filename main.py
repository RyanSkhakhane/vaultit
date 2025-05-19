from wsgiref.util import request_uri

from fastapi import FastAPI, HTTPException, Query
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from CRUD import (
    create_auto_gen, create_manual_gen,
    read_user, update_manual_gen, update_pwd_auto_gen,
    delete_user
)

templates = Jinja2Templates(directory="assets")
app = FastAPI()
app.mount("/static", StaticFiles(directory="assets/static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/vaultit", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# AUTO CREATE
# @app.get("/create-auto", response_class=HTMLResponse)
# def auto_create_password(request: Request):
#     return templates.TemplateResponse("auto_create_password.html", {"request": request})

@app.get("/create", response_class=HTMLResponse)
def show_update_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create/auto")
def create_auto(username: str = Form(...), website: str = Form(...)):
    password = create_auto_gen(username, website)
    return {
        "message": "User created successfully (auto-generated password)",
        "username": username,
        "website": website,
        "password": password
    }

# MANUAL CREATE
# @app.get("/create-manual", response_class=HTMLResponse)
# def create_password(request: Request):
#     return templates.TemplateResponse("create_password.html", {"request": request})

@app.post("/create/manual")
def create_manual(username: str =Form(...), website: str=Form(...), password: str=Form(...)):
    create_manual_gen(username, website, password)
    return {
        "message": "User created successfully (manual password)",
        "username": username,
        "website": website,
        "password": password
    }

# READ
@app.get("/read-password", response_class=HTMLResponse)
def read_password(request: Request):
    return templates.TemplateResponse("read.html", {"request": request})

@app.get("/read/")
def read(username: str = Query(None), website: str = Query(None)):
    if not username and not website:
        raise HTTPException(status_code=400, detail="Must provide username or website.")
    user = read_user(username or "", website or "")
    if user == "Not found":
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user[0],
        "username": user[1],
        "website": user[2],
        "password": user[3]
    }



@app.get("/update", response_class=HTMLResponse)
def show_update_form(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


# AUTO UPDATE
@app.put("/update/auto")
def update_auto(username: str = Query(None), website: str = Query(None)):
    if not username and not website:
        raise HTTPException(status_code=400, detail="Must provide username or website.")
    updated = update_pwd_auto_gen(username or "", website or "")
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password auto-updated successfully"}

# MANUAL UPDATE
@app.put("/update/manual")
def update_manual(username: str = Query(None), website: str = Query(None), new_password: str = Query(...)):
    if not username and not website:
        raise HTTPException(status_code=400, detail="Must provide username or website.")
    updated = update_manual_gen(username or "", website or "", new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password manually updated successfully"}

# DELETE
@app.get("/delete", response_class=HTMLResponse)
def show_delete_form(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})


@app.delete("/delete/")
def delete(username: str, website: str):
    if not delete_user(username, website):
        raise HTTPException(status_code=404, detail="User not found or mismatch")
    return {"message": "User deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
