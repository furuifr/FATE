#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import functools
import math

from arch.api.utils import log_utils
from federatedml.feature.quantile_summaries import QuantileSummaries
from federatedml.statistic.data_overview import get_header
# from federatedml.statistic.statics import MultivariateStatisticalSummary

LOGGER = log_utils.getLogger()


class IVAttributes(object):
    def __init__(self, woe_array, iv_array, event_count_array, non_event_count_array,
                 event_rate_array, non_event_rate_array, split_points=None, iv=None):
        self.woe_array = woe_array
        self.iv_array = iv_array
        self.event_count_array = event_count_array
        self.non_event_count_array = non_event_count_array
        self.event_rate_array = event_rate_array
        self.non_event_rate_array = non_event_rate_array
        if split_points is None:
            self.split_points = []
        else:
            self.split_points = split_points

        if iv is None:
            iv = 0
            for idx, woe in enumerate(self.woe_array):
                non_event_rate = non_event_count_array[idx]
                event_rate = event_rate_array[idx]
                iv += (non_event_rate - event_rate) * woe
        self.iv = iv

    @property
    def is_woe_monotonic(self):
        """
        Check the woe is monotonic or not
        """
        woe_array = self.woe_array
        if len(woe_array) <= 1:
            return True

        is_increasing = all(x <= y for x, y in zip(woe_array, woe_array[1:]))
        is_decreasing = all(x >= y for x, y in zip(woe_array, woe_array[1:]))
        return is_increasing or is_decreasing

    @property
    def bin_nums(self):
        return len(self.woe_array)

    def result_dict(self):
        save_dict = self.__dict__
        save_dict['is_woe_monotonic'] = self.is_woe_monotonic
        save_dict['bin_nums'] = self.bin_nums
        return save_dict

    def display_result(self, display_results):
        save_dict = self.result_dict()
        dis_str = ""
        for d_s in display_results:
            dis_str += "{} is {};\n".format(d_s, save_dict.get(d_s))
        return dis_str

    def reconstruct(self, iv_obj):
        self.woe_array = list(iv_obj.woe_array)
        self.iv_array = list(iv_obj.iv_array)
        self.event_count_array = list(iv_obj.event_count_array)
        self.non_event_count_array = list(iv_obj.non_event_count_array)
        self.event_rate_array = list(iv_obj.event_rate_array)
        self.non_event_rate_array = list(iv_obj.non_event_rate_array)
        self.split_points = dict(iv_obj.split_points)
        for key, values in self.split_points.items():
            values = list(values)
            self.split_points[key] = values

        self.iv = iv_obj.iv


