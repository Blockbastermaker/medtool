
import pandas as pd
import numpy as np
import os
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
import xlrd

class LoadRawCsv :

    def __init__(self, raw_datafile):

        if os.path.exists(raw_datafile) : #and \".csv\" == raw_datafile[-4:]:

            self.rawdata = raw_datafile
        else :
            self.rawdata = None

        # the dataset
        self.dataframe = None

        # all the features
        self.features_all = None
        self.result_features = None

        # the common features per patient
        self.features_common = None

        # the unique features for each measurement and each patient
        self.features_results= None

        # all the measurements for each patient
        self.measure_type = None

        # the unique patient identifier
        self.patients_id = None

        # the units of the measurement
        self.units = None

    def loadraw(self, delimiter="\t", encoding="GBK"):
        '''
        Note: GBK is a Simplified Chinese Character Set
        https://en.wikipedia.org/wiki/GBK_(character_encoding)
        ----------------------
        Parameter
        :param delimiter: str, the separate spacer
        :param encoding: str, the encoding method. For simplified Chinese, it is GBK.
        :return:
        '''

        self.dataframe = pd.read_csv(self.rawdata, sep=delimiter, encoding=encoding)

        self.features_all = self.dataframe.columns

    def measurements(self, measure_feature = '结果'):

        '''
        get the measurements required for each patient
        ----------------------
        :param measure_feature: str, the result colunmn name
        :return:
        '''

        self.measure_type = self.dataframe[measure_feature].unique()

    def patients(self, id_feature=None):
        '''
        get the patient unique identifier, or say ID number
        ----------------------
        :param id_feature: str, the patient unique identifier
        :return:
        '''
        self.patients_id = self.dataframe[id_feature].unique()

    def get_units(self, unit_feature=None):

        self.units = self.dataframe[unit_feature].values[:len(self.measure_type)]

class DataSetClean :

    def __init__(self, dataframe_raw):
        '''
        ----------------------
        :param dataframe_raw: pd.DataFrame, the object hold the raw input data file
        '''
        # raw data set
        self.dataframe = dataframe_raw

        # the features that are to be saved to a new file
        self.features_tosave = None

        # the cleaned dataset
        self.dataframe_clean = pd.DataFrame()

        self.feature_id = None

        self.measure_newtype = None

    def process_commonf(self, features=None):
        '''
        add the common feature information to the cleaned dataset (pd.DataFrame)
        ----------------------
        :param features: list, the common feature names that are unique for each patient
        :return:
        '''

        self.dataframe_clean[features] = \
            self.dataframe[features].drop_duplicates(subset=None,
                                                     keep='first',
                                                     inplace=False)
        print(np.arange(self.dataframe_clean.shape[0]))
        self.dataframe_clean.reindex(index=np.arange(self.dataframe_clean.shape[0]))

    def process_resultf(self, measuretype_f = "", result_f="", measurements=[],):
        '''
        add the measurements to the cleaned dataset (pd.DataFrame)
        ----------------------
        :param result_f: str, the "Result" column name which holds the measurement values
        :param measurements: list, the measurement types
        :param patients_num: int, number of patients in the dataset
        :param units: list, the units for each of the measurement types
        :return:
        '''

        if len(measurements) :
            for m in measurements :
                val = self.dataframe[self.dataframe[measuretype_f] == m ][result_f].values
                self.dataframe_clean[m] = val
        else :
            pass

    def measure_newf(self, measure_type, units):
        '''
        for the measurement types, now give them new names
        ---------------------
        :param measure_type: list, original measurement types
        :param units: list, the units of the measurement
        :return:
        '''
        newf = []
        for f, u in zip(measure_type, units):
            newf.append("R_".join(f.split(",")) + "_" + u)

        self.measure_newtype = newf

    def save_results(self, output="cleaned_dataset.csv", encoding="utf_8_sig"):
        '''
        save the processed dataset to a new file
        ----------------------
        :param output: str, output csv file
        :param encoding: str, encoding methods, default is utf_8_sig
        :return:
        '''

        self.dataframe_clean.to_csv(output, header=True, sep=",", encoding=encoding, index=False)

    def groupping(self, group_infor=[]):
        '''
        add groupping information to the dataset
        ---------------------
        :param group_infor:
        :return:
        '''

        self.dataframe_clean["Group"] = group_infor

    def add_features(self, feature_name, feature_values):
        '''
        add a feature into the the dataframe
        ---------------------
        :param feature_name:
        :param feature_values:
        :return:
        '''
        self.dataframe_clean[feature_name] = feature_values

class LoadQPCRData :

    def __init__(self, input):

        self.fn = input
        self.df = self.loadDataFile()

        self.features_all = self.df.columns

        self.lineIndex = self.line_index()

    def loadDataFile(self, header_index=6):
        '''
        load files
        ----------------------
        :param header_index: int, the index of the header line
        :return: pd.DataFrame
        '''

        return pd.read_excel(self.fn, header=header_index)

    def line_index(self, start=2, dt=4):
        '''
        get only partial of the dataframe,
        keep only some lines using dt and start
        ----------------------
        :param start: int, the starting line index
        :param dt: int, delta (or gap) between lines
        :return: np.array
        '''
        return np.array(self.df[self.features_all[0]][start::dt].index)

    def getLine_by_index(self, index):
        '''
        subset a dataframe by index
        ----------------------
        :param index: np.array
        :return: pd.DataFrame
        '''

        return self.df.iloc[index]



