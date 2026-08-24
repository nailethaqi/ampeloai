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

from PIL import Image, UnidentifiedImageError

from ai.predict import predict_image


app = FastAPI(
    title="AmpeloAI",
    description=(
        "AI-based web system for grape leaf "
        "disease image analysis"
    ),
    version="1.1.0"
)


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
        "system": "AmpeloAI",
        "case_study": "Grape Leaf Disease Detection",
        "supported_classes": [
            "Black_Rot",
            "Esca",
            "Healthy",
            "Leaf_Blight"
        ],
        "unsupported_class": "Other"
    }


@app.post("/api/predict")
async def predict(
    file: UploadFile = File(...)
):

    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png"
    }

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only JPG, JPEG and PNG "
                "images are allowed."
            )
        )

    contents = await file.read()

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty."
        )

    try:

        with Image.open(
            BytesIO(contents)
        ) as image:

            image.load()

            result = predict_image(
                image
            )

    except UnidentifiedImageError:

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file is not "
                "a valid image."
            )
        )

    except OSError:

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded image could "
                "not be processed."
            )
        )

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Image analysis failed: "
                f"{str(error)}"
            )
        )

    return {
        "success": True,
        "prediction": result
    }