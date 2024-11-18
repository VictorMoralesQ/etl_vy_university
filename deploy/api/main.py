import os
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/booking")
def read_booking(limit: int = 1000, offset: int = 0):
    df = pd.read_csv(r'.datasets/booking.csv')
    df = df.replace(np.nan, None)
    return {"data": df.iloc[offset:offset + limit].to_dict(orient='records'),
            "total_items": len(df.index)}

@app.get("/booking/new")
def read_booking(limit: int = 1000, offset: int = 0):
    df = pd.read_csv(r'.datasets/Booking_20240201_20240331.csv')
    df = df.replace(np.nan, None)
    return {"data": df.iloc[offset:offset + limit].to_dict(orient='records'),
            "total_items": len(df.index)}

@app.get("/booking/passenger")
def read_booking_passenger(limit: int = 1000, offset: int = 0):
    df = pd.read_csv('.datasets/booking_passenger.csv')
    df = df.replace(np.nan, None)
    return {"data": df.iloc[offset:offset + limit].to_dict(orient='records'),
            "total_items": len(df.index)}

@app.get("/booking/passenger/new")
def read_booking_passenger(limit: int = 1000, offset: int = 0):
    df = pd.read_csv('.datasets/BookingPassenger_20190201_20190331.csv')
    df = df.replace(np.nan, None)
    return {"data": df.iloc[offset:offset + limit].to_dict(orient='records'),
            "total_items": len(df.index)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
