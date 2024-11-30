# Local Video Streaming

Um aplicativo web simples em Django para streaming de vídeos locais. O aplicativo monitora uma pasta específica e exibe automaticamente os vídeos em uma interface web amigável.

## Características

- Interface responsiva para listar vídeos
- Reprodutor de vídeo integrado
- Miniaturas automáticas dos vídeos
- Suporte para formatos comuns (.mp4, .avi, .mov, .mkv)
- Atualização automática quando novos vídeos são adicionados à pasta

## Requisitos

- Python 3.12+
- Django 5.1.3+
- python-dotenv

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pedrohenriqueperes/streaming.git
cd streaming
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install django python-dotenv
```

4. Crie um arquivo .env na raiz do projeto:
```bash
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie a pasta para os vídeos:
```bash
mkdir videos_folder
```

## Uso

1. Inicie o servidor:
```bash
python manage.py runserver
```

2. Coloque seus vídeos na pasta `videos_folder`

3. Acesse http://localhost:8000 no seu navegador

## Estrutura do Projeto

```
streaming/
├── manage.py
├── streaming/
├── videos/
├── templates/
│   └── videos/
│       ├── video_list.html
│       └── video_detail.html
├── videos_folder/
├── .env
└── README.md
```

## Extensões de Vídeo Suportadas

- .mp4
- .avi
- .mov
- .mkv

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Autor

Pedro Henrique Peres - [pedrohenriqueperes](https://github.com/pedrohenriqueperes)

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.