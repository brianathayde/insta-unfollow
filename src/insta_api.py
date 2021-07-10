import sys
import colorama

from instaloader import instaloader
from instaloader.exceptions import BadCredentialsException
from instaloader.instaloadercontext import InstaloaderContext
from instaloader.nodeiterator import NodeIterator
from instaloader.structures import Profile

from getpass import getpass

from src.user import User
from src.printer import Printer

class InstaAPI:
    # * Inicializa a classe Instaloader e autentica o usuário com a API
    def __init__(self) -> None:
        username = str(input('Login/Usuário do Instagram: '))
        password = str(getpass('Senha: '))

        self.user = User(username, password)
        
        colorama.init() 

    # * Retorna todas as contas a quem o usuário logado segue
    def get_followees(self, context: InstaloaderContext, username: str) -> NodeIterator[Profile]:
        try:
            profile = instaloader.Profile.from_username(context, username)

            return profile.get_followees()
        except Exception as error:
            Printer.error(str(error))
            sys.exit()

    # * Retorna todas as contas a quem o usuário logado é seguido
    def get_followers(self, context: InstaloaderContext, username: str) -> NodeIterator[Profile]:
        try:
            profile = instaloader.Profile.from_username(context, username)

            return profile.get_followers()
        except Exception as error:
            Printer.error(str(error))
            sys.exit()

    def run(self):
        insta_loader = instaloader.Instaloader()

        try:
            insta_loader.login(self.user.username, self.user.password)
        except Exception as error:
            Printer.error(str(error))
            sys.exit()

        Printer.primary('Buscando seguidores...')
        followers = self.get_followers(insta_loader.context, self.user.username)

        Printer.primary('Buscando quem você segue...')
        followees = self.get_followees(insta_loader.context, self.user.username)

        followers_list = []
        followees_list = []

        Printer.primary('Verificando as listas...')

        Printer.primary('Armazenando seguidores...')
        for follower in followers:
            followers_list.append(follower.username)

        Printer.primary('Armazenando quem você está seguindo...')
        for followee in followees:
            followees_list.append(followee.username)
        
        Printer.primary('Buscando e armazenando a interseção entre os usuários que você segue mas que não o seguem de volta...')
        # * Lista de interseção entre que o usuário da sessão segue mas que não o seguem de volta
        intersect_users_list = list(set(followees_list) - set(followers_list))
        
        file = open('reports/' + self.user.username + '.txt', 'w')

        Printer.primary('Criando relatório...')

        for username in intersect_users_list:
            file.write(username + '\n')

        file.close()

        Printer.primary('Operação finalizada... arquivo: ' + self.user.username + '.txt criado!')

        sys.exit()
        
        