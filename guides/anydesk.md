# Conserto Anydesk

Para abrir o `Anydesk` digite no terminal:

    anydesk

O ID do seu computador não é único.Para fazer ser único por favor faça: 

    sudo rm /etc/anydesk/service.conf

Depois digite no terminal:

    wget -qO - https://raw.githubusercontent.com/Insper/404/master/desktop%20ssd/patchs/patch_0_anydesk_chrome.sh | bash

Depois *reinicie o computador*:

    sudo reboot
