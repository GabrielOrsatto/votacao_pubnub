from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import os

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-fbf348af-ded5-4280-9373-6c7117f3fe6c'
pnconfig.subscribe_key = 'sub-c-825aa364-9989-4fa3-a933-3792c3e0892a'
pnconfig.uuid = input("Seu nome: ")
pubnub = PubNub(pnconfig)
canal = 'votacao_teste'
votos = {}

class VotacaoCallback(SubscribeCallback):
    def message(self, pubnub, message):
        opcao = message.message['opcao']
        votos[opcao] = votos.get(opcao, 0) + 1
        print(f"Voto recebido: {opcao} | Total: {votos}")

pubnub.add_listener(VotacaoCallback())
pubnub.subscribe().channels(canal).execute()

def votar():
    while True:
        print("\nOpções: A, B, C (ou aperte Ctrl + C para encerrar)")
        escolha = input("Vote agora: ").strip().upper()
        if escolha in ['A', 'B', 'C']:
            pubnub.publish().channel(canal).message({'opcao': escolha}).sync()
        else:
            print("Opção inválida.")

try:
    votar()
except KeyboardInterrupt:
    print("\nInterrompido pelo usuário. Saindo...")
    os._exit(0)
