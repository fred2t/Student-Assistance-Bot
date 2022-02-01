import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip, concatenate_videoclips

from typing import *

Node = TypeVar('Node')
PointX = Union[int, float]
PointY = Union[int, float]
Coordinate = Tuple[PointX, PointY]

NodeStorage = Dict[Node, Coordinate]

MapImage = str

"""
DESIGN ---------------

Take in list of nodes

split each node into intervals
add each one into a tuple of lists
loop through them, when the list(node) finishes, and direction needs to be changed

we draw thatfinished node, and start a new interval to draw the new arrows in the other direction 

"""




class MapAnimate:
    def __init__(self, nodes: NodeStorage, other_floor: Optional[NodeStorage] = None) -> None:
        self.fig, self.ax = plt.subplots()
        self.grid_scale = ((0, 104), (0,68))
        # self.grid_scale = ((0, 2000), (0,1200))
        self.animation_iter = 10

        # all of these and similar with look like: 
        """[((x1, y1), (x2, y2)), ((x1, y1), (x2, y2)), ...]"""
        self.nodes: NodeStorage = nodes
        self.other_floor = other_floor

        self.lineOsO: List[Tuple[Coordinate, Coordinate]] = []

        self.background_image: MapImage = 'unnamed.jpg'

        
        
        
    def set_map_size(self) -> None:
        return self.ax.set(xlim=self.grid_scale[0], ylim=self.grid_scale[1])
    
    def needed_frames(self) -> int:
        return (len(self.nodes) - 1) * self.animation_iter

    
    def setup_screen(self) -> None:
        """prepare all visuals for the graph"""
        
        # clear the screen from the last position
        self.ax.cla()
        # reset map to a constant size to avoid graph vibrations
        self.set_map_size()

        # image
        img = mpimg.imread(self.background_image)
        plt.imshow(img)


    def animate(self, i) -> None:
        print(i)
        
        # create the arrow connecting each node: take the coordinates of the first and second
        # node in the list and create steps to animate that
        if self.nodes:
            x_start, y_start = self.nodes[list(self.nodes)[0]]
            x_end, y_end = self.nodes[list(self.nodes)[1]]

            # each arrow will be completed by a set amount of animation steps
            x_steps = np.linspace(x_start, x_end, self.animation_iter)
            y_steps = np.linspace(y_start, y_end, self.animation_iter)
            # print((x_start, x_end))
            # print((x_start, y_end))

            # check if we've finished an entire connection, if so, add the pair of nodes to a storage
            # for completed connections to be redrawn as lines later
            if (i + 1) % self.animation_iter == 0:
                self.lineOsO.append(((x_start, x_end), (y_start, y_end)))

        self.setup_screen()
        
        # if if we're at an iteration above a single coordinate connection completetion, we have past lines
        # that have been completed, and we need to redraw them all
        if i > self.animation_iter - 1:
            for line in self.lineOsO:
                plt.plot(line[0], line[1], 'r-')


        index_subtractor = (i // self.animation_iter) * self.animation_iter
        # we restart drawing a new arrow that changes direction starting from the end of the last point
        # recorded, aka, the end of the head of the last completed arrow location
        self.ax.arrow(x_start, y_start,
            x_steps[i - index_subtractor] - x_start, y_steps[i - index_subtractor] - y_start,

            head_width = 2, head_length = 2, fc = 'blue', ec = 'blue')
        
        # if we have reached an end of a node-pair connection process, we delete that first node, cause
        # we have finished using it's coordinates to create the line connection
        if (i + 1) % self.animation_iter == 0:
            self.nodes.pop(list(self.nodes)[0])

        # print(i)
        # print(x.points2map)
        # print(x.lineOsO)


    def make_single_gif(self, save_name):
        frames_needed = self.needed_frames()
        anim = animation.FuncAnimation(self.fig, self.animate, interval=10, frames=frames_needed, repeat=False)


        # create the animation in gif format
        writergif = animation.PillowWriter(fps=30)
        anim.save(save_name, writer=writergif)

    
    def create_gif(self) -> None:
        # if statement if there's an other floor, if there is, we do stuff on first floor,
        # and at the end, nodes = other floor
        # that way the process is redone later
        # if it doesn't exist, it'd do the same process anyways

        if self.other_floor:
            self.make_single_gif(r"route1.gif")
            self.nodes = self.other_floor
            self.background_image = 'unnamed.jpg'

        self.make_single_gif(r"route2.gif")

        # if two floors exist, we need to combine the gif that show the different floors
        if self.other_floor:
            self.combine_floor_gifs()

            import os
            # cannot remove route2 gif as well (actually got not clue why: 
            # PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: 'route2.gif)
            os.remove('route1.gif')

        

        



    def combine_floor_gifs(self):
        """take the gif videos of two different floors and combine them into one gif"""

        # use VideoFileClip() class create two video object, then we merge them
        gif_1 = VideoFileClip("route1.gif")
        gif_2 = VideoFileClip("route2.gif")

        # Merge videos with concatenate_videoclips()
        the_gif = concatenate_videoclips([gif_1, gif_2])
        the_gif.write_gif("xdhmmname.gif")
         

x = MapAnimate({
    'n1': (50, 35),
    'n2': (90, 45),
    'n3': (100, 60),
    'n4': (1, 1),
    'n5': (50, 50),
    'n6': (90, 10)
},
{
    'n7': (90, 10),
    'n8': (1, 1)
})



if __name__ == "__main__":
    x.create_gif()