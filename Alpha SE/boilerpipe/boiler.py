import os


def handle(path, index):
    os.system("java -jar boilerpipe/boilerpipe.jar {0} > {1}".format(os.path.join(path, index + '.html'),
                                                                     os.path.join(path, index + '.txt')))
    os.unlink(os.path.join(path, index + '.html'))
