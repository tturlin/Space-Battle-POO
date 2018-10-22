# -*- coding: utf-8 -*-
from black_hole import *
import constants as c
import functions as f
from spacecraft import *
from shots import *

import matplotlib
#matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.projections import polar
import numpy as np
import tkinter
import tkinter.messagebox


class App():
    """
    This class is used to create and manage the entire GUI of the game.
    """

    def __init__(self):
        """Initialisation of the window."""
        # Defining some variable thaat need to be initialized
        self.object = []
        self.action = 1
        self.angle_shot = -1
        self.hole = Black_hole(100)

        # Creation of the window and configuration of general settings
        self.window = tkinter.Tk(className=' Space Battle')
        self.window.geometry("%dx%d+0+0" % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.grid_propagate(flag=0)
        self.window.columnconfigure(0, minsize=300)
        self.window.columnconfigure(1, minsize=self.window.winfo_screenwidth()-600)
        self.window.columnconfigure(2, minsize=300)

        maxwidth=int(self.window.winfo_screenwidth()-50)

        # Creating the game option zone
        self.game_opt = tkinter.LabelFrame(self.window, text='Game options', width=maxwidth, height=100)
        self.game_opt.grid(row=0, column=0, columnspan=3, padx=25, pady=5)
        self.game_opt.grid_propagate(flag=0)
        numberofplayer = tkinter.Label(self.game_opt, text='Number of player (one will set a target that\'s just moving)')
        numberofplayer.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Creating the selection of the number of player
        nb = [1, 2]
        self.nb_player = tkinter.DoubleVar()
        self.nb_player.set(nb[0])
        self.nb1 = tkinter.Radiobutton(self.game_opt, variable=self.nb_player, text='Solo', value=nb[0], command=lambda : self.one_player())
        self.nb1.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.nb2 = tkinter.Radiobutton(self.game_opt, variable=self.nb_player, text='2 Players', value=nb[1], command=lambda : self.two_player())
        self.nb2.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Creating the selection of the limit condition
        zoninglabel = tkinter.Label(self.game_opt, text='Which exit of game zone would you like ?')
        zoninglabel.grid(row=0, column=2, padx=150, pady=5, sticky='ew')
        zoning = ['limit', 'speed']
        self.limit_game = tkinter.DoubleVar()
        self.limit_game.set(zoning[0])
        self.zoning1 = tkinter.Radiobutton(self.game_opt, variable=self.limit_game, text='Speed liberation', value=zoning[1])
        self.zoning1.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.zoning2 = tkinter.Radiobutton(self.game_opt, variable=self.limit_game, text='Limit condition', value=zoning[0])
        self.zoning2.grid(row=1, column=3, padx=5, pady=5, sticky='w')


        # Creating the player one frame
        self.p1 = tkinter.LabelFrame(self.window, text='Player 1', width=250, height=225)
        self.p1.grid(row=1, column=0, padx=5, pady=5)
        self.p1.grid_propagate(0)

        # creating inputs for the Spacecraft
        self.dist1 = tkinter.DoubleVar()
        self.dist1.set(50.0)
        self.p1_dist1_text = tkinter.Label(self.p1, text='Distance to the EH, in Rs :')
        self.p1_dist1_text.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.p1_dist = tkinter.Entry(self.p1, textvariable=self.dist1, width=5)
        self.p1_dist.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.vr1 = tkinter.DoubleVar()
        self.vr1.set(0.1)
        self.p1_vr1_text = tkinter.Label(self.p1, text='Radial speed, in c :')
        self.p1_vr1_text.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.p1_vr1 = tkinter.Entry(self.p1, textvariable=self.vr1, width=5)
        self.p1_vr1.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.vt1 = tkinter.DoubleVar()
        self.vt1.set(0.1)
        self.p1_vt1_text = tkinter.Label(self.p1, text='Tangential speed, in c :')
        self.p1_vt1_text.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.p1_vt1 = tkinter.Entry(self.p1, textvariable=self.vt1, width=5)
        self.p1_vt1.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.hs_text1 = tkinter.Label(self.p1, text='Heavy shot remaining :')
        self.hs_text1.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.hs1 = tkinter.Label(self.p1, text='')
        self.hs1.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.ls_text1 = tkinter.Label(self.p1, text='Light shot remaining :')
        self.ls_text1.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.ls1 = tkinter.Label(self.p1, text='')
        self.ls1.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        self.validate1 = tkinter.Button(self.p1, text='Validate', command=lambda : self.spacecraft1_init())
        self.validate1.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Creating the player two frame
        self.p2 = tkinter.LabelFrame(self.window, text='Player 2', width=250, height=225)
        self.p2.grid(row=1, column=2, padx=5, pady=5)
        self.p2.grid_propagate(0)

        # creating inputs for the Spacecraft
        self.dist2 = tkinter.DoubleVar()
        self.dist2.set(50.0)
        self.p2_dist2_text = tkinter.Label(self.p2, text='Distance to the EH, in Rs :')
        self.p2_dist2_text.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.p2_dist = tkinter.Entry(self.p2, textvariable=self.dist2, width=5, state='disable')
        self.p2_dist.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.vr2 = tkinter.DoubleVar()
        self.vr2.set(0.1)
        self.p2_vr2_text = tkinter.Label(self.p2, text='Radial speed, in c :')
        self.p2_vr2_text.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.p2_vr2 = tkinter.Entry(self.p2, textvariable=self.vr2, width=5, state='disable')
        self.p2_vr2.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.vt2 = tkinter.DoubleVar()
        self.vt2.set(0.1)
        self.p2_vt2_text = tkinter.Label(self.p2, text='Tangential speed, in c :')
        self.p2_vt2_text.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.p2_vt2 = tkinter.Entry(self.p2, textvariable=self.vt2, width=5, state='disable')
        self.p2_vt2.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.hs_text2 = tkinter.Label(self.p2, text='Heavy shot remaining :')
        self.hs_text2.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.hs2 = tkinter.Label(self.p2, text='')
        self.hs2.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.ls_text2 = tkinter.Label(self.p2, text='Light shot remaining :')
        self.ls_text2.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.ls2 = tkinter.Label(self.p2, text='')
        self.ls2.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        self.validate2 = tkinter.Button(self.p2, text='Validate', state='disable', command=lambda : self.spacecraft2_init())
        self.validate2.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Creating actions for player one
        self.p1_act = tkinter.LabelFrame(self.window, text='Action', width=250, height=180)
        self.p1_act.grid(row=2, column=0, padx=5, pady=5)
        self.p1_act.grid_propagate(0)
        self.p1_act.columnconfigure(0, minsize=250)


        self.wait1 = tkinter.Button(self.p1_act, text='Wait', command=lambda : self.wait(self.player1))
        self.wait1.grid(row=0, column=0, padx=25, pady=10, sticky='ew')

        self.lightshot1 = tkinter.Button(self.p1_act, text='Light shot', command=lambda : self.light_shot(self.player1))
        self.lightshot1.grid(row=1, column=0, padx=25, pady=10, sticky='ew')

        self.heavyshot1 = tkinter.Button(self.p1_act, text='Heavy shot', command=lambda : self.heavy_shot(self.player1))
        self.heavyshot1.grid(row=2, column=0, padx=25, pady=10, sticky='ew')

        # Creating actions for player two
        self.p2_act = tkinter.LabelFrame(self.window, text='Action', width=250, height=180)
        self.p2_act.grid(row=2, column=2, padx=5, pady=5)
        self.p2_act.grid_propagate(0)
        self.p2_act.columnconfigure(0, minsize=250)


        self.wait2 = tkinter.Button(self.p2_act, text='Wait', state='disable', command=lambda : self.wait(self.player2))
        self.wait2.grid(row=0, column=0, padx=25, pady=10, sticky='ew')

        self.lightshot2 = tkinter.Button(self.p2_act, text='Light shot', state='disable', command=lambda : self.light_shot(self.player2))
        self.lightshot2.grid(row=1, column=0, padx=25, pady=10, sticky='ew')

        self.heavyshot2 = tkinter.Button(self.p2_act, text='Heavy shot', state='disable', command=lambda : self.heavy_shot(self.player1))
        self.heavyshot2.grid(row=2, column=0, padx=25, pady=10, sticky='ew')


        self.endturn = tkinter.Button(self.window, text='End of turn', state='disable', command=lambda : self.next_turn())
        self.endturn.grid(row=3, column=1)

        # Configuration of matplotlib for integration of the display
        self.fig = Figure(edgecolor='black', facecolor='black')
        self.fi = self.fig.add_subplot(111, projection='polar', facecolor='black')

        self.axe = self.fig.get_axes()[0]
        self.axe.set_rlim(0, 200)
        self.axe.grid(color='g')
        # self.axe.set_color('green')
        self.axe.xaxis.set_ticklabels(['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$3\frac{\pi}{4}$', r'$\pi$', r'$5\frac{\pi}{4}$', r'$3\frac{\pi}{2}$', r'$7\frac{\pi}{4}$'], color = 'grey')
        self.axe.yaxis.set_ticklabels(['', '50', '', '100', '', '150', '', '200'], color = 'grey')

        self.fi.plot(np.linspace(0, 2*np.pi,100),np.ones(100),'w-', markersize=2, color='g')
        self.fi.plot(np.linspace(0, 2*np.pi,100),np.ones(100) + 199,'w-', markersize=2, color='g', linewidth=2)

        self.canva = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canva.show()
        self.canva.get_tk_widget().grid(row=1, column=1, rowspan=2, padx=5, pady=25)


    def run(self):
        """Starting the Gui"""
        self.window.mainloop()

    def spacecraft1_init(self):
        """Initialistaion of the player one's spacecraft"""

        # Verification of inputs
        tot=0
        if 1. < float(self.dist1.get()) < c.GAME_ZONE:
            tot += 1
        if 0. < float(self.vr1.get()) < 1:
            tot += 1
        if 0. < float(self.vt1.get()) < 1:
            tot += 1
        if tot == 3:
            # Setting some GUI part to disable
            self.player1 = Spacecraft(self.dist1.get(), 0, self.vr1.get(), self.vt1.get(), 'b')
            self.object.append(self.player1)
            self.player2 = Spacecraft(round(float(np.random.uniform(10, 35)), 3),\
                                 np.pi, round(float(np.random.uniform(-0.1, 0.1)), 3),\
                                 round(float(np.random.choice([-1., 1.])* np.random.normal(0.3, 0.1)), 3), 'r')
            self.object.append(self.player2)
            self.validate1.configure(state='disable')
            self.hs1.configure(text=self.player1.heavy_shot)
            self.ls1.configure(text=self.player1.light_shot)
            self.p1_dist.configure(state='disable')
            self.p1_vr1.configure(state='disable')
            self.p1_vt1.configure(state='disable')
            if self.nb_player.get() == 1:
                self.player2 = Spacecraft(round(float(np.random.uniform(10, 35)), 3),\
                                     np.pi, round(float(np.random.uniform(-0.1, 0.1)), 3),\
                                     round(float(np.random.choice([-1., 1.])* np.random.normal(0.4, 0.1)), 3), 'r')
                self.hs2.configure(text=self.player2.heavy_shot)
                self.ls2.configure(text=self.player2.light_shot)

    def spacecraft2_init(self):
        """Initialistaion of the player two's spacecraft"""

        # Verification of inputs
        tot=0
        if 1. < float(self.dist2.get()) < c.GAME_ZONE:
            tot += 1
        if 0. < float(self.vr2.get()) < 1:
            tot += 1
        if 0. < float(self.vt2.get()) < 1:
            tot += 1
        if tot == 3:
            # Setting some GUI part to disable
            self.player2 = Spacecraft(self.dist2.get(), np.pi, self.vr2.get(), self.vt2.get(), 'r')
            self.validate2.configure(state='disable')
            self.p2_dist.configure(state='disable')
            self.p2_vr2.configure(state='disable')
            self.p2_vt2.configure(state='disable')
            self.hs2.configure(text=self.player2.heavy_shot)
            self.ls2.configure(text=self.player2.light_shot)

    def one_player(self):
        """Setting the number of real players at one"""
        self.p2_dist.configure(state='disable')
        self.p2_vr2.configure(state='disable')
        self.p2_vt2.configure(state='disable')
        self.validate2.configure(state='disable')
        self.action = 1

    def two_player(self):
        """Setting the number of real players at two"""
        self.p2_dist.configure(state='normal')
        self.p2_vr2.configure(state='normal')
        self.p2_vt2.configure(state='normal')
        self.validate2.configure(state='normal')
        self.action = 0

    def next_turn(self):
        """Calculation of trajectories with a leapfrog algorithm (for leapfrog
        implementation see spacecraft and shots classes)"""
        self.fi.clear()
        self.axe = self.fig.get_axes()[0]
        self.axe.set_rlim(0, 200)
        self.axe.grid(color='g')
        # self.axe.set_color('green')
        self.axe.xaxis.set_ticklabels(['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$3\frac{\pi}{4}$', r'$\pi$', r'$5\frac{\pi}{4}$', r'$3\frac{\pi}{2}$', r'$7\frac{\pi}{4}$'], color = 'grey')
        self.axe.yaxis.set_ticklabels(['', '50', '', '100', '', '150', '', '200'], color = 'grey')

        self.fi.plot(np.linspace(0, 2*np.pi,100),np.ones(100),'w-', markersize=2, color='g')
        self.fi.plot(np.linspace(0, 2*np.pi,100),np.ones(100) + 199,'w-', markersize=2, color='g', linewidth=2)

        for j in range(200):
            for i in self.object:
                i.leapfrog(self.hole)
                if i.shooting:
                    f.collide(i, self.object[0:-2], self.hole)
                    if i == self.object[-1]:
                        f.collide(i, self.object[1:], self.hole)
                else:
                    f.collide(i, self.object, self.hole)
                if self.limit_game == "Limit condition":
                    f.zone_verification(self.object, self.hole)
                else:
                    f.zone_verification_vlib(self.object, self.hole)

        for i in self.object:
            self.fi.plot(i.theta, i.r, '*', c=i.color, markersize=5)
            self.fi.plot(i.trajplot[:,0], i.trajplot[:,1], c=i.color, linestyle = '', marker = ',')

        self.canva.show()
        if self.nb_player.get() == 2:
            self.action = 0
        else:
            self.action = 1
        self.endturn.configure(state='disable')
        self.wait1.configure(state='normal')
        self.heavyshot1.configure(state='normal')
        self.lightshot1.configure(state='normal')
        if self.nb_player.get() == 2:
            self.wait2.configure(state='normal')
            self.heavyshot2.configure(state='normal')
            self.lightshot2.configure(state='normal')

    def wait(self, spacecraft):
        """Action that doing nothing for the spacraft, just wait for a better position"""
        spacecraft.shooting = False
        if spacecraft == self.player1:
            self.lightshot1.configure(state='disable')
            self.heavyshot1.configure(state='disable')
            self.action += 1
        else:
            self.lightshot2.configure(state='disable')
            self.heavyshot2.configure(state='disable')
            self.action += 1
        if self.action == 2:
            self.endturn.configure(state='normal')

    def light_shot(self, spacecraft):
        """Action that launch a light explosive shot that destroy everything
        that collide with him."""
        if spacecraft.light_shot:
            self.angle()
            shot = Light_shot(self.angle_shot, spacecraft)
            self.angle_shot = False
            spacecraft.light_shot -= 1
            self.ls1.configure(text=spacecraft.light_shot)
            self.object.append(shot)
            spacecraft.shooting = True
        if spacecraft == self.player1:
            self.wait1.configure(state='disable')
            self.heavyshot1.configure(state='disable')
            self.action += 1
        else:
            self.wait2.configure(state='disable')
            self.heavyshot2.configure(state='disable')
            self.action += 1
        if self.action == 2:
            self.endturn.configure(state='normal')


    def heavy_shot(self, spacecraft):
        """Action that launch a heavy shot, that deviate anything that collide
        with him"""
        if spacecraft.heavy_shot:
            self.angle()
            hshot = Heavy_shot(self.angle_shot, spacecraft)
            spacecraft.heavy_shot -= 1
            self.hs1.configure(text=spacecraft.heavy_shot)
            self.object.append(hshot)
            spacecraft.shooting = True
            f.recoil(spacecraft, hshot)
        if spacecraft == self.player1:
            self.wait1.configure(state='disable')
            self.lightshot1.configure(state='disable')
            self.action += 1
        else:
            self.wait2.configure(state='disable')
            self.lightshot2.configure(state='disable')
            self.action += 1
        if self.action == 2:
            self.endturn.configure(state='normal')

    def angle(self):
        """Create a pop-up window to select the starting angle for shots, in rad."""
        popup = tkinter.Toplevel()
        popup.wm_title("Shooting angle")
        rule = tkinter.Label(popup, text='Angle have to be set between 0 and 2π')
        rule.grid(row=0, column=0, padx=25, pady=25, columnspan=2)
        labelBonus = tkinter.Label(popup, text="Angle : ")
        labelBonus.grid(row=1, column=0, padx=10, pady=10)
        ang = tkinter.DoubleVar()
        ang.set(-1.)
        ang_value = tkinter.Entry(popup, textvariable=ang, width=10)
        ang_value.grid(row=1, column=1, padx=10, pady=10)
        def is_valid(popup, ang):
            if 0<=ang.get()<2*np.pi:
                popup.destroy()
        B1 = tkinter.Button(popup, text="Validate", command=lambda : is_valid(popup, ang))
        B1.grid(row=2, column=0, columnspan=2)
        self.angle_shot = ang.get()


if __name__ == '__main__':
    game = App()
    game.run()
