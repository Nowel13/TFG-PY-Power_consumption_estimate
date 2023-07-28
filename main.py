import os
import time
from typing import List
from fastapi import FastAPI, UploadFile, File
from py_scripts.prepare_data.read_files import main as read_data
from py_scripts.prepare_data.merge_results import main as merge_data
from py_scripts.prepare_data.prepare_final_state import main as clean_data
from py_scripts.models.ada_boost.ada_boost_regression import main as abr
from py_scripts.models.bagging.bagging_regression import main as br
from py_scripts.models.extra_trees.extra_trees_regression import main as etr
from py_scripts.models.gradient_boosting.gradient_boosting_regression import main as gbr
from py_scripts.models.k_neighbors.k_neighbors_regression import main as knr
from py_scripts.models.linear_regression.linear_regression import main as lr
from py_scripts.models.neural_network.mlp_regression import main as mr
from py_scripts.models.radius_neighbors.radius_neighbors_regression import main as rnr
from py_scripts.models.random_forest.random_forest import main as rf
from py_scripts.models.stacking.stacking_regression import main as sr
from py_scripts.models.voting.voting_regression import main as vr

app = FastAPI()

@app.get("/")
def number_of_files():
	return { "n_files": get_n_files() }

@app.post("/file")
async def upload_file(file: UploadFile):
	file_location = 'files/' + file.filename
	with open(file_location, 'wb') as out_file:
		contents = await file.read()
		out_file.write(contents)
	return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/files")
async def upload_files(files: List[UploadFile] = File(...)):
	for file in files:
		file_location = 'files/' + file.filename
		with open(file_location, 'wb') as out_file:
			contents = await file.read()
			out_file.write(contents)
		print(f"Archivo escrito en : {file_location}")
	return {"info": "files saved correctly"}

def remove_file(path):
	# removing the file
	if not os.remove(path):
		# success message
		return f"{path} is removed successfully"
	else:
		# failure message
		return f"Unable to delete the {path}"

@app.delete("/delete")
def delete():
	response = {}
	folder_names = ["files/", "processed_files", "result_files"]
	for folder in folder_names:
		for root_folder, folders, files in os.walk(folder):
			for file in files:
				file_path = os.path.join(root_folder, file)
				response[file] = remove_file(file_path)
	return response

# @app.delete("/delete_result_files")
# def delete():
# 	for root_folder, folders, files in os.walk("processed_files/"):
# 		for file in files:
# 			file_path = os.path.join(root_folder, file)
# 			remove_file(file_path)
# 	# for root_folder, folders, files in os.walk("result_files/"):
# 	# 	for file in files:
# 	# 		file_path = os.path.join(root_folder, file)
# 	# 		remove_file(file_path)

@app.get("/read")
def read_files():
  start = time.time()
  read_data()
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

@app.get("/process")
def process_data(max_days_before: int, init_date = "2009-01-01"):
	start = time.time()
	print(init_date)
	read_data()
	merge_data()
	clean_data(max_days_before, init_date)
	finish = time.time()
	return {
		"n_files": get_n_files(),
		"message": f"Done in {finish-start} seconds",
	}

@app.post("/apply")
def apply_model(model_name: str):
	start = time.time()
	match model_name:
		case "ada_boost":
			abr()
		case "bagging":
			br()
		case "extra_trees":
			etr
		case "gradient_boosting":
			gbr()
		case "k_neighbors":
			knr()
		case "linear_regression":
			lr()
		case "neural_network":
			mr()
		case "radius_neighbors":
			rnr()
		case "random_forest":
			rf()
		case "stacking":
			sr()
		case "voting":
			vr()
		case _:
			rf()
	finish = time.time()
	response = {
		"selected": model_name,
		"time": f'Done in {finish - start} seconds',
	}
	return response

@app.get("/results")
def get_result_graphic():
	for root_folder, folders, files in os.walk("media/"):
		return { "image": files[0] }

def get_n_files():
	for root_folder, folders, files in os.walk("files/"):
		n_files = len(files)
	return n_files