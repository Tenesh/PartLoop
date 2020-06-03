import psycopg2


def ConnectDatabase():
    return psycopg2.connect(host='localhost', user='postgres', password='postgres123', database='PartLoop')