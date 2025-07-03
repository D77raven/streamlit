import requests
import pandas as pd




def get_data():
  params = {
  "engine": "google_maps_reviews",
  "data_id": "0x47806a582c8ef4ef:0xad9cb038d3db2c4f",
  "hl": "it",
  "api_key": "5b8b8d40cc9f3d5e932ca5452dfe6551d55c49a921634a1cf8406b3c8635d197"
  }

  url = f'https://serpapi.com/search.json?engine=google_maps_reviews&data_id=0x47806a582c8ef4ef:0xad9cb038d3db2c4f&hl=it&api_key=5b8b8d40cc9f3d5e932ca5452dfe6551d55c49a921634a1cf8406b3c8635d197'
  
  response = requests.get(url, params=params)
  
  if response.status_code == 200:
    data = response.json()
  
    print("data essiste")
    df = pd.DataFrame(data['reviews'])
    dati_finale = df[["snippet", 'rating']]
  
    return dati_finale
  
  else:
  
    print("data non essiste")
    return None


if __name__ == "__main__":
    df = get_data()
    if df is not None:
        print(df.head(20))

    else:
        print("No reviews found.")

