from fastapi import FastAPI

app = FastAPI()

async def main():
    return
    



@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        print("Application shutdown")
        log.write("Application shutdown")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


print("starting")
main()

