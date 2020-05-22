# rest-api mittels Flask
# Verwaltung von docker images
# ToDo:
# [/] Auflistung verfügbarer apps/images
# [ ] Konfigurieren / erstellen / Dockerfile
# [ ] Einschalten
# [ ] Pausieren / commiten / weiterfahren
# [ ] Killen
# [ ] Connect
# [ ] Disconnect

# get - holen
# post - erstellen
# put - aktualisieren
# delete - löschen


from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
import docker
import base64
import os


# Globals
app = Flask(__name__)
api = Api(app)
docker = docker.from_env()


class util():
    def getImage(image):
        return {
            "name" : image.tags[0].split(":")[0],
            "id" : image.short_id,
            "comment" : image.attrs["Comment"],
            "created" : image.attrs["Created"],
            "parent" : image.attrs["Parent"],
            "labels" : image.labels
        }


class appList(Resource):
    def get(self):
        response = []
        for image in docker.images.list():
            response.append(util.getImage(image))

        return response

    def post(self):
        response = []
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="gebe den Name der App an")
        parser.add_argument("dockerfile", type=str, required=True, help="es fehlt das Dockerfile enkodiert in Base64")
        parser.add_argument("installfile", type=werkzeug.datastructures.FileStorage, location="files")
        args = parser.parse_args()
        # App-Pfad erstellen
        path = f"/home/remote/remote/{args["name"]}"
        os.makedirs(path, exist_ok=True)
        # Dockerfile aus Base64 dekodieren und in Datei schreiben
        dockerfile = open(f"{path}/Dockerfile", "w+")
        dockerfile.write(base64.decodestring(args["dockerfile"]))
        dockerfile.close()
        # Optionale Installationsdateien abspeichern
        if "installfile" in args:
            installfile = args["installfile"]
            installfile.save(f"{path}/installfile.zip")

        return args


class appEntity(Resource):
    def get(self, name):
        try:
            image = docker.images.get(name)
            return util.getImage(image)
        except:
            return f"App '{name}' nicht gefunden.", 404


api.add_resource(appList, "/apps")
api.add_resource(appEntity, "/apps/<string:name>")


if __name__ == "__main__":
    app.run(debug=True)
