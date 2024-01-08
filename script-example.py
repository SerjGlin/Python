import sys
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import psycopg2
import authorize
#!!!ПРИМЕР СКРИПТА,ЧИТАЮЩЕГО ИЗ БАЗЫ И ДЕЛАЮЩЕГО ВЫЗОВ API!!!

requests.packages.urllib3.disable_warnings()

# необходимо для формирования endpoint
registers_id = 43607 #указать мастер-реестр, по которому идет ТП
actorId = '' #указать актора
rule = 'READ' #указать правило
contour = 'dev'    #указать контурs

if contour == 'dev':
    CURR_ENDPOINT = 'здесь актуальный адрес'
    conn_string = "строка подключения к postgres"
elif contour == 'test':
    CURR_ENDPOINT = 'здесь актуальный адрес'
    conn_string = "строка подключения к postgres"


#Авторизация

headersAuth = authorize.authorize(contour=contour)
print(headersAuth)
def acl_linked_docs_buttons(prop):  #создание прав на кнопку связанных документов карточек и реестров
    try:
        url_buttons ='https://' + CURR_ENDPOINT + '/api/tech-process/acl/table';
        print('url: ', url_buttons)
        acl_button = requests.post(url_buttons, data=json.dumps(prop), headers=headersAuth)
        result = acl_button.text
        print('Результат выполнения запроса: ', result)
    except requests.exceptions.RequestException as e:
        return e

def runner():

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''             
                                                select ldob.linked_documents_objdoc_buttons_id as ld_buttons_id, 1 as buttons_type 
                                                from mod_tech_process.linked_documents_objdoc_buttons ldob 
                                                join mod_tech_process.linked_documents ld 
                                                on ldob.linked_documents_id = ld.linked_documents_id
                                                join mod_tech_process.stages s
                                                on ld.stages_id = s.stages_id
                                                where s.registers_id = '{registerID}'   
                                                union
                                                select ldrb.linked_documents_registers_buttons_id, 2 as buttons_type
                                                from mod_tech_process.linked_documents_registers_buttons ldrb
                                                join mod_tech_process.linked_documents ld
                                                on ldrb.linked_documents_id = ld.linked_documents_id
                                                join mod_tech_process.stages s
                                                on ld.stages_id = s.stages_id
                                                where s.registers_id = '{registerID}'                   
                                        '''.format(registerID=registers_id)

    # print('sql: ', sql)
    cursor.execute(sql)
    ld_buttons = cursor.fetchall()
    if not ld_buttons:
        print('Запрос не нашел созданных кнопок, скрипт завершен')
        sys.exit()
    conn.close()
    cursor.close()
    with ThreadPoolExecutor(max_workers=1) as executor:
        for row in ld_buttons:
            buttons_id = row[0]
            buttons_type = row[1]
            # print(buttons_id, buttons_type)
            if buttons_type == 1:   #если кнопка карточки
                properties={
                    'aclName': 'linked_documents_objdoc_buttons',
                    'actorId': actorId,
                    'id': buttons_id,
                    'rule': rule
                }
                #вызов метода раздачи прав
                # print(properties)
                acl_linked_docs_buttons(properties)
            elif buttons_type == 2:  #если кнопка реестра
                properties = {
                    'aclName': 'linked_documents_registers_buttons',
                    'actorId': actorId,
                    'id': buttons_id,
                    'rule': rule
                }
                #вызов метода раздачи прав
                # print(properties)
                acl_linked_docs_buttons(properties)


runner()
