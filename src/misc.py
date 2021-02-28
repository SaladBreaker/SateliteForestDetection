import folium
import geopandas as gpd
from src.base import BaseObject
from shapely.geometry import Polygon


class MapManager(BaseObject):
    """
    Class used for displaying shapes on map
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_map_with_target(target_polygon, zoom=14):

        target_poly_set = gpd.GeoDataFrame(
            index=[0], crs="EPSG:4326", geometry=[Polygon(target_polygon)]
        )
        m = folium.Map(MapManager.__get_map_center(target_polygon), zoom_start=zoom)
        folium.GeoJson(target_poly_set).add_to(m)
        return m

    @staticmethod
    def __get_map_center(target_polygon):
        return (
            sum([p[1] for p in target_polygon]) / len(target_polygon),
            sum([p[0] for p in target_polygon]) / len(target_polygon),
        )
