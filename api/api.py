# rest-api mittels Flask
# Verwaltung von VirtualBox-VMs
# ToDo:
# [/] Auflistung verfügbarer VMs
# [ ] Einschalten
# [ ] Pausieren / Sichern
# [ ] Herunterfahren per ACPI
# [ ] Killen
# [ ] Connect
# [ ] Disconnect
# [ ] Snapshot erstellen
# [ ] Snapshot laden

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


import virtualbox

vbox = virtualbox.VirtualBox()
session = virtualbox.Session()


class util():
    def getMachine(machine):
        return {
            "name" : machine.name,
            "description" : machine.description,
            "os_type_id" : machine.os_type_id,
            "state" : [str(machine.state), int(machine.state)],
            "cpu_count" : machine.cpu_count,
            "memory_size" : machine.memory_size,
            "id_p" : machine.id_p,
        }


class vmList(Resource):
    def get(self):
        response = []
        for machine in vbox.machines:
            response.append(util.getMachine(machine))
        return response

api.add_resource(vmList, "/vm")


class vm(Resource):
    def get(self, name):
        for machine in vbox.machines:
            if name == machine.name:
                return util.getMachine(machine)
        return "Virtuelle Maschine '{}' nicht gefunden.".format(name), 404

    def lock(self):
        return { "locked" : True }

api.add_resource(vm, "/vm/<string:name>")


class vmAction(Resource):
    def post(self, name, action):
        try:
            machine = vbox.find_machine(name)
            if action == "powerOn":
                progress = machine.launch_vm_process(session, "gui", "")
                print(progress)
            elif action == "powerOff":
                session.console.power_down()
            return util.getMachine(machine)
        except:
            return "Aktion '{}' konnte auf virtueller Maschine '{}' nicht durchgeführt werden.".format(action, name), 500

api.add_resource(vmAction, "/vm/<string:name>/<string:action>")


if __name__ == "__main__":
    app.run(debug=True)
