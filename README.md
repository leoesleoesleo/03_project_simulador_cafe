#
# Proyecto Simulador Café

## &nbsp; [![pyVersion37](https://img.shields.io/badge/python-3.7.6-blue.svg)](https://www.python.org/download/releases/3.7/)

## Flujo del proceso
<div align="center">
	<img height="700" src="https://leoesleoesleo.github.io/imagenes/botsi_flujo.PNG" alt="PokeAPI">
</div>  

## Manual de instalación

### Pasos

- Clonar repositorio
	```
	git clone https://github.com/leoesleoesleo/03_project_botsitech.git
	```
- Crear entorno virtual

    Ejemplo anaconda
	```
	conda create -n env_simulador python=3.7
	```
	```
	conda activate env_simulador
	```
    Ejemplo virtualenv
    ```
	pip install virtualenv
	```
	```
	python3 -m venv env_simulador
	```
	```
	\Scripts\activate
	```
	
- Navegar hasta la carpeta del proyecto en la carpeta requirements para instalar dependencias
    ```
    pip install -r requirements.txt
    ```

- Ejecutar pruebas unitarias (Opcional)
   ```
   pytest -v  
    ``` 

- Validar cobertura de la aplicación (Opcional)
    ```
   coverage run -m pytest -v -p no:cacheprovider --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html  
    ```    
    
- Levantar servicio
    ```
   python manage.py runserver
    ```

-  Iniciar programa en el navegador
    ```
   https://127.0.0.1:5000
    ```
