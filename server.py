import icetracker

if __name__ == '__main__':
    icetracker.Config(path="./config.json")
    icetracker.WSGI().start("0.0.0.0", 8001)
