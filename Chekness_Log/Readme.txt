1º Instalar el servicio:

	sudo bash instalacion.sh
	
2º Modificar el archivo config.ini

	sudo nano config.ini
	
3º Para activar el servicio

	sudo systemctl enable chekness-log.service
	sudo systemctl start chekness-log.service
	
4º Para desactivar el servicio

	sudo systemctl stop chekness-log.service
	sudo systemctl disable chekness-log.service
	
5º Ser feliz