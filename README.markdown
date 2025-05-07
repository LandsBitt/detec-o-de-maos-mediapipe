# Detecção de Mãos com MediaPipe

Este projeto utiliza o **MediaPipe**, uma biblioteca desenvolvida pelo Google, para detecção e rastreamento de mãos em tempo real. A aplicação captura vídeo da câmera e desenha as *landmarks* das mãos detectadas.

## Funcionalidades

- Detecção e rastreamento de mãos em tempo real
- Desenho das conexões entre *landmarks* das mãos
- Exibição do vídeo com as mãos detectadas

## Como Rodar o Projeto

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/detecao-de-maos-mediapipe.git](https://github.com/LandsBitt/detec-o-de-maos-mediapipe.git)
```

### 2. Instalar as Dependências

Se estiver usando um ambiente virtual, ative-o e instale as dependências:

```bash
pip install -r requirements.txt
```

**Dependências necessárias**:
- `opencv-python`: Para captura de vídeo e manipulação de imagens
- `mediapipe`: Para detecção e rastreamento de mãos

### 3. Executar o Código

Rode o projeto com:

```bash
python main.py
```

### 4. Sair do Programa

Pressione a tecla `q` durante a execução para fechar a aplicação.

## Dependências

- `opencv-python`
- `mediapipe`

## Como Adicionar Novas Dependências

Para adicionar uma nova dependência:

```bash
pip install <nome-da-dependência>
```

Salve as dependências no arquivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um *fork* do repositório
2. Realize suas alterações
3. Crie um *pull request*