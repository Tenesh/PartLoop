# Introduction

PartLoop is an [inventory management software](https://en.wikipedia.org/wiki/Inventory_management_software), designed for general spare part or component management .

PartLoop is entirely written in **PYTHON** with several frameworks namely [**_PyQt5_**](https://pypi.org/project/PyQt5/) and [**_psycopg2_**](https://pypi.org/project/psycopg2/).

With PartLoop, you can manage your inventory with _precision_ and **accuracy**. The core functionality of the system are **managing parts** and **usage entries**.

1. You can add or edit parts with various details such as _manufacturer_, _brand_, _model_, _minimum stock_ and etc.
2. You can easily track the _actual quantity_ of parts in the system which will alert if _lower limit_ reached!
3. You can _record the usage of each stock_ using entry function providing.
4. With various _filtering keys_, PartLoop allows you to search for many fields in seconds.

# Requirements

## Platform

- Python
- PostgreSQL database

## Dependencies

- PyQt5
- psycopg2
- PyQt5-tools

# Getting started

## Cloning the repo

    $ git clone https://github.com/Tenesh/PartLoop.git

## Setting up database

    #Restore PartLoop database in your localhost created database.
    $ pg_dump dbname < partloopdump.sql

## Install dependencies

    $ pip install -r requirements.txt 


## Launch PartLoop

Simply run *index.py* and start managing your inventory!<br>

    $ python index.py


#### That's all. How often did you forget to re-order parts because your stock went low and you didn't notice? Now, you have no worry! **_PartLoop got you covered._**
