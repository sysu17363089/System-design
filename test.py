# from twisted.web.static import File
import os
from klein import Klein


app = Klein()


@app.route("/", branch=True)
def pg_index(request):

    file_name = "train_model.zip"
    with open(file_name, 'rb') as file:

        return file.read()


app.run("localhost", 8080)