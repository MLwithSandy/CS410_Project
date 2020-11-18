import pandas as pd


def read_NASDAQ_List(fileName):
    list_nsdq_stock = pd.read_csv(fileName, sep=',', header=0, engine='python')
    print(list_nsdq_stock.head(5))
    return list_nsdq_stock


def main(fileName):
    list_nsdq_stock = read_NASDAQ_List(fileName);
    return list_nsdq_stock


if __name__ == '__main__':
    fileName = 'nasdaq_result_list.csv'
    main(fileName)
