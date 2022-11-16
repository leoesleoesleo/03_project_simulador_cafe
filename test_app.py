# -*- coding: utf-8 -*-

from unittest import mock
import requests
import pytest
import os
import json

from mocks.mocks import (
    mocks_desagregacion_regiones,
    mocks_desagregacion_canales,
    mocks_desagregacion_categorias,
    mocks_desagregacion_marcas
)

from app import(
    allowed_file,
    json_input,
    FILE_INPUT,
    desagregacion_regiones,
    desagregacion_canales,
    desagregacion_categorias,
    desagregacion_marcas
)

ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT_MOCKS = os.path.join(ROOT_FILE, 'mocks', 'mocks_data_in.json')


def test_allowed_file():
    filename = 'prueba.csv'
    assert allowed_file(filename) == True


def test_json_input():
    data = json_input(FILE_INPUT)
    mock = json_input(FILE_INPUT_MOCKS)
    assert data.keys() == mock.keys()


def test_json_col_names_acc():
    data = json_input(FILE_INPUT)
    mock = json_input(FILE_INPUT_MOCKS)
    assert data['col_names_acc'] == mock['col_names_acc']


def test_json_col_names_noacc():
    data = json_input(FILE_INPUT)
    mock = json_input(FILE_INPUT_MOCKS)
    assert data['col_names_noacc'] == mock['col_names_noacc']


def test_desagregacion_regiones():
    data = desagregacion_regiones()
    mock = mocks_desagregacion_regiones
    assert data['data_desagregacion'] == mock


def test_desagregacion_canales():
    param_region = 'ATLANTICO'
    data = desagregacion_canales(param_region)
    mock = mocks_desagregacion_canales
    assert data['data_desagregacion'] == mock


def test_desagregacion_categorias():
    param_region = 'ATLANTICO'
    param_canal = 'ATLANTICO_CADENAS1'
    data = desagregacion_categorias(param_region, param_canal)
    mock = mocks_desagregacion_categorias
    assert data['data_desagregacion'] == mock


def test_desagregacion_marcas():
    param_region = 'ATLANTICO'
    param_canal = 'ATLANTICO_CADENAS1'
    param_categoria = 'ATLANTICO_CAFE MOLIDO#CAPSULAS'
    data = desagregacion_marcas(param_region, param_canal, param_categoria)
    mock = mocks_desagregacion_marcas
    assert data['data_desagregacion'] == mock
