# Como criar um arquivo de swap

Um arquivo de *swap* serve como memória virtual e complementa a memória do sistema. Por padão do Ubuntu, temos 2GB de *swap*. Nós vamos aumentar esse espaço para 8GB.  

Abra um terminal *Crtl+Alt+t* e vamos visualizar a quantidade de *memoria* e o *swap* atual com o comando: 

	free -h

Primeiramente vamos desativar *swap*:

	sudo swapoff -a

Agora vamos dar um resize no arquivo *swapfile* e criar um swap de 8GB.

	sudo dd if=/dev/zero of=/swapfile bs=1M count=8192

Agora vamos transformar o arquivo em um arquivo de *swap*:

	sudo mkswap /swapfile

E por último vamos ativá-lo:

	sudo swapon /swapfile

Vamos reiniciar o computador para testar:

	reboot

Para verificar isso, usamos o comando:

	free -h
