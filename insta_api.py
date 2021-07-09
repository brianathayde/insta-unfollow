import sys

from instaloader import instaloader
from instaloader.nodeiterator import NodeIterator
from instaloader.structures import Profile


from user import User
from getpass import getpass

class InstaAPI:
    # * Inicializa a classe Instaloader e autentica o usuário com a API
    def __init__(self) -> None:
        username = str(input('Login/Usuário do Instagram: '))
        password = str(getpass('Senha: '))

        self.user = User(username, password)
        self = self
        

    # * Retorna todas as contas a quem o usuário logado segue
    def get_followees(self) -> NodeIterator[Profile]:
        try:
            profile = instaloader.Profile.from_username(self.insta_loader.context, self.user.username)

            return profile.get_followees()
        except Exception as error:
            print(error)
            sys.exit()

    def get_followers(self) -> NodeIterator[Profile]:
        try:
            profile = instaloader.Profile.from_username(self.insta_loader.context, self.user.username)

            return profile.get_followers()
        except Exception as error:
            print(error)
            sys.exit()

    def run(self):
        self.insta_loader = instaloader.Instaloader()
        try:
            self.insta_loader.login(self.user.username, self.user.password)
        except Exception as error:
            print('erro inicio')
            sys.exit()

        print('vai pra l1')
        l1 = self.get_followers()
        print('vai pra l2')
        l2 = self.get_followees()

        usersimfollowing = []
        usersfollowingme = []

        print('vai pegar a primeira lista')
        # Retorna uma lista com os nomes de usuarios
        # Precisa criar uma nova lista porque demora e as vezes trava na hora de comparar com o get diretamente
        for followers in l1:
            usersfollowingme.append(followers)
            print("me segue: @" + followers.username)  
        print('vai pegar a segunda lista')  
        for followees in l2:
            usersimfollowing.append(followees)
            print("eu sigo: @" + followees.username)  


        # Lista com o usuários que nao seguem de volta
        # String que vai conter todos nomes     
        totxt = ""
        for imfollowing in usersimfollowing:
            following = False
            for followingme in usersfollowingme:
                if imfollowing.username == followingme.username:
                    following = True
                    break
            if following == False:
                print("@" + imfollowing.username)
                totxt += "@" + imfollowing.username + "\n"

        file = open("arrobasFinal.txt", "w") 
        file.write(totxt) 
        file.close()
        print('*******************')
        print('até logo!')
        print('*******************')
        sys.exit()
        
        