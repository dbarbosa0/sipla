# SIPLA
O SIPLA é uma interface gráfica para a integração entre o Banco de Dados Geográficos da Distribuidora (BDGB) no padrão definido pelo [PRODIST- Módulo 10](https://www.aneel.gov.br/modulo-10) da [ANEEL](https://www.aneel.gov.br) com o [OpenDSS](http://smartgrid.epri.com/SimulationTool.aspx) escrito em [Python 3](https://www.python.org)


## Instalação
Para executar o software, os seguintes pacotes são necessários:

```
pip install PyQt5
pip install PyQtWebEngine
pip install numpy
pip install scipy
pip install matplotlib
pip install Unidecode
pip install mysqlclient
```


```
pip install git+https://github.com/pyqtgraph/pyqtgraph@develop
pip install folium
pip install 'OpenDSSDirect.py[extras]'
```

### [Microsoft Windows](https://www.microsoft.com/windows/)
Para utilização do OpenDSS via [_Component Object Model_ (COM)](https://docs.microsoft.com/en-us/windows/win32/com/component-object-model--com--portal), é necessário instalar o _software_ OpenDSS e os seguintes pacotes adicionais no Python:

```
pip install pywin32
```

**Recomendação**: Verifique a instalação utilizando o _script_ _dssvplot35.py_ na pasta "Examples" do OpenDSS.

### GNU Linux
Para utilização no GNU Linux, verifique se os pacotes não podem ser instalados via gerenciador de pacotes ao invés do pip, visto que assim evita-se erros posteriores.

###### Arch Linux
```
python-pip
python-pyqt5
python-pyqt5-webengine
python-numpy
python-scipy
python-matplotlib
python-unidecode
python-mysqlclient
pip install 'OpenDSSDirect.py[extras]'
pip install git+https://github.com/pyqtgraph/pyqtgraph@develop
```


## Desenvolvimento 
O desenvolvimento é coordenado pela [G-SEPi](https://www.ligasep.eng.ufba.br/) da [UFBA](https://www.ufba.br/)

### Agradecimentos
Agradecimentos especiais a Sandy Aquino, Felipe Bomfim e Matheus Carvalho pelas importantes contribuições
