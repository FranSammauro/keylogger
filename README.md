# Instalacion del Keylogger

En este repositorio ve voy a dejar el paso a paso como vas a instalar el servidor y el keylogger, en tu computadora, lo que si te aconsejo es que esto son con fines educativos, ten mucho cuidado.

## Creacion de Nuestro Entorno de Trabajo
---------------------------------

### Requisitos 
- Python 
- vitualenv
------------------------------------------

###  Creamos el entorno virtual

```python
python -m virtualenv venv
```

> Ejecutamos virtualenv
```python
.\venv\Scripts\activate
```

> Detemos virtualenv
```python
deactivate
```

-----------------------------------
###  Instalacion de librerias 
```python
pip install -r ".\requirements.txt"
```