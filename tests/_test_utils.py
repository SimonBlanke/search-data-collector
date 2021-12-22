import numpy as np

from collections import Counter


def search_data_equal(search_data1, search_data2, assert_order=True):
    col1 = list(search_data1.columns)
    col2 = list(search_data2.columns)

    print("\n col1 \n", col1, "\n", type(col1))
    print("\n col2 \n", col2, "\n", type(col2))

    if set(col1) != set(col2):
        return False

    dtypes1 = list(search_data1.dtypes)
    dtypes2 = list(search_data2.dtypes)

    print("\n dtypes1 \n", dtypes1, "\n", type(dtypes1))
    print("\n dtypes2 \n", dtypes2, "\n", type(dtypes2))

    if set(dtypes1) != set(dtypes2):
        return False

    print("\n search_data1 \n", search_data1, "\n dtypes:\n", search_data1.dtypes)
    print("\n search_data2 \n", search_data2, "\n dtypes:\n", search_data2.dtypes)

    for col in col1:
        values1 = search_data1[col].values
        values2 = search_data2[col].values

        if not assert_order:
            occur_d1 = Counter(list(values1))
            occur_d2 = Counter(list(values2))

            if occur_d1 != occur_d2:
                print("\n occur_d1 \n", occur_d1)
                print("\n occur_d2 \n", occur_d2)

                return False

        if assert_order and not np.array_equal(values1, values2):
            print("\n values1 \n", values1)
            print("\n values2 \n", values2)

            return False

    return True
