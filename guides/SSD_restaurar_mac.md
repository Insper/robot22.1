# Como restaurar o SSD - versão MAC

Este guia serve para você reinstalar o SSD Linux que foi emprestado pelo Insper se ele estiver corrompido. Esta é a versão Mac, existe uma versão Windows. 

Os pré-requisitos para esta recuperação são ter 54 GB de espaço temporário em algum disco.

**Se você não tiver este espaço** pode fazer as etapas de 1 a 5 usando o espaço do próprio SSD e depois copiar o robot.7z para onde você tiver espaço (aí precisa ter 27GB livres)

Aviso: **Você pode ter perda séria de dados ou de seu sistema operacional principal. Faça com muita atenção**

## 1. Primeiro passo - descobrir o id do SSD: 

Conecte o SSD de 128GB que foi cedido pela disciplina. 

Abra o terminal do Mac

Dê o comando `diskutil list` para descobrirmos qual é o **id** do SSD de 128GB. A listagem abaixo é  *apenas um exemplo*

    Woxpro:~ mirwox$ diskutil list
    /dev/disk0 (internal, physical):
    #:                       TYPE NAME                    SIZE       IDENTIFIER
    0:      GUID_partition_scheme                        *500.3 GB   disk0
    1:                        EFI EFI                     209.7 MB   disk0s1
    2:                 Apple_APFS Container disk1         500.1 GB   disk0s2

    /dev/disk1 (synthesized):
    #:                       TYPE NAME                    SIZE       IDENTIFIER
    0:      APFS Container Scheme -                      +500.1 GB   disk1
                                    Physical Store disk0s2
    1:                APFS Volume Macintosh HD            432.2 GB   disk1s1
    2:                APFS Volume Preboot                 21.3 MB    disk1s2
    3:                APFS Volume Recovery                515.0 MB   disk1s3
    4:                APFS Volume VM                      7.5 GB     disk1s4

 
    /dev/disk6 (external, physical):
    #:                       TYPE NAME                    SIZE       IDENTIFIER
    0:      GUID_partition_scheme                        *128.0 GB   disk6
    1:       Microsoft Basic Data                         1.0 MB     disk6s1
    2:        Bios Boot Partition                         1.0 MB     disk6s2
    3:                        EFI usbboot                 255.9 MB   disk6s3
    4:           Linux Filesystem                         119.8 GB   disk6s5

Vemos pela listagem acima que o disco marcado como **external, physical** e que tem 128GB é o id  `/dev/disk6` (em alguns comandos vamos usar como `/dev/rdisk6`). 

**Anote o id do disco**. Cuidado que este id pode mudar se você rebootar ou se o computador entrar em *power saving*, portanto refaça a etapa acima se não estiver conduzindo o guia todo de uma vez.


## 2. Faça o download

Baixe os arquivos disponíveis neste link do Teams de Robótica [https://alinsperedu.sharepoint.com/:f:/s/RobticaComputacional1.osem2020/ErQKW7yXobFAmFHg8BwAPxYBfaokIcEWyYUZWNz_qtZl3g?e=ULgvFE](https://alinsperedu.sharepoint.com/:f:/s/RobticaComputacional1.osem2020/ErQKW7yXobFAmFHg8BwAPxYBfaokIcEWyYUZWNz_qtZl3g?e=ULgvFE)

**Não importa onde você baixe**, desde que saiba abrir o terminal na pasta.

Você precisa fazer parte do grupo de robótica no Ms-Teams para poder baixar


## 3. Verificar integridade do download 


Depois de baixar, você terá os seguintes arquivos:

robot.7z.md5	robot.7z_aa	robot.7z_ab

Coloque-se na mesma pasta em que estes arquivos estão usando o terminal. Dê o seguinte comando:

    md5 robot.7z_* 

Se os valores que você obtiver forem **diferentes** dos que estão mostrados abaixo, significa que seu **download foi corrompido** e você vai precisar baixar de novo.

    Woxpro:tmp mirwox$ md5 robot.7z_* 
    MD5 (robot.7z_aa) = b1c47392d12e2b70d69eab62ef9c3578
    MD5 (robot.7z_ab) = aa8b0f2c5534d7260530de7675353e3e

## 4. Juntar os arquivos

Digite no terminal:

    cat robot.7z_a* > robot.7z

Você vai verificar que apareceu um arquivo `robot.7z`no seu diretório.

    Woxpro:tmp mirwox$ ls
    robot.7z

Se isso aconteceu, agora você já pode apagar os arquivos baixados:

    rm robot.7z_aa
    rm robot.7z_aa

## 5. Verificar se tem ou instalar o p7zip

Digite no seu terminal:

    7z --help

Se a resposta começar assim significa que você tem o programa:

    7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
    p7zip Version 16.02 (locale=utf8,Utf16=on,HugeFiles=on,64 bits,8 CPUs x64)

    Usage: 7z <command> [<switches>...] <archive_name> [<file_names>...]
        [<@listfiles...>]

    <Commands>
    a : Add files to archive
    b : Benchmark
    d : Delete files from archive
    e : Extract files from archive (without using directory names)
    h : Calculate hash values

Se a resposta for assim:

    -bash: 7z: command not found

Significa que você *não tem** o 7z. Daí você [precisa instalar o homebrew](https://brew.sh/) e depois instalar 7z usando o comando `brew install p7zip`. 

## 6. Desmontar o disco de 128GB sem ejetar

Você precisa **desmontar** o disco de 128GB para que o MacOS pare de usá-lo e possamos regravá-lo a nível de bit.

Agora você vai precisar do **id** que anotou acima. No caso deste guia o id era `/dev/disk6`

    diskutil unmountDisk /dev/disk6

A mensagem que deve vir é a seguinte:

    Unmount of all volumes on disk6 was successful

## 7. Extrair o arquivo 7z e restaurar diretamente o SSD

Verifique se o arquivo 7z está na pasta em que estava trabalhando:

    Woxpro:tmp mirwox$ ls robot.7z
    robot.7z

Lembre-se do **id** do disco que anotou no primeiro passo. Agora vamos usar a versão que tem letra `r`, e que será `/dev/rdisk6`

Note que você realmente precisa ter anotado o **id**, e que se no seu computador você usar o errado poderá perder seu sistema operacional e dados:


    7z e -so robot.7z | sudo dd of=/dev/rdisk6 bs=4m

Digite a senha de sudo para o comando prosseguir. 

Aguarde terminar. Deve levar cerca de 2 horas.

Exemplo de como deve ficar ao terminar:

    Woxpro:tmp mirwox$ 7z e -so robot.7z | sudo dd of=/dev/rdisk6 bs=4m
    Password:
    0+1953792 records in
    0+1953792 records out
    128043712512 bytes transferred in 2590.049041 secs (49436791 bytes/sec)                     


## 8. Remova o SSD

Use o comando `diskutil eject` para poder ejetar o disco de forma segura. Novamente aqui você vai precisar do **id** do disco:

    Woxpro:tmp mirwox$ diskutil eject /dev/disk6
    Disk /dev/disk6 ejected

## 9. Boot pelo SSD 

Agora tente fazer o *boot* pelo SSD

# Final

Lembre-se de [instalar o Git LFS](https://github.com/Insper/robot20/blob/master/guides/git_lfs.md) quando bootar pelo SSD. 