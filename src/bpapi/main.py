from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def sections():
    return {'fast': 'api'}