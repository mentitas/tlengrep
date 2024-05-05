# Trabajo práctico: tlengrep

El propósito de este proyecto consiste en desarrollar una herramienta capaz de detectar las ocurrencias de una expresión regular en un texto. Creamos un parser que permite leer una cadena de texto de entrada, y traducirla a una instancia de la clase RegEx. Luego representamos las expresiones regulares como objetos e implementamos la funcionalidad de búsqueda haciendo uso de autómatas finitos.

## Cómo correr nuestros tests
Correr el script `experimentacion.sh` que se encuentra en `tlengrep/tests` 

## Estructura del repositorio

El repositorio contiene los siguientes directorios:
- `tlengrep`: contiene el código fuente del trabajo práctico.

## Modo de ejecución

Todos los comandos que se mencionan a continuación deben ejecutarse desde el
directorio `tlengrep`.

### Pasos previos

1. (Opcional) Crear un entorno virtual de Python:
   ```bash
   python3 -m venv venv
   ```
   y activarlo:
   ```bash
   source venv/bin/activate
   ```
   (para desactivarlo, ejecutar `deactivate`).

2. Instalar las dependencias:
   ```bash
    pip install -r requirements.txt
    ```

### Ejecución del programa
El programa se ejecuta con el comando:
```bash
python3 tlengrep.py [expresión regular] [archivo de entrada]
```

- El argumento `expresión regular` indica la expresión regular a buscar y es
  obligatorio.
- El argumento `archivo de entrada` indica el archivo en el que se debe buscar
  y es opcional. De no ser especificado, se lee de la entrada estándar.

El programa admite las siguientes opciones:
- `-h`, `--help`: muestra un mensaje de ayuda y termina.
- `-m`, `--module [módulo]`: permite cargar una expresión regular ya parseada
  desde un módulo de Python. De usarse esta opción, no se debe especificar
  la expresión regular como argumento.
- `-n`, `--naive`: utiliza la implementación naive brindada por la cátedra.

## Ejecución de los tests
Para ejecutar los tests, utilizar el comando:
```bash
pytest
```

Para ejecutar solo los tests de la cátedra:
- Para la primera entrega, ejecutar:
  ```bash
  pytest -k test_regex.py
  ```
- Para la segunda entrega, ejecutar:
  ```bash
  pytest -k test_parser.py
  ```



