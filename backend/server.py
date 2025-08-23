# This is the file that we actually run and would be the entry point of our app
from src.app import app

# This just says that if we are running this python file directly, we import uvicorn
if __name__ == "__main__":
    # Uvicorn is a webserver that allows us to serve our fast API app
    import uvicorn

    # This means that we run the app on local host
    uvicorn.run(app, host="0.0.0.0", port=8000)