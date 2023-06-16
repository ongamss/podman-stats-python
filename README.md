# podman-stats-python
O [podman](https://podman.io/) é uma alternativa altamente recomendada em vez dos contêineres do Docker quando você busca maior segurança, isolamento de identificador exclusivo (UID) por meio de namespaces e integração com o systemd.
Nesse painel de monitoramento feito em python é exibido as métricas do pods criados o comando 'podman run', onde os pods com uso de memória ou cpu entre 70% a 80% ficam marcados com a cor laranja e acima de 80% vermelho.
- Exemplo de criação de dois pods:
## criação de pod1 com imagem nginx
```
sudo podman run -d --name nx1 -m 256m --cpus=1 -p 9004:80 nginx
```
## criação de pod2 com imagem nginx
```
sudo podman run -d --name nx2 -m 256m --cpus=1 -p 9004:80 nginx
```
Para simular o cenário de uso de recursos foi utilizando o comando stress via prompt de comando nos pods em executção:
```
stress --cpu 1 --io 4 --vm 4 --vm-bytes 128M --timeout 120s
```
## Instalação
```
sudo pip3 install -r requirements.txt
```
## Execução
```
sudo python3 monitor.py
```
Acesse no browser o endereço: http://127.0.0.1:8050 para visualização do painel
![Podman-stats1](https://github.com/ongamss/podman-stats-python/assets/70037523/fc76c978-df5b-43b1-94bc-8ee6d0eb20ca)

