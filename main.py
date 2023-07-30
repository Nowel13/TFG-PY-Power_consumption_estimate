import os
import time
import pandas as pd
from zipfile import ZipFile
from typing import List, Dict, Any
from starlette.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from py_scripts.general_model import main as predict
from py_scripts.prepare_data.merge_results import main as merge_data
from py_scripts.prepare_data.read_files import get_file as save_data
from py_scripts.prepare_data.read_files import read_files as read_data
from py_scripts.prepare_data.prepare_final_state import main as clean_data

app = FastAPI()

# Devuelve el número de ficheros que se hayan subido a la API:
@app.get("/")
def number_of_files():
	return { "n_files": get_n_files() }

# Permite subir y guardar un único fichero a la API:
@app.post("/upload_file")
async def upload_file(file: UploadFile):
	file_location = 'data/files/' + file.filename
	with open(file_location, 'wb') as out_file:
		contents = await file.read()
		out_file.write(contents)
	return {"info": f"file '{file.filename}' saved at '{file_location}'"}

# Versión para recibir los archivos directamente y almacenarlos en disco para su 
# posterior procesamiento:
@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
	for file in files:
		file_location = 'data/files/' + file.filename
		with open(file_location, 'wb') as out_file:
			contents = await file.read()
			out_file.write(contents)
		print(f"Archivo escrito en : {file_location}")
	return {"info": "files saved correctly"}

# Versión más rápida, recibe los archivos ya procesados desde el front
# pero tarda muchísimo menos:
@app.post("/upload_processed_files")
async def upload__processed_files(files: List[Dict[str, Any]]):
	save_data(files)
	return {"info": "files saved correctly"}

# Permite eliminar todos los archivos subidos y procesados para poder
# comenzar de nuevo:
@app.delete("/delete")
def delete():
	response = {}
	folder_names = ["data/files", "data/processed_files", "data/final_files", "data/results", "data/zip"]
	for folder in folder_names:
		for root_folder, folders, files in os.walk(folder):
			for file in files:
				file_path = os.path.join(root_folder, file)
				response[file] = remove_file(file_path)
	return response

# En caso de tener los archivos almacenados en disco sin procesar, este
# método los procesa y almacena en processed_files/:
@app.get("/read")
def read_files():
  start = time.time()
  read_data()
  finish = time.time()
  return f"done in {finish-start} seconds"

# Permite unificar los archivos de datos procesados en uno sólo para su
# posterior uso:
@app.get("/merge")
def merge_files():
  start = time.time()
  merge_data()
  finish = time.time()
  return f"done in {finish-start} seconds"

# Termina de limpiar y preparar los datos unificados, para el estudio:
@app.get("/clean")
def clean_files(max_days_before: int, init_date = None):
  start = time.time()
  clean_data(max_days_before, init_date)
  finish = time.time()
  return f"done in {finish-start} seconds"

# Unifica, limpia y prepara los datos para el estudio, pero con una
# única llamada:
@app.get("/process")
def process_data(max_days_before: str, init_date = "2009-01-01"):
	start = time.time()
	merge_data()
	clean_data(int(max_days_before), init_date)
	finish = time.time()
	return {
		"n_files": get_n_files(),
		"message": f"Done in {finish-start} seconds",
	}

# Aplica el modelo elegido y con los parámetros establecidos:
@app.post("/apply_model")
def apply_model(model_name: str):
	start = time.time()
	predict(model_name)
	finish = time.time()
	response = {
		"selected": model_name,
		"time": round(finish - start, 2),
	}
	return response

# Devuelve dos archivos, uno con el dataframe que contiene los resultados
# de las predicciones y otro con la gráfica resultante:
@app.get("/results")
def get_result_graphic():
	response = {}
	for root_folder, folders, files in os.walk("data/results/"):
		with ZipFile('data/zip/files.zip', 'w') as zipF:
			for file in files:
				zipF.write(f"data/results/{file}")
	return FileResponse('data/zip/files.zip', media_type='application/octet-stream')


####################################
####### FUNCIONES AUXILIARES #######
####################################

# Permite indicar el número de archivos que hay subidos a la API actualmente:
def get_n_files():
	for root_folder, folders, files in os.walk("data/processed_files/"):
		n_files = len(files)
	return n_files

# Elimina el archivo que se le pase por parámetro:
def remove_file(path):
	if not os.remove(path):
		return f"{path} is removed successfully"
	else:
		return f"Unable to delete the {path}"
