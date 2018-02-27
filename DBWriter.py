import cx_Oracle
import json

server = json.load(open('credentials'))
conndata = f"{server['user']}/{server['pass']}@{server['ip']}:{server['port']}/{server['SID']}"

def priceCleanUp(price):
    
    numbers = '0123456789.'
    result = ''
    for i in price:
        if (i in numbers):
            result+=i
    return float(result)


def DBInsert(tender):
    
    #input is the DICT with tender information
    
    #init DB connection
    db = None
    
    #converting data types

    id_tender = int(tender['tenderNumber'])
    dt_start = tender['tenderStart'].split(' ')[-1]
    dt_end = tender['tenderEnd'].split(' ')[-2]
    name_tender = tender['tenderName']
    host_tender = tender['tenderOwner']
    edrpou = tender['tenderOwnerID']
    price = priceCleanUp(tender['tenderPrice'].split('грн')[0])
    link_tender = tender['tenderPageLink']
    
    try:
        db = cx_Oracle.connect(conndata)

        try:
            curs = db.cursor()
            curs.execute(f"""
            
            INSERT INTO {server['table']}
            (id_tender, name_tender, host_tender, edrpou, price, link_tender, dt_start, dt_end) 
            VALUES 
            ({id_tender}, '{name_tender}', '{host_tender}', {edrpou}, {price}, '{link_tender}', TO_DATE('{dt_start}', 'DD.MM.YYYY'), TO_DATE('{dt_end}', 'DD.MM.YYYY'))""")
            
            #test output
            curs.execute(f"SELECT * FROM {server['table']}")
            
            pprint(curs.fetchall())
        finally:
            curs.close()
            
    #close DB connection        
    finally:
        if db is not None:
            db.close()