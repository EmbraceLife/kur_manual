"""
Inputs:
1. file_path for feature array, target array for training, validation, test set

Return:
1. ready-to-train dataset: features arrays, targets arrays for training, validation, test set


### Summary:
- to load is faster than to process and create features and targets from previous pyfile
- processed ready features array and targets array for training, validation, test sets can be imported from this source file

### Steps
- load train_features, train_targets, valid_features, valid_targets, test_features, test_targets from files
- change its shape for training and predict
"""


from prep_data_utils_01_save_load_large_arrays_bcolz_np_pickle_torch import bz_load_array
import numpy as np
# create paths for loading those arrays above
train_features_path = "/Users/Natsume/Downloads/data_for_all/stocks/features_targets/train_features_path"
train_targets_path = "/Users/Natsume/Downloads/data_for_all/stocks/features_targets/train_targets_path"

valid_features_path = "/Users/Natsume/Downloads/data_for_all/stocks/features_targets/valid_features_path"
valid_targets_path = "/Users/Natsume/Downloads/data_for_all/stocks/features_targets/valid_targets_path"

test_features_path = "/Users/Natsume/Downloads/data_for_all/stocks/features_targets/test_features_path"
test_targets_path = "/Users/Natsume/Downloads/data_for_all/stocks/features_targets/test_targets_path"

train_features = bz_load_array(train_features_path)
train_targets = bz_load_array(train_targets_path)
valid_features = bz_load_array(valid_features_path)
valid_targets = bz_load_array(valid_targets_path)
test_features = bz_load_array(test_features_path)
test_targets = bz_load_array(test_targets_path)


### do np.reshape and np.transpose have very different result

# train_features_reshape = np.reshape(train_features, (-1, 30, 61))
# valid_features_reshape = np.reshape(valid_features, (-1, 30, 61))
# test_features_reshape = np.reshape(test_features, (-1, 30, 61))
train_features = np.transpose(train_features, (0, 2, 1))
valid_features = np.transpose(valid_features, (0, 2, 1))
test_features = np.transpose(test_features, (0, 2, 1))

# check_test_f = np.load("/Users/Natsume/Downloads/data_for_all/stocks/test_features_check.npy")
# check_test_l = np.load("/Users/Natsume/Downloads/data_for_all/stocks/test_labels_check.npy")
#
# test_targets == check_test_l
# test_features_t == check_test_f