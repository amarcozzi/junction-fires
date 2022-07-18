import json
import numpy as np
from string import Template
from skimage import draw

params = {
    "fuel_model": "bfm",
    "theta": 35,
    "line_length": 10,
    "dxdy": 1.,
    "dz": 1.,
    "nxny": 120.,
    "nz": 40.,
    "wind_speed": 2.7,
}


def main() -> None:
    # Select appropriate fuel model template file
    if params["fuel_model"] == "bfm":
        template_filename = "templates/input_junction_fire_bfm.fds"
    elif params["fuel-model"] == "bfm":
        template_filename = "templates/input_junction_fire_pfm.fds"
    else:
        print("Must have bfm or pfm for fuel model")
        return

    # Compute the ignition line locations
    params["ignition_lines"] = get_ignition_lines(params["theta"], params["line_length"])

    # Load the fuel model template file
    with open(template_filename) as fin:
        template_file = fin.read()
    template = Template(template_file)

    # Write parameters to new fds input file
    with open("test_fds_input.fds", "w") as fout:
        fout_string = template.substitute(params)
        fout.write(fout_string)

def get_ignition_lines(theta_deg: float, l_meters: int) -> list[str]:
    """Finds locations of ignition lines based on theta and the grid parameters, and writes ignition lines to a list of strings.

    NOTE: Grid cell 0, 0 corresponds to origin (0 meters, 0 meters)

    Args:
        theta_deg (float): angle of the ignition lines from the x-axis (in degrees)
        l_meters (float): length of the ignition line from the origin (in meters)

    Returns:
        list[str]: _description_
    """
    # TODO: Convert l from distance from origin in meters to distance from origin in pixels
    l_pixels = l_meters

    # Find the r,c coordinates of the top ignition line
    theta_rads = np.deg2rad(theta_deg)
    r1_pixels = l_pixels * np.sin(theta_rads)
    c1_pixels = l_pixels * np.cos(theta_rads)

    # TODO: Figure out what to do about rounding
    r1_pixels = int(r1_pixels)
    c1_pixels = int(c1_pixels)

    # Generate grid coordinates for the line from the origin to the vector defined by l and theta
    rr, cc_top = draw.line(0, 0, r1_pixels, c1_pixels)
    cc_bottom = [-c for c in cc_top]

    # Write the ignition line coordinates
    top_ignition_lines = []
    bot_ignition_lines = []
    for i in range(len(rr)):
        r_coord = rr[i]
        c_top_coord = cc_top[i]
        c_bot_coord = cc_bottom[i]

        print()
        
        # TODO: Convert the grid coordinate to world coordinates
        # &INIT PART_ID='blade of grass', XB=0.,100.,-50.,50.,0.00,0.21, N_PARTICLES_PER_CELL=1, CELL_CENTERED=T, MASS_PER_VOLUME=1.33, DRY=T /


    print()

    


if __name__ == "__main__":
    main()