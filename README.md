# RaspRobot
The repository for the programmation réseaux of Master 2 ISD. Groupe: Kelun CHAI, Djaber Solimani and Nogaye Gning

## Organization
| Nom | Task |
| ---- | ---- |
| Djaber Solimani | Communication réseau en TCP + Code Serveur/Client + Mise en place du Raspberry Pi|
| Nogaye Gning | Construction du robot + Mise en place du Raspberry Pi |
| Kelun Chai | Code robot + Mise en place du Raspberry Pi |

## Server
*Usage*: `python3 server.py`
Le serveur démarrera automatiquement sur le port 9000 de `192.168.1.1`. 

Il peut traiter les messages envoyés par le client (connect) et le robot (register). Si le message reçu n'est pas reconnu, il renvoie un message d'erreur.
## Client
*Usage*: `python3 client.py router_ip`

Le client se connecte au routeur via l'adresse IP, puis il peut envoyer des commandes.
## Robot
*Usage*: `python3 robot.py robot_name router_ip`

Le robot se connecte au routeur avec l'adresse IP, il peut traiter les commandes suivantes: [`forward`, `backward`, `left`, `right`, `speed`]
