
import pandas as pd
import numpy as np
import os

class LoadRawCsv :

    def __init__(self, raw_datafile):

        if os.path.exists(raw_datafile) : #and \".csv\" == raw_datafile[-4:]:

            self.rawdata = raw_datafile
        else :
            self.rawdata = None

        self.dataframe = None

        self.features_all = None
        self.result_features = None

        # the common features per patient
        self.features_common = None

        # the unique features for each measurement and each patient
        self.features_results= None

        # all the measurements for each patient
        self.measure_type = None

        self.patients_id = None

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
        ----------------------
        :param id_feature: the patient unique identifier
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

    def process_resultf(self, result_f="", measurements=[], patients_num=0, units=None):
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
            result_values = self.dataframe[result_f].values

            result_values = np.reshape(result_values, (patients_num, len(measurements) ))

            print(result_values.shape)

            for i in range(len(measurements)) :
                self.dataframe_clean[self.measure_newtype[i]] = result_values[:, i]
        else :
            pass

    def measure_newf(self, measure_type, units):
        newf = []
        for f, u in zip(measure_type, units):
            newf.append("R_".join(f.split(",")) + "_" + u)

        self.measure_newtype = newf

    def save_results(self, output="cleaned_dataset.csv"):
        '''
        save the processed dataset to a new file
        ----------------------
        :param output:
        :return:
        '''

        self.dataframe_clean.to_csv(output, header=True, sep=",", encoding="GBK", index=False)

    def groupping(self, group_infor=[]):

        self.dataframe_clean["Group"] = group_infor





