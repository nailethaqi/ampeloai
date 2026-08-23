from io import BytesIO

from fastapi import (
    FastAPI,
    Request,
    UploadFile,
    File,
    HTTPException
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from PIL import Image

from ai.predict import predict_image

from database import (
    init_db,
    save_analysis,
    get_history,
    get_statistics
)


app = FastAPI(
    title="Smart Agriculture AI",
    description=(
        "Web system for AI-based grape leaf "
        "disease image analysis"
    ),
    version="1.0.0"
)




init_db()




app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)




templates = Jinja2Templates(
    directory="templates"
)




@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )




@app.get("/api/status")
def status():

    return {
        "status": "online",
        "system": "Smart Agriculture AI",
        "case_study": "Grape Leaf Disease Detection"
    }




@app.post("/api/predict")
async def predict(
    file: UploadFile = File(...)
):

    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png"
    ]

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only JPG, JPEG and PNG "
                "images are allowed."
            )
        )


    try:

        contents = await file.read()

        image = Image.open(
            BytesIO(contents)
        )

        result = predict_image(image)


       
        save_analysis(
            predicted_class=result[
                "predicted_class"
            ],
            confidence=result[
                "confidence"
            ]
        )


        return {
            "success": True,
            "prediction": result
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Image analysis failed: "
                f"{str(error)}"
            )
        )




@app.get("/api/history")
def history():

    return {
        "history": get_history()
    }




@app.get("/api/statistics")
def statistics():

    return get_statistics()