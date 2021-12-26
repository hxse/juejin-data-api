from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from gm.api import *
import time
from pathlib import Path
import uvicorn
import json
import base64
from PIL import Image
from combin_image import combin_image
from request_image import request_image

with open("./config.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    set_token(data["token"])


def get_data(name, frequency, count) -> pd.DataFrame:
    df = history_n(
        symbol=name,  # "SHFE.rb2010"
        frequency=frequency,
        count=count,
        fields="bob,open,high,low,close,volume",
        df=True,
    )
    return df
    # df = df.rename(columns={"bob": "x"})
    df["sma8"] = df["close"].rolling(8).mean()
    df["sma16"] = df["close"].rolling(16).mean()
    df["sma32"] = df["close"].rolling(32).mean()
    df["sma64"] = df["close"].rolling(64).mean()
    return df.dropna(axis=0, how="any")
    return df.where(df.notnull(), None)


app = FastAPI()


origins = ["https://null.jsbin.com", "https://output.jsbin.com", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def write_csv(path, data):
    data.to_csv(path, sep="\t", index=False)


def read_csv(path):
    data = pd.read_csv(path, sep="\t")
    return data


@app.get("/")
def read_root():
    return {"Hello": "World"}


def process_data(name, frequency, count, refresh):
    path = Path(f"./history_data/{name}-{frequency}-{count}.csv")
    start = time.time()
    print("start:", start)
    if refresh or (not path.exists()):
        df = get_data(name, frequency, count)
        df["bob"] = df["bob"].apply(lambda x: x.timestamp())
        write_csv(path, df)
    else:
        df = read_csv(path)
    data = [df[i].tolist() for i in df]
    print("end:", df.shape, time.time() - start, path, refresh)
    return data


@app.get("/ohlcv")
def item(
    name: str,
    frequency: str,
    count: int,
    refresh: bool = True,
    testUpdate: bool = False,
    splitStart: int = 0,
    splitEnd: int = 0,
):
    data = process_data(name, frequency, count, refresh)
    if not testUpdate:
        return JSONResponse(content=data)
    else:
        print(splitStart, splitEnd)
        return JSONResponse(content=[i[splitStart:splitEnd] for i in data])


@app.get("/data")
def read_item(name: str, frequency: str, count: int):
    df = get_data(name, frequency, count)
    df["timestamp"] = df["bob"].apply(lambda x: x.timestamp() * 1000)
    return JSONResponse(content=df.values.tolist())

    df["date"] = df["bob"].dt.strftime("%Y/%m/%d %h:%min:%s")
    column = ["timestamp", "open", "close", "high", "low", "sma16", "sma32", "sma64"]
    df = df.filter(column, axis=1)
    print(df)
    return JSONResponse(content=df.values.tolist())

    for i in df:
        if "sma" not in i:
            df[i] = df[i].astype(float)

    df = [[i, df.loc[i].to_list()[1:5], df.loc[i].to_list()[5:]] for i in df.index]
    print(df[0], [type(i) for i in df[0][1]])
    return JSONResponse(content=df)


@app.post("/store")
async def getInformation(info: Request):
    data = await info.json()
    print(data["id"], len(data["dataUrl"].split(",")[1]))
    with open(f"./image/{data['id']}.png", "wb") as f:
        f.write(base64.b64decode(data["dataUrl"].split(",")[1]))

    storeIdx = data["id"].split("_")[1]
    targetPath = Path("./image") / f"all_{storeIdx}.png"
    imageArr = [
        i for i in Path("./image").glob(f"*_{storeIdx }.png") if i.name != targetPath.name
    ]

    if data['config']["screenNum"] == len(imageArr):
        targetPath.unlink(missing_ok=True)
        combin_image(imageArr, targetPath)
        for i in imageArr:
            i.unlink()
        request_image(targetPath,{"name":data['config']['name']})
        # targetPath.unlink()
    return JSONResponse(content=data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, debug=False)
