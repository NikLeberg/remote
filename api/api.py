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


# Globals
app = Flask(__name__)
api = Api(app)
docker = docker.from_env()


class util():
    def getImage(image):
        return {
            "name" : image.tags[0].split(":")[0],
            "id" : image.short_id,
            "comment" : image.attrs["Commend"],
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
        parser.add_argument("name", type=str, required=True, help="Name der App")
        parser.add_argument("dockerfile", type=str, required=True, help="Dockerfile enkodiert in Base64")
        parser.add_argument("installfile", type=werkzeug.datastructures.FileStorage, help="Optionale Installationsmedien die beim Bau der App verfügbar sind", location="files")
        args = parser.parse_args()
        # Dockerfile aus Base64 dekodieren und in Datei schreiben
        dockerfile = open("Dockerfile", "w+")
        dockerfile.write(base64.decodestring(args["dockerfile"]))
        dockerfile.close()
        # Optionale Installationsdateien abspeichern
        if "installfile" in args:
            installfile = args["installfile"]
            installfile.save("installfile")

        return "Ich habs versucht."


class appEntity(Resource):
    def get(self, name):
        try:
            image = docker.images.get(name)
            return util.getImage(image)
        except:
            return "App '{}' nicht gefunden.".format(name), 404


api.add_resource(appList, "/apps")
api.add_resource(appEntity, "/apps/<string:name>")


if __name__ == "__main__":
    app.run(debug=True)
