* Verificar a versão do pip. A versão usada é a 25.1.1
`pip3 --version`

* Se estiver desatualizado:
`python3 -m pip install --upgrade pip`

* Instalar o gerenciador de pacotes e ambiente `uv`: 
`python3 -m pip install uv`

* Se já possuir o `uv`, fazer o upgrade. A versão usada é a 0.8.22.
`python3 -m pip install --upgrade uv`

* Verificar a versão do `uv`:
`uv --version`

* Verificar versões do Python instaladas:
`uv python list`

* Instalar a versão 3.11
`uv python install 3.11`

* Fixar a versão desejada para iniciar o projeto. Neste caso a 3.11: 
`uv python pin 3.11`

* Cria um projeto dentro do diretório escolhido: 
`uv init tech_challenge_fase_03`

* Cria um ambiente virtual
`uv venv`

* Ativa o ambiente virtual 
`source .venv/bin/activate`

* Modifica a versão do python dentro de pyproject.toml
`requires-python = ">=3.11"`

* Instalar as dependência do cookiecutter no ambiente
`uv add cookiecutter`

* Criar o template
`cookiecutter gh:drivendata/cookiecutter-data-science -c v1`

* Adiciona o ipykernel
`uv add ipykernel`