class Binning(object):
    """
    This is use for discrete data so that can transform data or use information for feature selection.

    Parameters
    ----------
    param : FeatureBinningParam object,
            Parameters that user set.

    Attributes
    ----------
    cols_dict: dict
        Record key, value pairs where key is cols' name, and value is cols' index. This is use for obtain correct
        data from a data_instance

    """

    def __init__(self, params):
        self.params = params
        self.bin_num = params.bin_num
        self.cols = params.cols
        self.cols_dict = {}

    def fit_split_points(self, data_instances):
        """
        Get split points

        Parameters
        ----------
        data_instances : DTable
            The input data

        Returns
        -------

        split_points : dict.
            Each value represent for the split points for a feature. The element in each row represent for
            the corresponding split point.
            e.g.
            split_points = {'x1': [0.1, 0.2, 0.3, 0.4 ...],    # The first feature
                            'x2': [1, 2, 3, 4, ...],           # The second feature
                            ...]                         # Other features

        """
        raise NotImplementedError("Should not call this class directly")

    def _init_cols(self, data_instances):
        header = get_header(data_instances)
        if self.cols == -1:
            self.cols = header

        self.cols_dict = {}
        for col in self.cols:
            col_index = header.index(col)
            self.cols_dict[col] = col_index

    def transform(self, data_instances, split_points=None):
        """
        Apply the binning method

        Parameters
        ----------
        data_instances : DTable
            The input data

        split_points : dict.
            Each value represent for the split points for a feature. The element in each row represent for
            the corresponding split point.
            e.g.
            split_points = {'x1': [0.1, 0.2, 0.3, 0.4 ...],    # The first feature
                            'x2': [1, 2, 3, 4, ...],           # The second feature
                            ...]                         # Other features

        Returns
        -------
        data_bin_table : DTable.

            Each element represent for the corresponding bin number this feature belongs to.
            e.g. it could be:
            [{'x1': 1, 'x2': 5, 'x3': 2}
            ...
             ]
        """
        self._init_cols(data_instances)

        if split_points is None:
            split_points = self.fit_split_points(data_instances)

        f = functools.partial(self.bin_data,
                              split_points=split_points,
                              cols_dict=self.cols_dict)
        data_bin_dict = data_instances.mapValues(f)
        return data_bin_dict

    def cal_local_iv(self, data_instances, split_points=None, label_table=None):
        """
        Calculate iv attributes

        Parameters
        ----------
        data_instances : DTable
            The input data

        split_points : dict.
            Each value represent for the split points for a feature. The element in each row represent for
            the corresponding split point.
            e.g.
            split_points = {'x1': [0.1, 0.2, 0.3, 0.4 ...],    # The first feature
                            'x2': [1, 2, 3, 4, ...],           # The second feature
                            ...]                         # Other features

        label_table : DTable
            id with labels

        Returns
        -------
        Dict of IVAttributes object

        """
        self._init_cols(data_instances)

        if split_points is None:
            split_points = self.fit_split_points(data_instances)

        data_bin_table = self.transform(data_instances, split_points)
        if label_table is None:
            label_table = data_instances.mapValues(lambda x: x.label)
        event_count_table = label_table.mapValues(lambda x: (x, 1 - x))
        data_bin_with_label = data_bin_table.join(event_count_table, lambda x, y: (x, y))
        f = functools.partial(self.add_label_in_partition,
                              total_bin=self.bin_num,
                              cols_dict=self.cols_dict)

        result_sum = data_bin_with_label.mapPartitions(f)
        result_counts = result_sum.reduce(self.aggregate_partition_label)

        iv_attrs = self.cal_iv_woe(result_counts,
                                   self.params.adjustment_factor,
                                   split_points=split_points)
        return iv_attrs

    @staticmethod
    def bin_data(instance, split_points, cols_dict):
        """
        Apply the binning method

        Parameters
        ----------
        instance : DTable
            The input data

        split_points : dict.
            Each value represent for the split points for a feature. The element in each row represent for
            the corresponding split point.
            e.g.
            split_points = {'x1': [0.1, 0.2, 0.3, 0.4 ...],    # The first feature
                            'x2': [1, 2, 3, 4, ...],           # The second feature
                            ...]                         # Other features

        cols_dict: dict
            Record key, value pairs where key is cols' name, and value is cols' index.

        Returns
        -------
        result_bin_dict : dict.
            Each element represent for the corresponding bin number this feature belongs to.
            e.g. it could be:
            [{'x1': 1, 'x2': 5, 'x3': 2}
            ...
             ]  # Each number represent for the bin number it belongs to.
        """

        result_bin_nums = {}
        for col_name, col_index in cols_dict.items():
            col_split_points = split_points[col_name]

            value = instance.features[col_index]

            col_bin_num = len(col_split_points)
            for bin_num, split_point in enumerate(col_split_points):
                if value < split_point:
                    col_bin_num = bin_num
                    break
            result_bin_nums[col_name] = col_bin_num
        # result_bin_nums = tuple(result_bin_nums)
        return result_bin_nums

    @staticmethod
    def woe_1d(data_event_count, adjustment_factor, split_points):
        """
        Given event and non-event count in one column, calculate its woe value.

        Parameters
        ----------
        data_event_count : list
            [(event_sum, non-event_sum), (same sum in second_bin), (in third bin) ...]

        adjustment_factor : float
            The adjustment factor when calculating WOE

        split_points : list
            For this specific column, its split_points for each bin.

        Returns
        -------
        IVAttributes : object
            Stored information that related iv and woe value
        """
        event_total = 0
        non_event_total = 0
        for event_sum, non_event_sum in data_event_count:
            event_total += event_sum
            non_event_total += non_event_sum
        # LOGGER.debug("In woe_1d func, data_event_count is {}, event_total: {}, non_event_total: {}".format(
        #     data_event_count, event_total, non_event_total
        # ))
        if event_total == 0:
            raise ValueError("NO event label in target data")
        if non_event_total == 0:
            raise ValueError("NO non-event label in target data")

        iv = 0
        event_count_array = []
        non_event_count_array = []
        event_rate_array = []
        non_event_rate_array = []
        woe_array = []
        iv_array = []

        for event_count, non_event_count in data_event_count:
            if event_count == 0 and non_event_count == 0:
                continue
            if event_count == 0 or non_event_count == 0:
                event_rate = 1.0 * (event_count + adjustment_factor) / event_total
                non_event_rate = 1.0 * (non_event_count + adjustment_factor) / non_event_total
            else:
                event_rate = 1.0 * event_count / event_total
                non_event_rate = 1.0 * non_event_count / non_event_total
            woe_i = math.log(non_event_rate / event_rate)

            event_count_array.append(event_count)
            non_event_count_array.append(non_event_count)
            event_rate_array.append(event_rate)
            non_event_rate_array.append(non_event_rate)
            woe_array.append(woe_i)
            iv_i = (non_event_rate - event_rate) * woe_i
            iv_array.append(iv_i)
            iv += iv_i
        return IVAttributes(woe_array=woe_array, iv_array=iv_array, event_count_array=event_count_array,
                            non_event_count_array=non_event_count_array, split_points=split_points,
                            event_rate_array=event_rate_array, non_event_rate_array=non_event_rate_array, iv=iv)

    @staticmethod
    def cal_iv_woe(result_counts, adjustment_factor, split_points=None):
        """
        Given event count information calculate iv information

        Parameters
        ----------
        result_counts: DTable.
            It is like:
                {'x1': [[event_count, non_event_count], [event_count, non_event_count] ... ],
                 'x2': [[event_count, non_event_count], [event_count, non_event_count] ... ],
                 ...
                }

        adjustment_factor : float
            The adjustment factor when calculating WOE

        split_points : dict
            split_points = {'x1': [0.1, 0.2, 0.3, 0.4 ...],    # The first feature
                            'x2': [1, 2, 3, 4, ...],           # The second feature
                            ...]                         # Other features

        Returns
        -------
        Dict of IVAttributes object
            {'x1': attr_obj,
             'x2': attr_obj
             ...
             }
        """
        result_ivs = {}
        for col_name, data_event_count in result_counts.items():
            if split_points is not None:
                feature_split_point = split_points[col_name]
            else:
                feature_split_point = None
            result_ivs[col_name] = Binning.woe_1d(data_event_count, adjustment_factor, feature_split_point)
        return result_ivs

    @staticmethod
    def add_label_in_partition(data_bin_with_table, total_bin, cols_dict, encryptor=None):
        """
        Add all label, so that become convenient to calculate woe and iv

        Parameters
        ----------
        data_bin_with_table : DTable
            The input data, the DTable is like:
            (id, {'x1': 1, 'x2': 5, 'x3': 2}, y, 1 - y)

        total_bin : int, > 0
            Specify the largest bin number

        cols_dict: dict
            Record key, value pairs where key is cols' name, and value is cols' index.

        encryptor: Paillier Object
            If encryptor is not None, y and 1-y is indicated to be encrypted and will initialize 0 with encryption.

        Returns
        -------
        result_sum: the result DTable. It is like:
            {'x1': [[event_count, non_event_count], [event_count, non_event_count] ... ],
             'x2': [[event_count, non_event_count], [event_count, non_event_count] ... ],
             ...
            }

        """
        result_sum = {}
        for col_name in cols_dict:
            result_col_sum = []
            for bin_index in range(total_bin):
                if encryptor is not None:
                    result_col_sum.append([encryptor.encrypt(0), encryptor.encrypt(0)])
                else:
                    result_col_sum.append([0, 0])
            result_sum[col_name] = result_col_sum  # {'x1': [[0, 0], [0, 0] ... ],...}

        for _, datas in data_bin_with_table:
            bin_idx_dict = datas[0]
            y_combo = datas[1]
            # LOGGER.debug("In data_bin_with_table loop, bin_idxs: {}, y: {}, inverse_y: {}".format(
            #     bin_idxs, y_combo[0], y_combo[1]
            # ))
            y = y_combo[0]
            inverse_y = y_combo[1]
            for col_name, bin_idx in bin_idx_dict.items():
                col_sum = result_sum[col_name]
                label_sum = col_sum[bin_idx]
                label_sum[0] = label_sum[0] + y
                label_sum[1] = label_sum[1] + inverse_y
                col_sum[bin_idx] = label_sum
                result_sum[col_name] = col_sum

        return result_sum

    @staticmethod
    def aggregate_partition_label(sum1, sum2):
        """
        Used in reduce function. Aggregate the result calculate from each partition.

        Parameters
        ----------
        sum1 :  DTable.
            It is like:
                {'x1': [[event_count, non_event_count], [event_count, non_event_count] ... ],
                 'x2': [[event_count, non_event_count], [event_count, non_event_count] ... ],
                 ...
                }

        sum2 : DTable
            Same as sum1
        Returns
        -------
        Merged sum. The format is same as sum1.

        """
        if sum1 is None and sum2 is None:
            return None

        if sum1 is None:
            return sum2

        if sum2 is None:
            return sum1

        new_result = {}
        for col_name, count_sum1 in sum1.items():
            count_sum2 = sum2[col_name]
            tmp_list = []
            for idx, label_sum1 in enumerate(count_sum1):
                label_sum2 = count_sum2[idx]
                tmp = (label_sum1[0] + label_sum2[0], label_sum1[1] + label_sum2[1])
                tmp_list.append(tmp)
            new_result[col_name] = tmp_list
        return new_result


