#
# Proyecto Simulador Café

## &nbsp; [![pyVersion37](https://img.shields.io/badge/python-3.7.6-blue.svg)](https://www.python.org/download/releases/3.7/)

## Flujo del proceso
<div align="center">
	<img height="700" src="https://leoesleoesleo.github.io/imagenes/flujo_simulador_cafe.png" alt="Flujo">
</div>  

## Insumos 
<p align="justify">
Data_in es el json que se pide para pronosticar los siguientes 12 meses. Tiene que traer incluido los próximos 12 meses y esto se deja claro en la columna de "pronostico" de los datos. 
</p>
<p align="justify">
Es decir se entregan todos los datos históricos y futuros. las columnas más importantes son "venta_kg", "venta_dinero", "pronostico", "mes", "ano". 
Las demás columnas son datos de variables explicativas, el nombre de las columnas se da en "col_names".
</p>
<p align="justify">
Además se tiene que entregar la información de la desagregación en marca, canal, categoria y región. Para especificar si se quiere usar el modelo 3.1 variables accionables  independientes ( el usuarios modifica las variables accionables y se le entrega una predicción) se coloca "variables_accionables_dependientes": false. 
En caso contrario se tiene que llenar los datos de "venta_kg" y "venta_dinero" para el futuro y poner "variables_accionables_dependientes": true para que el modelo use la parte 3.2 (optimizar y hallar las variables accionables) .
</p>
<p align="justify">
Data out retorna los datos completados (llenando el pronóstico de venta o las variables accionables ) .
Se entrega también una variable booleana "posible" en caso de no encontrar modelo, también se entregan las 5 variables notables más importantes en orden en variables notables.
</p>
<p align="justify">
Por último train_model se entrega una desagregación y se pide que se entrene un modelo. en este caso solo se retorna error en caso de no poder entrenarlo.
</p>



## Manual de instalación

### Pasos

- Clonar repositorio
	```
	git clone https://github.com/leoesleoesleo/03_project_simulador_cafe.git
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
	python -m venv env_simulador
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

<div align="center">
	<img height="700" src="https://leoesleoesleo.github.io/imagenes/pytest_simulador_cafe.PNG" alt="Flujo">
</div>  


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
