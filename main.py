from fastapi import FastAPI
app = FastAPI()

@app.get("/day")
def hello(days = None):
  if days is None:
    return {"No se han especificado días"}
  else:
    return {"Se ha elegido utilizar {} días".format(days)}