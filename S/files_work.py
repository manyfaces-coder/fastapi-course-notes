from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(filename, "wb") as f:
        f.write(file.read())
