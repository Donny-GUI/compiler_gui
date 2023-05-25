from dataclasses import dataclass
import os


@dataclass(slots=True)
class Asset:
    homedir = os.path.join(os.getcwd(), "images")
    animated_logo = os.path.join(homedir, "spinpy.gif")
    spinner25 = os.path.join(homedir, "spinpy25.gif")
    spinner75 = os.path.join(homedir, "spinpy75.gif")
    spinpy50 = os.path.join(homedir, "spinpy50.gif")
    spinpy20 = os.path.join(homedir, "spinpy20.gif")
    compspin = os.path.join(homedir, "spincomp.gif")