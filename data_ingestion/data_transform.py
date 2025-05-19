import pandas as pd
from langchain_core.documents import Document

class data_converter:
    def __init__(self):
        print("data converter has being initialized...")
        self.product_data = pd.read_csv(r"C:\Users\Asus\Desktop\AI Projects\Customer_Support_System\data\flipkart_product_review.csv")
        print(self.product_data.head())

    def data_transformation(self):
        pass

if __name__ == '__main__':
    data_con = data_converter()
