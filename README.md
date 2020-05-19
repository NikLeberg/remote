# remote
remotely control a linux-vm -> connect to docker containerized applications on it -> stream X11 display to local machine via chrome browser -> forward USB with WebUSB to remote

---

This project is a POC (to be proofed). Easier solutions would be rdp or vnc.
The ultimate goal is: being able to remotely control windows (with wine) and linux gui apps.

---

### Virtualbox
* Zugriff auf Virtualbox-Instanzen per Chrome Webbrowser
* USB Weiterleitung mittels WebUSB
    * ev. nötig: USB Treiber auf WinUSB setzen per Zadig
* Verwaltung & Erstellung der VMs per REST API
* Simple Webpage

### Docker
* virtualbox mit Linux Gast auf Windows Host
    * 3 x Portweiterleitung:
        * Management-Website
        * X11-Stream
        * USB-Stream
* in Linux läuft Webserver
    * apache2 / nginx für statische Daten
    * flask REST API
    * Docker Server
        * mit base-image: wine & X11 Weiterleitung
    * per API:
        * Docker Images
            * list
            * dockerfile online edit & upload
            * start / stop
            * connect / disconnect
    REST API
---

# Notizen
[WebUSB Beispiel](https://medium.com/@gendor/connecting-to-usb-devices-with-your-browser-d433a6df6f2)
User auffordern ein USB-Gerät freizuschalten:

    let device = await navigator.usb.requestDevice({filters: []});

[Chrome Geräte Fehler](chrome://device-log)
[Erweitertes Beispiel](https://www.visuality.pl/posts/webusb-bridge-between-usb-devices-and-web-browsers)
[WebUSB Draft](https://wicg.github.io/webusb/)
[USB Vendor/Hardware ID Datenbank](https://devicehunt.com/view/type/usb/vendor/10C4/device/EA60)