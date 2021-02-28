from src.settings.credentials import AUTH
from sentinelsat import SentinelAPI
from shapely.geometry import Point, Polygon

from src.base import BaseObject


class Santinel2Dumper(BaseObject):
    def __init__(self) -> None:
        super().__init__()
        self.api_client = self.__get_api_client()

    def __get_api_client(self):
        return SentinelAPI(
            AUTH["USERNAME"], AUTH["PASSWORD"], "https://scihub.copernicus.eu/dhus"
        )

    def get_products_from_query(
        self,
        footprint,
        date_range,
        processinglevel="Level-2A",
        cloudcoverpercentage=(0, 10),
    ):
        """
        Function used for searching available data for a footprint

        :param footprint: A Polygon that contains the targeted area
        :type footprint: shapely.geometry.Polygon

        :param date_range: data range for the desired zone
        :type date_range: tuple of form: ('YYYYMMDD','YYYYMMDD')

        :param processinglevel: processing level of the image, default: "Level-2A"
        :type processinglevel: str

        :param cloudcoverpercentage: specify the allowed cloude coverage. Default: (0,10)
        :type cloudcoverpercentage: tuple of percentages. Ex: (0,10)

        :return: A GeoDataframe containing availabe data for the queries
        :return type: geopandas.GeoDataframe
        """
        products = self.api_client.query(
            footprint,
            date=date_range,
            platformname="Sentinel-2",
            processinglevel=processinglevel,
            cloudcoverpercentage=cloudcoverpercentage,
        )

        return self.api_client.to_geodataframe(products)

    def download_satelite_data(self, target_uuid, downlaod_dir, checksum=True):
        """
        Downloads the .zip file for the specified target_uuid

        :param target_uuid: uuid of the archive (Can be obtained from the query function)
        :type target_uuid: str

        :param downlaod_dir: target dir of the zip file
        :type downlaod_dir: str

        :param checksum: apply checksum after download. Default: true
        :type checksum: boolean
        """
        self.log.info(f"Starting downloading for: {target_uuid}")
        self.api_client.download(
            target_uuid, directory_path=downlaod_dir, checksum=checksum
        )
        self.log.info(f"Finished downlaod for: {target_uuid}")
