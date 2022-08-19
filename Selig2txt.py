import re
import argparse


parser = argparse.ArgumentParser(
    description="Convert a Selig or xfoil airfoil file to .txt to be used in Solidworks"
)
parser.add_argument(
    "inputfile",
    help="Path to file to be used as input. If it is in the same directory, just the filename.",  # noqa: E501
)
parser.add_argument(
    "--split",
    help="Split the airfoil into two curves. Two output files are created",
    action="store_true",
)
args = parser.parse_args()


class airfoil_coord:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = 0.0  # just default this one to 0.0 to make life easier later


if __name__ == "__main__":
    try:
        print(args.inputfile)
        inputname = args.inputfile
        if "." in args.inputfile:
            inputname = args.inputfile[: args.inputfile.find(".")]
        print(inputname)
        contents = ""
        with open(args.inputfile, "r") as f:
            contents = f.readlines()
        while not contents[0].strip().startswith("1.000"):
            # something not the correct point is on the first line. get rid of it.
            contents.pop(0)
        contents = "".join(contents)
        contents = contents + "\n"  # add a blank line at the end
        match1 = re.compile(r"^ +", re.MULTILINE)  # leading whitespace
        match2 = re.compile(r"( +)")
        match4 = re.compile(r"(^\d\..+)(\n)", re.MULTILINE)
        contents = re.sub(
            match1, "", contents
        )  # remove leading whitespace on all the lines
        contents = re.sub(match2, ",", contents)  # put a comma between the numbers
        splitcontents = contents.split("\n")
        coords = []
        for line in splitcontents:
            if len(line) < 1:
                continue
            x, y = line.split(",")
            coords.append(airfoil_coord(x, y))

        contents = re.sub(
            match4, lambda match: f"{match.group(1)},0.000000\n", contents
        )

        # split the airfoil in to top and bottom
        if args.split:
            print("splitting {}".format(inputname))
            # split the file at the 0,0 point and make top and bottom output files
            # find the minimum of the x coord since not all files have a 0.00000
            min_x_index = 0
            for i in range(len(coords)):
                if coords[i].x < coords[min_x_index].x:
                    min_x_index = i

            top = coords[:min_x_index]
            bottom = coords[min_x_index:]
            zero_coord = airfoil_coord(0, 0)

            if top[-1].x != float(0) or top[-1].y != float(0) or top[-1].z != float(0):
                # add on a zero_coord if it is missing
                top = top + [zero_coord]

            if (
                bottom[0].x != float(0)
                or bottom[0].y != float(0)
                or bottom[0].z != float(0)
            ):
                # put a zero at the beginning if it is missing
                bottom = [zero_coord] + bottom

            with open(inputname + "TOP.txt", "w") as outputTOP:
                for coord in top:
                    outputTOP.write(
                        "{:.6f},{:.6f},{:.6f}\n".format(coord.x, coord.y, coord.z)
                    )
            with open(inputname + "BOT.txt", "w") as outputBOT:
                for coord in bottom:
                    outputBOT.write(
                        "{:.6f},{:.6f},{:.6f}\n".format(coord.x, coord.y, coord.z)
                    )
        else:
            with open("output.txt", "w") as output:
                for coord in coords:
                    output.write(
                        "{:.6f},{:.6f},{:.6f}\n".format(coord.x, coord.y, coord.z)
                    )
        # sys.exit()
    # except IndexError:
    #     print('Please drag and drop the Selig .dat file')
    finally:
        input("Press ENTER to continue...")