class QuantileBinning(Binning):
    """
    After quantile binning, the numbers of elements in each binning are equal.

    The result of this algorithm has the following deterministic bound:
    If the data_instances has N elements and if we request the quantile at probability `p` up to error
    `err`, then the algorithm will return a sample `x` from the data so that the *exact* rank
    of `x` is close to (p * N).
    More precisely,

    {{{
      floor((p - 2 * err) * N) <= rank(x) <= ceil((p + 2 * err) * N)
    }}}

    This method implements a variation of the Greenwald-Khanna algorithm (with some speed
    optimizations).
    """

    def __init__(self, params):
        super(QuantileBinning, self).__init__(params)
        self.summary_dict = None

    def fit_split_points(self, data_instances):
        """
        Apply the binning method

        Parameters
        ----------
        data_instances : DTable
            The input data

        Returns
        -------
        split_points : dict.
            Each value represent for the split points for a feature. The element in each row represent for
            the corresponding split point.
            e.g.
            split_points = {'x1': [0.1, 0.2, 0.3, 0.4 ...],    # The first feature
                            'x2': [1, 2, 3, 4, ...],           # The second feature
                            ...]                         # Other features

        """
        self._init_cols(data_instances)
        percent_value = 1.0 / self.bin_num
        # calculate the split points
        percentile_rate = [i * percent_value for i in range(1, self.bin_num)]

        if self.summary_dict is None:
            f = functools.partial(self.approxiQuantile,
                                  cols_dict=self.cols_dict,
                                  params=self.params)
            summary_dict = data_instances.mapPartitions(f)
            summary_dict = summary_dict.reduce(self.merge_summary_dict)
            self.summary_dict = summary_dict
        else:
            summary_dict = self.summary_dict
        split_points = {}
        for col_name, summary in summary_dict.items():
            split_point = []
            for percen_rate in percentile_rate:
                split_point.append(summary.query(percen_rate))
            split_points[col_name] = split_point

        return split_points

    @staticmethod
    def approxiQuantile(data_instances, cols_dict, params):
        """
        Calculates each quantile information

        Parameters
        ----------
        data_instances : DTable
            The input data

        cols_dict: dict
            Record key, value pairs where key is cols' name, and value is cols' index.

        param : FeatureBinningParam object,
                Parameters that user set.

        Returns
        -------
        summary_dict: dict
            {'col_name1': summary1,
             'col_name2': summary2,
             ...
             }

        """

        summary_dict = {}
        for col_name, col_index in cols_dict.items():
            quantile_summaries = QuantileSummaries(compress_thres=params.compress_thres,
                                                   head_size=params.head_size,
                                                   error=params.error)
            summary_dict[col_name] = quantile_summaries
        QuantileBinning.insert_datas(data_instances, summary_dict, cols_dict)
        return summary_dict

    @staticmethod
    def insert_datas(data_instances, summary_dict, cols_dict):
        for iter_key, instant in data_instances:
            features = instant.features
            for col_name, summary in summary_dict.items():
                col_index = cols_dict[col_name]
                summary.insert(features[col_index])

    @staticmethod
    def merge_summary_dict(s_dict1, s_dict2):
        if s_dict1 is None and s_dict2 is None:
            return None
        if s_dict1 is None:
            return s_dict2
        if s_dict2 is None:
            return s_dict1

        new_dict = {}
        for col_name, summary1 in s_dict1.items():
            summary2 = s_dict2.get(col_name)
            summary1.merge(summary2)
            new_dict[col_name] = summary1
        return new_dict

    def query_quantile_point(self, data_instances, cols, query_points):
        if self.summary_dict is None:
            f = functools.partial(self.approxiQuantile,
                                  cols_dict=self.cols_dict,
                                  params=self.params)
            summary_dict = data_instances.mapPartitions(f)
            summary_dict = summary_dict.reduce(self.merge_summary_dict)
            self.summary_dict = summary_dict
        else:
            summary_dict = self.summary_dict

        if isinstance(query_points, (int, float)):
            query_dict = {}
            for col_name in cols:
                query_dict[col_name] = query_points
        elif isinstance(query_points, dict):
            query_dict = query_points
        else:
            raise ValueError("query_points has wrong type, should be a float, int or dict")

        result = {}
        for col_name, query_point in query_dict.items():
            summary = summary_dict[col_name]
            result[col_name] = summary
        return result


