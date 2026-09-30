# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time # jy 추가

class RunawayGame:
    def __init__(self, canvas, runner: turtle.RawTurtle, chaser: turtle.RawTurtle, catch_radius=50, time_limit=60):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        #self.start_time = time.time() # jy 추가
        self.time_limit = time_limit; # jy 추가 : 게임 종료 시간(60초), 이 시간동안 잡을때마다 1점씩 증가

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        #self.runner.setpos((-init_dist / 2, 0))
        #self.runner.setheading(0)
        #self.chaser.setpos((+init_dist / 2, 0))
        #self.chaser.setheading(180)
        self.init_dist = init_dist
        self._reset_pos()

        # TODO) You can do something here and follows.
        self.score = 0
        self.start_time = time.time()

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def _reset_pos(self):
        self.runner.setpos((-self.init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+self.init_dist / 2, 0))
        self.chaser.setheading(180)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        remain = self.time_limit - (time.time() - self.start_time) # jy 추가

        is_catched = self.is_catched()
        dist = self.runner.distance(self.chaser)

        if is_catched:
            self.score += 1
            # 잡혔으면 다시 멀리 떨어뜨려 배치
            self._reset_pos()

        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched} / Distance: {dist:.1f} (need < {self.catch_radius2**0.5:.0f}) / Remain: {remain:.1f} / score: {self.score}') # jy 수정

        if remain <= 0:
            self.drawer.undo()
            self.drawer.setpos(-300, 260)
            self.drawer.write(f'Game over! Final Score: {self.score}')
            return

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn) 

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    #runner = RandomMover(screen)
    runner = RandomMover(screen, 10, 10) #runner turtle이 screen 밖으로 너무 빨리 나가는 것을 방지하기 위해 step_move를 10 -> 5로 줄임 
    #chaser = ManualMover(screen)
    chaser = ManualMover(screen, 10, 10)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
