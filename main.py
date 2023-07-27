import time
from typing import List
from fastapi import FastAPI, UploadFile, File
from py_scripts.prepare_data.read_files import main as read_files
from py_scripts.prepare_data.merge_results import main as merge_data
from py_scripts.prepare_data.prepare_final_state import main as clean_data

app = FastAPI()

@app.get("/")
def hello(days = None):
	if days is None:
		return {"No se han especificado días"}
	else:
		return {"Se ha elegido utilizar {} días".format(days)}

@app.post("/file")
def upload_file(file: UploadFile):
  file_location = 'files/' + file.filename
  open(file_location, 'wb').write(file.file.read())
  return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/files")
def upload_files(files: List[UploadFile] = File(...)):
	for file in files:
		file_location = 'files/' + file.filename
		open(file_location, 'wb').write(file.file.read())
		print(f"Archivo escrito en : {file_location}")
	return {"Archivos escritos correctamente"}

@app.get("/read")
def prepare_files():
  start = time.time()
  read_files()
  finish = time.time()
  return f"done in {finish-start} seconds"

@app.get("/merge")
def merge_files():
  start = time.time()
  merge_data()
  finish = time.time()
  return f"done in {finish-start} seconds"

@app.get("/clean")
def clean_files(max_days_before: int, init_date = None):
  start = time.time()
  clean_data(max_days_before, init_date)
  finish = time.time()
  return f"done in {finish-start} seconds"

