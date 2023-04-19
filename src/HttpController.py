from App import app


@app.route("/", ['POST'])
def SetJson(json: str):
    return "Hello, World!", 200


@app.route("", ['POST'])
def IsNormal():
    return True