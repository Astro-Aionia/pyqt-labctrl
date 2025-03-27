# PyQt-Labctrl

Applications for ultrafast experiments with GUI.

## How to Use

To add a new instrument, put dependencies and customized classed in `.\instrument`, GUI file in `.\ui`, and implement the functions of items in a GUI in `.\function`.

For complex mathematical operations, methods can be written in `.\calculation`.

To make a software for a specific experiment, design a new GUI and conbine all GUIs for single devices, put the mainwindow file in `.\app`.

## Instruments

- Servotronix stage CDHD2
- Toupcam camera
- TOPAS
- EMCCD

## Deployment

Use Ananconda to create an env, install required packages with

```cmd
pip install -f requirements.txt
```
