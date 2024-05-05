[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/SHHOCZhI)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=12189852)
# Trabajo práctico: tlengrep

Este repositorio contiene una base de código a partir de la cual implementar
el trabajo práctico de Teoría de Lenguajes.

## Aclaración del grupo BTS
El modo de ejecución es igual al provisto por la cátedra.
Lo único distinto es cómo corrimos los tests.

## Cómo correr nuestros tests
Correr el script `experimentacion.sh` que se encuentra en `tlengrep/tests` 

## Estructura del repositorio

El repositorio contiene los siguientes directorios:
- `tlengrep`: contiene el código fuente del trabajo práctico.
- `informe`: donde deben colocar el informe del trabajo práctico.

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



