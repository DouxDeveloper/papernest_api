import pandas as pd
import csv as cs
from utils.tools import *
import luigi
from luigi import Task, LocalTarget
from luigi.format import UTF8

CSV_FILE = "2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv"
OUTPUT_FILE_NAME = "results_address.csv"


class CSVFileHandler(Task):
    # CSV file as luigi parameter
    csv_file = luigi.Parameter()

    def output(self):
        return LocalTarget(OUTPUT_FILE_NAME, format=UTF8)

    def run(self):
        print("Running processing file task ...")
        # Read the CSV file
        self.dataframe = read_csv(self.csv_file)
        # # Add address column in the dataframe
        self.set_df_address()
        # # Get output
        self.dataframe.to_csv(self.output().path,
                              sep=',',
                              index=False,
                              encoding='utf-8',
                              header=True)

    def crate_csv_file(self, csv_file_name):
        """Create a CSV file from the dataframe content

        Args:
            csv_file_name (str): The CSV file name
            df_content (Dataframe): The dataframe content to add to CSV file
        """
        self.dataframe.to_csv(csv_file_name,
                              sep=',',
                              index=False,
                              encoding='utf-8',
                              header=True)

    def set_df_address(self):
        self.dataframe["address"] = self.dataframe.apply(
            get_adresse_from_coordinates, axis=1)


if __name__ == '__main__':
    luigi.build([CSVFileHandler(csv_file=CSV_FILE)])
