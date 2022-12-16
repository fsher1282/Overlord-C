import os
import json
import pandas as pd


if __name__ == '__main__':
    """
    By default with getting data from os.environ they are loaded
    as str so conversion will likely be necessary
    """
    DATA = os.environ['Query']

    json_data = json.loads(DATA)
    print(pd.DataFrame(json_data, index=['Hire Date', 'Age']))