# class BucketBinning(Binning):
#     """
#     For bucket binning, the length of each bin is the same which is:
#     L = [max(x) - min(x)] / n
#
#     The split points are min(x) + L * k
#     where k is the index of a bin.
#     """
#
#     def __init__(self, params):
#         super(BucketBinning, self).__init__(params)
#
#     def fit_split_points(self, data_instances):
#         """
#         Apply the binning method
#
#         Parameters
#         ----------
#         data_instances : DTable
#             The input data
#
#         cols : int or list of int
#             Specify which column(s) need to apply binning. -1 means do binning for all columns.
#
#         Returns
#         -------
#         split_points, 2-dimension list.
#             Each row represent for the split points for a feature. The element in each row represent for
#             the corresponding split point.
#             e.g.
#             split_points = [[0.1, 0.2, 0.3, 0.4 ...],    # The first feature
#                             [1, 2, 3, 4, ...],           # The second feature
#                             ...]                         # Other features
#
#         """
#         self._init_cols(data_instances)
#
#         statistics = MultivariateStatisticalSummary(data_instances, cols)
#         split_points = []
#         max_list = statistics.get_max(cols)
#         min_list = statistics.get_min(cols)
#         n = data_instances.count()
#         for idx, max_value in enumerate(max_list):
#             min_value = min_list[idx]
#             split_point = []
#             L = (max_value - min_value) / n
#             for k in range(self.bin_num - 1):
#                 s_p = min_value + (k + 1) * L
#                 split_point.append(s_p)
#             split_points.append(split_point)
#         return split_points
