# TesteDSIN

## Requisitos
- Python 3.12.0

## Setup

``` 
git clone https://github.com/marcoshronzani/TesteDSIN.git
cd TesteDSIN
cp contrib\env-sample .env
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver
```

## Acesso ao Sistema

O setup acima já cria e popula o banco de dados com três usuários, alguns agendamentos e serviços.

Usuário Admin
````
leila@cabeleleila.com.br
````
Senha Admin
````
leila
````

Usuário Cliente 1
````
marcosronzani@gmail.com
````
Senha Cliente 1
````
Marcos123
````

Usuário Cliente 2
````
amandaronzani@gmail.com
````
Senha Cliente 2
````
Amanda123
````

## Fotos
### Tela_Cadastro
![Tela_Cadastro](./FOTOS_SISTEMA/01-Tela_Cadastro.png "Tela_Cadastro")

### Tela_Login
![Tela_Login](./FOTOS_SISTEMA/02-Tela_Login.png "Tela_Login")

### Tela_Menu_Cliente
![Tela_Menu_Cliente](./FOTOS_SISTEMA/03-Tela_Menu_Cliente.png "Tela_Menu_Cliente")

### Tela_Agendamentos_Cliente
![Tela_Agendamentos_Cliente](./FOTOS_SISTEMA/04-Tela_Agendamentos_Cliente.png "Tela_Agendamentos_Cliente")

### Tela_Cadastro_Agendamento_Cliente
![Tela_Cadastro_Agendamento_Cliente](./FOTOS_SISTEMA/05-Tela_Cadastro_Agendamento_Cliente.png "Tela_Cadastro_Agendamento_Cliente")

### Tela_Editar_Agendamento_Cliente
![Tela_Editar_Agendamento_Cliente](./FOTOS_SISTEMA/06-Tela_Editar_Agendamento_Cliente.png "Tela_Editar_Agendamento_Cliente")

### Tela_Menu_Adm
![Tela_Menu_Adm](./FOTOS_SISTEMA/10-Tela_Menu_Adm.png "Tela_Menu_Adm")

### Tela_Aprovação_Adm
![Tela_Aprovação_Adm](./FOTOS_SISTEMA/11-Tela_Aprovação_Adm.png "Tela_Aprovação_Adm")

### Tela_Agendamentos_Adm
![Tela_Agendamentos_Adm](./FOTOS_SISTEMA/12-Tela_Agendamentos_Adm.png "Tela_Agendamentos_Adm")

### Tela_Editar_Agendamento_Adm
![Tela_Editar_Agendamento_Adm](./FOTOS_SISTEMA/13-Tela_Editar_Agendamento_Adm.png "Tela_Editar_Agendamento_Adm")

### Tela_Confirma_Exclusão_Agendamento_Adm
![Tela_Confirma_Exclusão_Agendamento_Adm](./FOTOS_SISTEMA/14-Tela_Confirma_Exclusão_Agendamento_Adm.png "Tela_Confirma_Exclusão_Agendamento_Adm")

### Tela_Serviços_Adm
![Tela_Serviços_Adm](./FOTOS_SISTEMA/15-Tela_Serviços_Adm.png "Tela_Serviços_Adm")

### Tela_Cadastro_Serviço_Adm
![Tela_Cadastro_Serviço_Adm](./FOTOS_SISTEMA/16-Tela_Cadastro_Serviço_Adm.png "Tela_Cadastro_Serviço_Adm")

### Tela_Editar_Serviço_Adm
![Tela_Editar_Serviço_Adm](./FOTOS_SISTEMA/17-Tela_Editar_Serviço_Adm.png "Tela_Editar_Serviço_Adm")

### Tela_Acompanhamento_Adm
![Tela_Acompanhamento_Adm](./FOTOS_SISTEMA/18-Tela_Acompanhamento_Adm.png "Tela_Acompanhamento_Adm")