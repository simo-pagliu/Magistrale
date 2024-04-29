import random
import numpy as np

#In elastic scattering, the neutron is scattered by the nucleus without any loss of kinetic energy.
#therefore the velocity are the same before and after the collision in the center of mass frame of reference
#also, the scattering cross section is isotropic in the center of mass frame, therefore the scattering sigma_scattering(theta)=sigma_scattering / (4*pi)

A_target = 235 #atomic mass number of U235

avg_scattering_angle_CM = 2/(3*A_target) #average scattering angle in the center of mass frame

#the actual scatterin angle is random, given by an uniform distribution between 0 and 2*pi
#give me a random number between 0 and 2*pi
scattering_angle_CM = random.uniform(0, 2*np.pi) 
print(f"The scattering angle in the center of mass frame is {scattering_angle_CM} rad")

#the scattering angle in the lab frame is given by a simple formula that comes from the cosine theorem
scattering_angle_L = np.arctan(np.sin(scattering_angle_CM)/(np.cos(scattering_angle_CM)+1/A_target)) #scattering angle in the lab frame
print(f"The scattering angle in the lab frame is {scattering_angle_L} rad")
#velocity of the neutron before the collision
v_initial = 1e3 #m/s

#velocity of the neutron after the collision in the LAB frame
v_final_L = np.sqrt(v_initial**2 * (1+2*A_target*np.cos(scattering_angle_CM)+A_target**2)/(A_target+1)**2 ) #velocity after the collision

#final velocity of the target atom, in the lab frame, at rest before the impact
v_final_target_L = np.sqrt((v_initial**2 - v_final_L**2)/A_target) #velocity of the target atom in the lab frame

#angle of the target atom in the lab frame
## I DON'T KNOW HOW TO COMPUTE THIS
theta_final_target_L = -(-v_initial + v_final_L * np.cos(scattering_angle_L))/v_final_target_L

coeff_run_time = 1. #run time coeff for the neutron at the start
path_n = 2
path_trg = 0.5
run_time_neutron_post = coeff_run_time / (v_final_L/v_initial) #run time of the neutron post collision
run_time_target_post = (path_trg/path_n) * coeff_run_time / (v_final_target_L/v_initial) #run time of the target post collision

## ANIMATION
from manim import *

class NeutronToTarget(Scene):
    def construct(self):
        neutron = Circle(0.1)  # create a circle
        neutron.set_stroke(0)  # remove the border
        neutron.set_fill(WHITE, opacity=0.5)  # set the color and transparency
        
        target = Circle(0.5)  # create a bigger circle for the target nucleus
        target.set_stroke(0) # remove the border
        target.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        target.next_to(neutron, RIGHT, buff=2)  # set the position
        self.play(Create(neutron), Create(target))  # show the shapes on screen

        self.play(
            neutron.animate.shift(RIGHT * 2),
            run_time = coeff_run_time,
            ),
        Wait(0),
        self.play(
            target.animate(run_time=run_time_target_post).shift(path_n*np.cos(theta_final_target_L)*RIGHT + path_n*np.sin(theta_final_target_L)*UP),
            neutron.animate(run_time=run_time_neutron_post).shift(path_trg*np.cos(scattering_angle_L)*RIGHT + path_trg*np.sin(scattering_angle_L)*UP),
            )

scene = NeutronToTarget()
scene.render(QUALITIES['medium_quality'])
#Open file
from manim.utils.file_ops import open_file as open_media_file 
open_media_file(scene.renderer.file_writer.movie_file_path)