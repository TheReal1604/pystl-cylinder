# pystl-cylinder
A python3 program which produces a cylinder in stl ASCII format at a given quality setting.

Parameters:
```
-rl LOWERRADIUS (--lower-radius)
-ru UPPERRADIUS (--upper-radius) 
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
`python3 main.py -rl 3 -ru 3 -he 5 -q high` 
- outputs a `demo.stl` in quality setting "high" of a cylinder with a radius of 3
and a height of 5

`python3 main.py -rl 5 -ru 3 -he 10 `
- outputs `cube.stl, low.stl, mid.stl, high.stl, ultrahigh.stl` of a cylinder with a lower radius of 5, upper radius of 3 
and a height of 10
