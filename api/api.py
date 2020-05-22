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
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)


import docker
docker = docker.from_env()


class util():
    def getImage(image):
        return {
            "name" : image.tag[0].split(":")[0],
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
        return "Erstellen neuer Apps wird noch nicht unterstützt.", 404


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
