## Como Funciona o Jogo 🎮

### Objetivo Principal 🎯
  - Sobreviver o máximo de tempo possível, desviando-se dos inimigos que aparecem.

  - Acumular a maior pontuação. 🏆

### Controles ⌨️
  - Movimento: Use as teclas de setas ou as teclas W, A, S, D para mover o seu personagem (o polvo).

## Mecânicas de Jogo ⚙️

### Inimigos 👾:
  - Aparecem aleatoriamente nas bordas da janela.

  - Perseguem a sua posição atual. A perseguição é mais "inteligente" e direta se você estiver parado.

### Sistema de Vidas ❤️:

  - Você começa com 3 vidas.

  - Perde uma vida ao colidir com um inimigo (arraias, predador natural do polvo).

  - Após ser atingido, você fica invencível por 2 segundos.

### Itens de Vida (Corações) 💖:

  - Aparecem aleatoriamente se você tiver menos de 3 vidas.

  - Têm um comportamento de "fuga" (afastam-se quando você se aproxima).

  - Ao coletar um, você recupera uma vida.

## Pontuação (Score) ⭐:

  - Você ganha 1 ponto sempre que um inimigo sai da janela.

## Dificuldade 📈:

  - A cada 5 pontos no score, a velocidade dos inimigos e a sua capacidade de perseguição aumentam.

## Menu 🖥️
  - Start Game: Inicia uma nova partida.

  - Exit: Fecha o jogo.

  - Slider de Volume: Controla o volume da música de fundo.

## Fim de Jogo (Game Over) 💀
  - Ocorre quando você perde todas as suas vidas.

  - Mostra a sua pontuação final e o tempo que sobreviveu.

  - Oferece as opções de voltar ao menu principal ou sair do jogo.

## Rodar o Jogo 🚀

Passo 1: Instalar o Biblioteca Pygame Zero

```bash
pip install pgzero
```

Passo 2: Rodar o Jogo

```bash
pgzrun main.py
```
