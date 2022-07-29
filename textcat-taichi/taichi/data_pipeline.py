import pandas as pd
import json
import re
import os

from collections import Counter


class DataPipeline(object):
    """
    expects path with csv or json files
    """

    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.raw_data = None

    def sample_from_csv(self, n_shot=None, random_state=0):
        """
        expects a file in csv format as follows:
        utterance, label (no headers and no index)

        Example:
        book a ticket from San Francisco to New York,en_US,Book a Flight

        returns a subsampled pandas dataframe with utterance and label columns
        if no n_shot provided, just returns the dataframe as is
        """
        df = pd.read_csv(self.data_path, names=["utterance", "label"])
        self.raw_data = df
        if n_shot is not None:
            examples_per_class = dict(Counter((df.label)))
            minimum_examples_per_class = min(examples_per_class.values())
            if minimum_examples_per_class >= n_shot:
                subsampled_df = df.groupby("label").sample(
                    n=n_shot, random_state=random_state
                )
                return subsampled_df
            else:
                error_message = "number of examples per class are not enough to sample based on n_shot={} value".format(
                    n_shot
                )
                raise Exception(error_message)
        else:
            return df

    def sample_from_json(self, n_shot=None, split="train", random_state=0):
        """
        expects a file in json format as follows:
        {split: list(list containing utterance and label)}

        Example:
        {'train':[[utterance1, label1], [utterance2, label2], ... 'test':[[...]]}

        returns a subsampled pandas dataframe with utterance and label columns
        """
        with open(self.data_path, "r") as input_json:
            self.raw_data = json.load(input_json)
        try:
            df = pd.DataFrame.from_records(
                self.raw_data[split], columns=["utterance", "label"]
            )
        except KeyError as default_error:
            error_message = "split {} not found, please select among the existing splits that exist: {}".format(
                split, list(self.raw_data.keys())
            )
            raise Exception(error_message)

        cols = list(df.columns)
        cols = cols[:1] + [cols[-1]] + cols[1:-1]
        df = df[cols]
        if n_shot is not None:
            examples_per_class = dict(Counter((df.label)))
            minimum_examples_per_class = min(examples_per_class.values())
            if minimum_examples_per_class >= n_shot:
                subsampled_df = df.groupby("label").sample(
                    n=n_shot, random_state=random_state
                )
                return subsampled_df
            else:
                error_message = "number of examples per class are not enough to sample based on n_shot={} value".format(
                    n_shot
                )
                raise Exception(error_message)
        else:
            return df

    def save_subsampled_data_to_csv(
        self,
        save_dir,
        n_shot=None,
        split="train",
        is_json=False,
        random_state=0,
        save_filename=None,
    ):
        """
        saves the subsampled data from csv/json into csv with utterance and label columns with no headers and no index in the requisite
        save directory
        """
        if is_json:
            subsampled_df = self.sample_from_json(
                n_shot=n_shot, split=split, random_state=random_state
            )
        else:
            subsampled_df = self.sample_from_csv(
                n_shot=n_shot, random_state=random_state
            )

        os.makedirs(save_dir, exist_ok=True)
        if save_filename is None:
            save_path = os.path.join(
                save_dir, self.name + "_" + str(n_shot) + "_shot_" + split + ".csv"
            )
        else:
            save_path = os.path.join(save_dir, save_filename)

        subsampled_df.to_csv(save_path, header=None, index=None)

    def save_subsampled_data_to_json(
        self,
        save_dir,
        n_shot=None,
        split="train",
        is_json=False,
        random_state=0,
        orient="values",
        save_filename=None,
    ):
        """
        saves the subsampled data from csv/json into json with individual utterance and label values as an independent array in the requisite
        save directory
        """
        if is_json:
            subsampled_df = self.sample_from_json(
                n_shot=n_shot, split=split, random_state=random_state
            )
        else:
            subsampled_df = self.sample_from_csv(
                n_shot=n_shot, random_state=random_state
            )

        os.makedirs(save_dir, exist_ok=True)
        if save_filename is None:
            save_path = os.path.join(
                save_dir, self.name + "_" + str(n_shot) + "_shot_" + split + ".json"
            )
        else:
            save_path = os.path.join(save_dir, save_filename)

        subsampled_df.to_json(save_path, orient=orient)
