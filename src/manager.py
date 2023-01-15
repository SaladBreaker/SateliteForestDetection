import numpy as np
from rasterio.mask import mask
import geopandas as gpd
from .exceptions import BadShapeOfArrayException
from .base import BaseObject
import rasterio as rio


class Santinel2Manager(BaseObject):
    """
    Object Manager for Santile-2A archives

    :param source_zip_path: relative or absolute path to the zip file. The zip file
    has to be a Santile-2 archive
    :type source_zip_path: str

    Note:
    - see: https://www.indexdatabase.de/db/s-single.php?id=96 for more info on the bands
    """

    def __init__(self, source_zip_path) -> None:
        super().__init__()
        self._zip_path = source_zip_path
        self.datasetreader = self.__get_raster_reader()

        # will stop the writer in case of bad shape
        self.MAX_BANDS = 5

    def __del__(self):
        del self.datasetreader

    def __get_raster_reader(self):
        """
        Reads the Santile-2 archive as a rasterio DatasetReader.
        If the file does not exists will raise FileNotFoundException.

        DatasetReader.subdatasets will return on index:
        - 0 -> R10m
        - 1 -> R20m
        - 2 -> R60m
        """
        self.check_if_file_exists(self._zip_path)

        self.log.info(f"Reading dataset from: {self._zip_path}")
        return rio.open(self._zip_path)

    def get_R10m_reader(self):
        """
        Returns a DatasetReader that contains R10 dataset:

        Note:
        - use .tags(band_index) to see band info.
        - .read to read all the bands in an numpy.ndarray
        """
        self.log.info(f"Getting R10m for {self._zip_path}")
        return rio.open(self.datasetreader.subdatasets[0])

    def get_R20m_reader(self):
        """
        Returns a DatasetReader that contains R20 dataset:

        Note:
        - use .tags(band_index) to see band info.
        - .read to read all the bands in an numpy.ndarray
        """

        self.log.info(f"Getting R20m for {self._zip_path}")
        return rio.open(self.datasetreader.subdatasets[1])

    def get_R60m_reader(self):
        """
        Returns a DatasetReader that contains R60 dataset:

        Note:
        - use .tags(band_index) to see band info.
        - .read to read all the bands in an numpy.ndarray
        """
        self.log.info(f"Getting R60m for {self._zip_path}")
        return rio.open(self.datasetreader.subdatasets[2])

    def get_RGB(self):
        """
        Return a numpy.ndarray that contains a matrix with RGB matrix
        """
        with self.get_R10m_reader() as R10:
            # 3-b2
            # 1-b4
            # 2-b3
            b2 = R10.read(3)
            b3 = R10.read(2)
            b4 = R10.read(1)

        return np.stack((b2, b3, b4), axis=0)

    def get_NDVI(self):
        """
        Return a numpy.ndarray that contains a matrix with NDVI matrix
        """
        self.log.info("Assambling NDVI image!")
        with self.get_R10m_reader() as R10:
            b4 = R10.read(1)
            b8 = R10.read(4)

        result = (b8.astype(float) - b4.astype(float)) / (b8 + b4)
        self.log.info("Finnished assambling NDVI image!")

        return result

    def get_GNDVI(self):
        """
        Return a numpy.ndarray that contains a matrix with GNDVI matrix
        """
        self.log.info("Assambling GNDVI image!")
        with self.get_R10m_reader() as R10:
            b3 = R10.read(2)
            b8 = R10.read(4)

        result = (b8.astype(float) - b3.astype(float)) / (b8 + b3)
        self.log.info("Finnished assambling GNDVI image!")

        return result

    def get_NRGI(self):
        """
        Return a numpy.ndarray that contains a matrix with NRGI matrix
        """
        self.log.info("Assambling NRGI image!")
        with self.get_R10m_reader() as R10:
            b3 = R10.read(2)
            b4 = R10.read(1)

        result = (b4.astype(float) - b3.astype(float)) / (b4 + b3)
        self.log.info("Finnished assambling NRGI image!")

        return result

    def get_EVI2(self):
        """
        Return a numpy.ndarray that contains a matrix with EVI2 matrix
        """
        self.log.info("Assambling EVI2 image!")
        with self.get_R20m_reader() as R20:
            b5 = R20.read(1)
            b9 = R20.read(4)

        result = 2.5 * (
            (b9.astype(float) - b5.astype(float))
            / (b9.astype(float) + 2.4 * b5.astype(float) + 1)
        )
        self.log.info("Finnished assambling EVI2 image!")

        return result

    def write_image(self, image_array, meta, result_path):
        """
        Stores a single field array into a file as a photo.

        :param image_array: a numpy array that contains the image matrix
        :type image_array: numpy.ndarray

        :param meta: matadata that will be written to the image.
        Can be obtained, for example by: R10.meta (assuming that R10m bands are used to create image_array).
        Also the function will autodetect the "count" field based on the number of bands.
        :type meta: dict

        :param result_path: relative or absolute pah where the image will be stored
        :type result_path: str
        """
        # THIS IS A BUG
        self.create_dir("/".join(result_path.split("/")[:-1]))

        self.log.info(
            f"Start writting to path:{result_path} array of shape: {image_array.shape}!"
        )
        if len(image_array.shape) == 2:
            meta["count"] = 1
        else:
            meta["count"] = image_array.shape[0]

        self.log.info(f"Detected {meta['count']} bands for shape: {image_array.shape}")

        if meta["count"] > self.MAX_BANDS:
            raise BadShapeOfArrayException(
                f"Too many bands. Array shape:{image_array.shape}, MAX_BANDS: {self.MAX_BANDS}. Ex of good shape: (3, 10980, 10980)"
            )

        meta.update(driver="GTiff")
        meta.update(dtype=rio.float32)

        with rio.open(result_path, "w+", **meta) as dst:
            for band_index in range(1, meta["count"] + 1):

                if meta["count"] == 1:
                    dst.write(image_array.astype(rio.float32), band_index)
                else:
                    dst.write(image_array[band_index].astype(rio.float32), band_index)

        self.log.info(f"Finnished writting to path:{result_path}!")

    def get_NDVI_vegetation_only(self, threshold):
        """
        Function will return the NDVI image with only pixels that are bigger than the threshold
        """
        img_NDVI = self.get_NDVI()
        img_NDVI_w_dense_vegetation = np.zeros(img_NDVI.shape)

        for index_line in range(img_NDVI.shape[0]):
            for index_column in range(img_NDVI.shape[1]):

                if img_NDVI[index_line][index_column] >= threshold:
                    img_NDVI_w_dense_vegetation[index_line][index_column] = img_NDVI[
                        index_line
                    ][index_column]

                else:
                    img_NDVI_w_dense_vegetation[index_line][index_column] = 0

        return img_NDVI_w_dense_vegetation

    def crop_image(self, source, result_path, target_mask):
        """
        Function that crops an image based on a mask.

        :param source: path to source image
        :type source: str

        :param result_path: path where the cropped image will be stored
        :type result_path: str

        :param target_mask: list of tuples with the points
        :type target_mask: list of tuples
        """
        self.log.info(f"Croping: {source}!")

        target_poly_set_proj = gpd.GeoDataFrame(
            index=[0], crs="EPSG:4326", geometry=[target_mask]
        ).to_crs(
            # TODO {"init": "epsg:32634"} give Deprication Warning
            {"init": "epsg:32634"}
        )

        with rio.open(source) as src:
            out_image, out_transform = mask(
                src, target_poly_set_proj.geometry, crop=True
            )

            out_meta = src.meta.copy()
            out_meta.update(
                {
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform,
                }
            )

        with rio.open(result_path, "w", **out_meta) as dest:
            dest.write(out_image)

        self.log.info(f"Finnished cropping: {source}")
