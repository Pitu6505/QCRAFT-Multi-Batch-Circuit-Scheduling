import aiohttp
import asyncio
import random
url = 'http://localhost:8082/'

pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'


urls = {
    "Combinational-Mapping-1": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler/main/circuits-code//combinational/mapping/20QBT_16CYC_32GN_1.0P2_0_vq.py",
    "Combinational-Mapping-2": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler/main/circuits-code//combinational/mapping/20QBT_4CYC_8GN_1.0P2_0_vq.py",
    "Combinational-Mapping-3": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler/main/circuits-code//combinational/mapping/20QBT_8CYC_16GN_1.0P2_0_vq.py",  
    "Popular-dj-1": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler/main/circuits-code//combinational/popularalgorithms/Deutsch-Jozsa/Deutsch-Jozsa_qcraft.py"
}


num_repeticiones = 147 #147 

base_urls = list(set(urls.values()))  # sin duplicados
random_urls = base_urls * num_repeticiones  # repetir n veces

# Políticas y criterios
policies = ["MaxML", "MaxPD", "time_maquinas"]
criterios = [1, 2, 3]
acum=0

async def post_request(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()

async def main():
    global acum
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url_value in random_urls:
            time_policy_data = {
                "url": url_value,
                "shots": 10000,
                "provider": ['ibm'],
                "policy": "multibatch", #time o batch o multibatch
                "criterio": 0,
                "callback_url": "Url del servidor"
            }
           
            print(f"Enviando petición con datos: {time_policy_data}")
            acum += 1
            print(f"ACUMMMM: {acum}")
            task = post_request(session, url + pathCircuit, time_policy_data)
            tasks.append(task)
                    

        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)
            
asyncio.run(main())