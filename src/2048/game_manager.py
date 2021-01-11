from game import Game

def main():
    size = 400, 400

    try:
        with open('best.txt', 'r') as f:
            best = int(f.read())
    except Exception:
        with open('best.txt', 'w') as f:
            f.write('0')
            best = 0

    game = Game(size, best=best)
    game.run()
    

if __name__ == '__main__':
    main()
