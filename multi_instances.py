import sys
import yaml

qtd_gnb = int(sys.argv[1])
qtd_ue = int(sys.argv[2])

# Gera os arquivos para subir n GNBs cada um com m UEs conectadas

def generate_files(qtd_gnb, qtd_ue):
    sum_ues = 0
    initial_ue = 1
    service_dictionary = {}
    with open("docker-compose.yaml", 'r') as file:
        list_doc = yaml.safe_load(file)
    with open("config/tester.yaml", 'r') as file_tester:
        tester_default = yaml.safe_load(file_tester)
        
    #print(list_doc)
    default_service = dict(list_doc['services']['my5grantester'])
    #print(default_service)
    for i in range(1, qtd_gnb+1):
        service_dictionary['my5grantester' + str(i)] = dict(default_service)
        service_dictionary['my5grantester' + str(i)]['container_name'] = 'my5grantester' + str(i)
        service_dictionary['my5grantester' + str(i)]['volumes'] = ['./config/tester' + str(i) + '.yaml:/workspace/my5G-RANTester/config/config.yml']
        service_dictionary['my5grantester' + str(i)]['command'] = './app load-test -n ' + str(qtd_ue)
        
        another_tester = dict(tester_default)
        another_tester['ue']['msin'] = str(sum_ues + initial_ue).zfill(10)
        
        with open("config/tester" + str(i) + ".yaml", 'w') as file_write_tester:
            yaml.dump(dict(another_tester), file_write_tester)
        
        print('Tester', i, 'UE range:', sum_ues+initial_ue, '-', sum_ues+initial_ue+qtd_ue-1, 'OK')
        sum_ues = sum_ues + qtd_ue

    list_doc['services'] = dict(service_dictionary)
    #print(list_doc)
    
    with open("n-testers-compose.yaml", 'w') as file2:
        yaml.dump(dict(list_doc), file2)
    

    #print(list_doc)

if __name__ == "__main__":
    generate_files(qtd_gnb, qtd_ue)
