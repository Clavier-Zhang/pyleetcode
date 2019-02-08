from bs4 import BeautifulSoup
import click

class Screen:

    # helper methods
    def space(self, s, size):
        return ('{:'+str(size)+'}').format(s)

    def dash(self, s, size):
        return ('{:-<'+str(size)+'}').format(s)

    def print_difficulty(self, difficulty):
        if difficulty == 1 or difficulty == 'Easy':
            click.secho(self.space('Easy', 8), fg='bright_green', nl=False)
        if difficulty == 2 or difficulty == 'Medium':
            click.secho(self.space('Medium', 8), fg='bright_yellow', nl=False)
        if difficulty == 3 or difficulty == 'Hard':
            click.secho(self.space('Hard', 8), fg='bright_red', nl=False)
    
    def print_need_pay(self, need_pay):
        if need_pay:
            click.secho(self.space('$', 2), fg='bright_yellow', nl=False)
        else:
            click.secho(self.space('', 2), nl=False)

    def print_is_favor(self, is_favor):
        if is_favor:
            click.secho(self.space('❤', 2), fg='bright_magenta', nl=False)
        else:
            click.secho(self.space('', 2), nl=False)

    def print_status(self, status):
        if status == 'ac':
            click.secho(self.space('AC', 3), fg='bright_cyan', nl=False)
        else:
            click.secho(self.space('', 3), fg='bright_cyan', nl=False)
    
    def print_content(self, content):
        content =  BeautifulSoup(content, "html.parser")
        content = content.get_text().replace('Example:\n', '\nExample:')
        click.secho(content, fg='bright_white')
        
    # question methods
    def print_question_summarys(self, question_summarys):
        for question_summary in question_summarys:
            stat = question_summary['stat']
            
            question_id = self.space(str(stat['question_id']), 5)
            question_title = self.dash(stat['question__title'], 55)

            difficulty = question_summary['difficulty']['level']
            paid_only = question_summary['paid_only']
            is_favor = question_summary['is_favor']
            status = question_summary['status']
            
            click.secho(question_id, fg='bright_white', nl=False)
            click.secho(question_title, fg='bright_white', nl=False)
            self.print_difficulty(difficulty)
            self.print_need_pay(paid_only)
            self.print_is_favor(is_favor)
            self.print_status(status)
            click.secho('', fg='bright_white')

    def print_question_detail(self, question_detail):
        question_id = self.space(question_detail['questionId'], 5)
        title = self.space(question_detail['title'], 55)
        difficulty = question_detail['difficulty']
        likes = question_detail['likes']
        dislikes = question_detail['dislikes']
        status = question_detail['status']
        topicTags = question_detail['topicTags']

        content = question_detail['content']

        sampleTestCase = question_detail['sampleTestCase']

        click.secho(question_id, fg='bright_white', nl=False)
        click.secho(title, fg='bright_white', nl=False)
        print(difficulty)
        self.print_content(content)
        print(sampleTestCase)
