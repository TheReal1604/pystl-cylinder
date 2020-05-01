# pystl-cylinder
A python3 program which produces a cylinder in stl ASCII format at a given quality setting.

Parameters:
```
-r RADIUS (--radius) 
-he HEIGHT (--height)
-q <quality>
-aq (--all-qualities)
-h HELP (--help)
```

Quality settings:
``` 
ultrahigh
high
mid
low
cube
```

The program outputs a file called `demo.stl` at the same location the script was executed.

If the program is called with `-aq` or `--all-qualities` it outputs an stl file of EACH quality setting
at the location the script was executed.

### Example
`python3 main.py -r 3 -he 5 -q high` 
- outputs a `demo.stl` in quality setting "high" of a cylinder with a radius of 3
and a height of 5

`python3 main.py -r 5 -he 10 --all-qualities `
- outputs `cube.stl, low.stl, mid.stl, high.stl, ultrahigh.stl` of a cylinder with a radius of 5 and a height of 10
