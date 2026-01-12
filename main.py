from multiprocessing import Process, Array, current_process, Value, Semaphore
import sys
from pathlib import Path


def paint_pixel(color, black1, black2, cr, cg, cb):
    with open(color, "a") as f:
        f.write(f"{cr} {cg} {cb}\n")
    
    with open (black1, "a") as f:
        f.write("0 0 0\n")
    
    with open (black2, "a") as f:
        f.write("0 0 0\n")


def all_black(f1,f2,f3):
    with open(f1, "a") as f:
        f.write("0 0 0\n")
    
    with open (f2, "a") as f:
        f.write("0 0 0\n")
    
    with open (f3, "a") as f:
        f.write("0 0 0\n")





class sorter (Process):

    def __init__(self, file, shared_red, shared_green, shared_blue, semaphore):
        super().__init__() 

        self._file = file
        self._shared_red = shared_red  
        self._shared_green = shared_green  
        self._shared_blue = shared_blue  
        self._semaphore = semaphore
        self._intro = ""
        self._red = 0
        self._green = 0
        self._blue = 0
        self._filered = ""
        self._filegreen = ""
        self._fileblue = ""

    def create_files(self):

        if self._red > self._green and self._red > self._blue:
            paint_pixel(self._filered, self._filegreen, self._fileblue, self._red, self._green, self._blue)

        elif self._green > self._red and self._green > self._blue:
            paint_pixel(self._filegreen, self._filered, self._fileblue, self._red, self._green, self._blue)

        elif self._blue > self._red and self._blue > self._green:
            paint_pixel(self._fileblue, self._filegreen, self._filered, self._red, self._green, self._blue)

        elif self._red == self._green and self._green == self._blue:
            all_black(self._filered, self._filegreen, self._fileblue)

    def run (self):
        with self._semaphore:
            is_intro = True
            num_count = 0
            number = ""
            
            
                
            with open(self._file, "r") as f:
                while c:= f.read(1):
                    if is_intro:
                        if c not in " \n\t\r":
                            number += c
                            
                            if num_count == 4:
                                is_intro = False
                                num_count = 0

                                fired = str(self._file)[0: len(str(self._file))-4] + "_red"
                                figreen = str(self._file)[0: len(str(self._file))-4] + "_green"
                                fiblue = str(self._file)[0: len(str(self._file))-4] + "_blue"

                                self._filered = Path(fired + ".ppm")
                                self._filegreen = Path(figreen + ".ppm")
                                self._fileblue = Path(fiblue + ".ppm")

                                with open (self._filered, "w") as fd:
                                    fd.write(self._intro)
        
                                with open (self._filegreen, "w") as fd:
                                    fd.write(self._intro)
        
                                with open (self._fileblue, "w") as fd:
                                    fd.write(self._intro)
                        else:
                            num_count += 1
                            self._intro += number
                            self._intro += c
                            number = ""

                            
                
                    else :
                        if c not in " \n\t\r":
                            number +=c
                            
                            
                        else:
                            if num_count == 0:
                                self._red = int(number)
                                self._shared_red.value += 1
                            elif num_count == 1:
                                self._green = int(number)
                                self._shared_green.value += 1
                            elif num_count == 2:
                                self._blue = int(number)
                                self._shared_blue.value += 1


                                self.create_files()
                                    
                                self._red = 0
                                self._blue = 0
                                self._green = 0
                                num_count = -1
                            num_count += 1
                            number = ""
                        
                                    





if __name__=="__main__":
    if len(sys.argv) < 2:
        print(f"Error: usage: python {sys.argv[0]} <directory with files>")
        exit(1)

    semaphore = Semaphore(4)

    shared_red = Value("i", 0)
    shared_green = Value("i", 0)
    shared_blue = Value("i", 0)

    dir = Path(sys.argv[1])

    files = []
    
    if dir.is_dir():
        for i in dir.iterdir():
            if i.is_file():
                files.append(i)
            else:
                print("Error: content: This program works using files. Please upload a directory whose content is .ppm files.")
                exit(1)
    else:
        print("Error: content: This program uses a directory with .ppm files. Please upload a directory.")
        exit(1)
    
    processes = []
    
    for f in files:
        processes.append(sorter(f, shared_red, shared_green, shared_blue, semaphore))
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    