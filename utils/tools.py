from pyproj import Transformer
import pandas as pd
import csv as cs
import requests

API_REVERSE_GOUV = "https://api-adresse.data.gouv.fr/reverse/"


def lamber93_to_gps(x, y):
    """Transform x,y to lat,long

    Args:
        x (float): The x coordinate to transform
        y (float): the y coordinate to transform

    Returns:
        float, float: The (lat, long) coordinates
    """
    lambert_epsg = "2154"
    wgs84_epsg = "4326"
    transformer = Transformer.from_crs(lambert_epsg, wgs84_epsg)
    transform = transformer.transform(x, y)
    lat, long = float(transform[0]), float(transform[1])
    return lat, long


def read_csv(csv_file):
    return pd.read_csv(csv_file,
                       sep=",",
                       dtype=str,
                       encoding='utf-8-sig',
                       quoting=cs.QUOTE_NONE)


def find_address(dataframe, column_to_search, city_name, postal_code):
    """Find the address with the postal_code and the cityname.
    For example, search ...75012 Paris in 10 rue de l'espérance 7501 Paris.

    Args:
        dataframe (Dataframe): The dataframe where to search
        column_to_search (str): The column name in the df to search
        city_name (str): The city name
        postal_code (str): The postal code

    Returns:
        Dataframe: Get the dataframe results of the search
    """
    dataframe["Indexes"] = dataframe[column_to_search].str.endswith(
        "{} {}".format(postal_code, city_name))
    results = dataframe[dataframe["Indexes"] > 0]
    return results


def get_adresse_from_coordinates(row):
    """Get the address from the row of a dataframe.

    Args:
        row (row): The row of dataframe

    Raises:
        Exception: If the query can't get the address from the API GOUV URL.

    Returns:
        str: The address from the row.
    """
    if row["x"] is not None and row["y"] is not None:
        lat, long = lamber93_to_gps(int(row["x"]), int(row["y"]))
        try:
            results = requests.get(
                API_REVERSE_GOUV +
                "?lon={}&lat={}&type=street".format(long, lat))
            if results.status_code == 200:
                return process_api_reverse_query(results.json())
            return ""
        except Exception as exp:
            raise Exception(
                "Can't get the results from the {} URL : {}".format(
                    API_REVERSE_GOUV, str(exp)))


def process_api_reverse_query(results_content):
    """Process the data coming from the API query and get the result of the adress from the results content

    Args:
        results_content (json): The JSON response from the requests query

    Returns:
        str: The address. None if no adress founded.
    """
    if "features" in results_content and len(results_content["features"]):
        # Get the first result as it's the best geolocation
        result = results_content["features"][0]["properties"]
        if "label" in result:
            return result["label"]
    return None


def process_dataframe_results(df):
    dict_to_return = {}

    # Get results like from dataframe records:
    # [{
    #         'Operateur': "SFR",
    #         '2G': 1,
    #         '3G': 1,
    #         '4G': 0
    #     }, {
    #         'Operateur': 'Orange',
    #         '2G': 0,
    #         "3G": 1,
    #         "4G": 1
    #     }]
    dict_records = df.to_dict('records')
    for d in dict_records:
        dict_ = {
            d["Operateur"]: {
                "2G": d["2G"] == "1",
                "3G": d["3G"] == "1",
                "4G": d["4G"] == "1"
            }
        }
        dict_to_return.update(dict_)
    return dict_to_return


def get_city_name(address):
    """Get the city name from address. For example get "Paris" from 157 boulevard Mac Donald 75019 Paris

    Args:
        address (str): The address

    Returns:
        str: The city name
    """
    split_address = address.split()
    return split_address[-1], split_address[-2]
