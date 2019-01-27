import mercury


def main():
    if mercury.isMaya():
        from mercury.qtlib import MercuryWidget
        window = MercuryWidget()
    return window
