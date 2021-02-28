import os, zipfile
import threading
import zipfile
import folium
import threading
import shutil
import geopandas as gpd

import app.exceptions as exceptions


def thread_function(func, args_list):
    """
    args_list has to list of tuples
    """
    threads = []
    for args in args_list:
        threads.append(threading.Thread(target=func, args=args))
        threads[-1].start()

    for t in threads:
        t.join()


def get_config(targets, DOWNLOAD_PATH, RESULTS_PATH):
    return {
        "old": {
            "level": "L2A",
            "orbit_no": targets.iloc[0].orbitnumber,
            "begin_time": targets.iloc[0].beginposition.strftime("%Y%m%dT%H%M%S"),
            "source_file_path": f"{DOWNLOAD_PATH}/{targets.iloc[0].identifier}.zip",
            "source_folder_path": f"{DOWNLOAD_PATH}/{targets.iloc[0].identifier}.SAFE",
            "RGB": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/RBG.tiff",
            "cropped_RGB": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/cropped_RBG.tif",
            "NDVI": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/NDVI.tiff",
            "cropped_NDVI": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/cropped_NDVI.tif",
            "GNDVI": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/GNDVI.tiff",
            "cropped_GNDVI": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/cropped_GNDVI.tif",
            "NRGI": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/NRGI.tiff",
            "cropped_NRGI": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/cropped_NRGI.tif",
            "EVI2": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/EVI2.tiff",
            "cropped_EVI2": f"{RESULTS_PATH}/{targets.iloc[0].identifier}/cropped_EVI2.tif",
        },
        "new": {
            "level": "L2A",
            "orbit_no": targets.iloc[1].orbitnumber,
            "begin_time": targets.iloc[1].beginposition.strftime("%Y%m%dT%H%M%S"),
            "source_file_path": f"{DOWNLOAD_PATH}/{targets.iloc[1].identifier}.zip",
            "source_folder_path": f"{DOWNLOAD_PATH}/{targets.iloc[1].identifier}.SAFE",
            "RGB": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/RBG.tiff",
            "cropped_RGB": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/cropped_RBG.tif",
            "NDVI": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/NDVI.tiff",
            "cropped_NDVI": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/cropped_NDVI.tif",
            "GNDVI": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/GNDVI.tiff",
            "cropped_GNDVI": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/cropped_GNDVI.tif",
            "NRGI": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/NRGI.tiff",
            "cropped_NRGI": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/cropped_NRGI.tif",
            "EVI2": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/EVI2.tiff",
            "cropped_EVI2": f"{RESULTS_PATH}/{targets.iloc[1].identifier}/cropped_EVI2.tif",
        },
    }
