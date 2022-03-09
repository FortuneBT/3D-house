import pandas as pd
import json
import numpy as np
import folium

class Data():
    """
    This class manage the data for the machine learning part
    """
    def __init__(self):
        self.mydata = None    
        self.process_data()
        

    def price_mean_by_region(self,mun):

        return self.mydata.loc[:,["Municipality","Region","Price"]].groupby(["Region"]).mean().sort_values(by="Price", ascending=False).tail(20)

    def find_top(self):
        """
        find the most pricy house of Belgium at this moment on Immoweb
        """
        return self.mydata.loc[:,["Municipality","Region","Price"]].sort_values(by="Price", ascending=False).head(5)

    def find_top_municipality(self,municipality):
        """
        find the municipality only giving a few letter of the municipality
        """
        return self.mydata.loc[self.mydata["Municipality"].str.contains(municipality,case=False)].sort_values(by="Price",ascending=False).head(5)

    def process_data(self):

        """"""
        belgium = json.load(open("../data/postal-codes-belgium.geojson", "r"))
        maisons = pd.read_csv("../data/housing_data.csv",dtype={"Bedrooms": "Int64"})
        belgium["features"][1]
        maisons.dropna(axis=1,thresh=7000, how="any", inplace=True)

        """"""

        maisons.drop(["Price (sr only)"],axis=1,inplace=True)
        maisons.drop(["Tenement building"],axis=1,inplace=True)
        maisons.drop(["Price HTML"],axis=1,inplace=True)

        """"""

        for elem in belgium["features"][0]["properties"]:
            propriete = belgium["features"][0]["properties"]
            
        """"""

        code_map_id = {}

        for x,feature in enumerate(belgium["features"]):
            properties = feature["properties"]
            feature["id"] = int(properties["postcode"])
            
            if "smun_name_fr" in properties.keys():
                code_map_id[feature["id"]] = properties["smun_name_fr"]
            elif "mun_name_fr" in properties.keys():
                code_map_id[feature["id"]] = properties["mun_name_fr"]
            
            elif "arr_name_fr" in properties.keys():
                code_map_id[feature["id"]] = properties["arr_name_fr"]
            else:
                code_map_id[feature["id"]] = np.nan

        """"""

        maisons["id"] = maisons["Post code"].apply(lambda x : code_map_id[x])

        """"""
        dfdic = pd.json_normalize(belgium["features"])

        dfdic["properties.postcode"] = dfdic["properties.postcode"].astype(int)

        dfdic = dfdic.rename(columns={"properties.postcode": "Post code"})

        df = pd.merge(maisons, dfdic, on=["Post code", "Post code"])


        """"""
        df.rename(inplace=True, columns={"id_x":"Municipality"})
        df.rename(inplace=True, columns={"properties.mun_name_nl":"nl"})
        df.rename(inplace=True, columns={"property sub-type":"Type"})
        df.rename(inplace=True, columns={"properties.reg_name_fr":"Region"})
        df.rename(inplace=True, columns={"properties.prov_name_fr":"Province"})
        df.sort_values(by="Price",ascending=False).groupby(["Municipality"])[["Address","Municipality","Post code","Type","Price"]].head()

        """"""
        self.mydata = df[["Address","Bedrooms","Post code","Municipality","Region","Province","Type","Price"]].copy()
        """"""
        self.mydata["Price"] = self.mydata["Price"].apply(lambda x: 0 if "<p" in x else int(x))
        """"""
        self.mydata.loc[:,"Bedrooms"].fillna(0,inplace=True)
        """"""
        self.mydata.dropna(subset=["Municipality"],inplace=True)

        self.mydata.dropna(subset=["Address"],inplace=True)

        self.mydata.loc[:,"Province"].fillna("Without Province",inplace=True)
        """"""
        self.mydata.loc[:,"Province"] = self.mydata.loc[:,"Province"].apply(lambda x : x.split(" (")[0] if " (" in x else x)
        """"""





