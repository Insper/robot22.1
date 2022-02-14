# Widgets no Jupyterlab 3

Alguns notebooks (por exemplo da aula 02) usam componentes interativos.

Estes widgets funcionam por padrão no Jupyter Notebook, que é mais antigo. Mas precisam ser ativados no Jupyter Lab.

Para instalar os widgets, siga os seguintes passos:

**1.** Certifique-se que está com o Jupyterlab 3. Se não estiver, faça:

Se estiver no conda:

    conda install -c conda-forge jupyterlab

Se estiver no Linux, faça: 

    pip install jupyterlab 


**2.** Instale o suporte aos widgets

Se estiver no conda e tiver um environment [chamado robotica](opencv_anaconda):

    conda install -n base -c conda-forge jupyterlab_widgets
    conda install -n base -c conda-forge ipywidgets
    conda install -n robotica -c conda-forge ipywidgets

   
 **No Linux fornecido instale via pip:**
 
    pip install ipywidgets
    pip3 install ipywidgets

