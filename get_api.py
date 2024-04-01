from fastapi import FastAPI
from utils.tools import *
from item import Item

CSV_FILE = "2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv"
CSV_FILE_WITH_ADDRESS = "results_address.csv"

app = FastAPI()


@app.post('/')
async def get_network_coverage(item: Item):
    try:
        # Read CSV file
        df = read_csv(CSV_FILE_WITH_ADDRESS)
        df.fillna('', inplace=True)
        # Get city name
        city_name, postal_code = get_city_name(item.address)
        results = find_address(df, "address", city_name, postal_code)
        print(results)
        # Process the dataframe
        results_processed = process_dataframe_results(results)
        return {"item": item, "coverage": results_processed}
    except Exception as exp:
        print("Error when reading the csv file : {}.".format(exp))


input = {
    "id5": "1 Bd de Parc, 77700 Milizac-Guipronvel",
    # "id1": "157 boulevard Mac Donald 75019 Paris",
    # "id4": "5 avenue Anatole France 75007 Paris",
    # "id6": "Place d'Armes, 78000 Versailles",
    # "id7": "17 Rue René Cassin, 51430 Bezannes",
    # "id8": "78 Le Poujol, 30125 L'Estréchure"
}
