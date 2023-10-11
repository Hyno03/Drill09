from pico2d import load_image, SDL_KEYDOWN, SDLK_a, get_time


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(boy):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class AutoRun:
    @staticmethod
    def enter(boy):
        boy.dir, boy.action = 1, 1
        boy.running = True
        boy.bigY, boy.width, boy.length = boy.y, 100, 100
        boy.speed = 1
        boy.run_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.width += 2
        boy.length += 2

        boy.speed += 0.25
        boy.x += boy.dir * boy.speed
        boy.bigY += 0.5

        if boy.x >= 780:
            boy.dir = -1
            boy.action = 0
        elif boy.x <= 20:
            boy.dir = 1
            boy.action = 1

        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.run_time > 2:
            boy.state_machine.handle_event(('TIME_OUT', 0))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.bigY, boy.width, boy.length)

class StateMachine:
    def __init__(self, boy):
        self.cur_state = Idle
        self.boy = boy
        self.transitions = {
            Idle: {a_down: AutoRun},
            AutoRun: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy)

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
