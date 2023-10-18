from fastapi import FastAPI, HTTPException
from engine import fetch_questions


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/get_questions/")
def get_questions(questions_num: int):
    if questions_num <= 0:
        raise HTTPException(status_code=400, detail="Invalid questions_num value")
    questions = fetch_questions(questions_num)
    return {"questions": questions}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
