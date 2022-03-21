from librapage.basepage import BasePage

from librapage.personal_board import PersonalBoardPage


class HomePage(BasePage):
    title = "BOSS首页"
    # pages = {
    #     "我的目标": "/newlibra/board/personal-board",
    #     "下属目标": "/newlibra/board/principal-board"
    # }
    personal_board = "/newlibra/board/personal-board"
    principal_board = "/newlibra/board/principal-board"

    def enter_personal_board(self):
        self.open(HomePage.personal_board)
        return PersonalBoardPage(self.driver)

    # def enter_principal_board(self):
    #     self.open(HomePage.principal_board)
