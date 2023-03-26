# LIRPy

Largest Interior Rectangle for Python

This was originally made for a stupid Minecraft project for the purpose of making as few Baritone selections as possible when designating a cylinder, but it should work in any other context as well.

I also hate numpy with a passion for mysterious reasons I can't even explain to myself.  Therefore, this project doesn't use it.

## Background

When I'm not breaking games for work, I tend to play engineering games, and one of the first such games I got into was Minecraft.  I play it off and on, and I tend to get into mega-projects, which often end up with me getting bored and having a bot called Baritone do most of the work. 

I needed a tool to generate Baritone selection AABBs (which are defined by opposing corner coordinates) for cylinders of arbitrary radius and depth. The easiest possible way would be to generate selections for every single voxel column.  This would not be practical due to the sheer number of selections needing to be made.

So, after doing some research, I determined what I needed was an axis-aligned largest interior rectangle library.

## Other Options

Other solutions I've looked at:

* [largestinteriorrectangle](https://github.com/lukasalexanderweber/lir) uses numba, which is so outdated it won't compile with LLVM 14.  It's also unfortunately spammed all over stackoverflow, which makes it harder to find background information.
* https://www.evryway.com/largest-interior/ - Never worked properly for me.
* https://pypi.org/project/maxrect/ - GIS-specific, so it requires weird inputs and works on polygons rather than grids. Their GitHub is also missing.
* Various things in other languages, like C, MATLAB, and C# - no

So I made my own system, with blackjack and classy sex workers.

## Caveats

I am no mathematician, so this is nowhere within ten light-years of optimized, and there are probably a dozen papers dense with calculus describing new and exciting ways of doing that. I didn't take calculus in uni.

This works well enough for my purposes, but **PRs with improvements are absolutely welcome.**

## Installation

Requires Python >= 3.10

`pip install lirpy`

## Development

Requires Python >= 3.10 *and* `poetry`

## Example:
```shell
$ python -m lirpy -472 58 570 -r 7 -d 1 --dump-steps
```
```
Center: -472 58 570
Radius: 7
Depth: 0
Along axis: -Y
Step 0:
       █       
    ███████    
   █████████   
  ███████████  
 █████████████ 
 █████████████ 
 █████████████ 
███████████████
 █████████████ 
 █████████████ 
 █████████████ 
  ███████████  
   █████████   
    ███████    
       █       
Step 1:
       █       
    ███████    
               
  █         █  
 ██         ██ 
 ██         ██ 
 ██         ██ 
███         ███
 ██         ██ 
 ██         ██ 
 ██         ██ 
  █         █  
               
    ███████    
       █       
Step 2:
       █       
    ███████    
               
  █         █  
            ██ 
            ██ 
            ██ 
█           ███
            ██ 
            ██ 
            ██ 
  █         █  
               
    ███████    
       █       
Step 3:
       █       
    ███████    
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
    ███████    
       █       
Step 4:
       █       
               
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
    ███████    
       █       
Step 5:
       █       
               
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 6:
               
               
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 7:
               
               
               
            █  
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 8:
               
               
               
               
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 9:
               
               
               
               
               
               
               
              █
               
               
               
  █         █  
               
               
       █       
Step 10:
               
               
               
               
               
               
               
               
               
               
               
  █         █  
               
               
       █       
Step 11:
               
               
               
               
               
               
               
               
               
               
               
            █  
               
               
       █       
Step 12:
               
               
               
               
               
               
               
               
               
               
               
               
               
               
       █       
Step 13:
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
#sel clear
#sel 1 -462 58 579
#sel 2 -454 58 589
#sel 1 -464 58 581
#sel 2 -463 58 587
#sel 1 -453 58 581
#sel 2 -452 58 587
#sel 1 -461 58 578
#sel 2 -455 58 578
#sel 1 -461 58 590
#sel 2 -455 58 590
#sel 1 -458 58 577
#sel 2 -458 58 577
#sel 1 -463 58 580
#sel 2 -463 58 580
#sel 1 -453 58 580
#sel 2 -453 58 580
#sel 1 -465 58 584
#sel 2 -465 58 584
#sel 1 -451 58 584
#sel 2 -451 58 584
#sel 1 -463 58 588
#sel 2 -463 58 588
#sel 1 -453 58 588
#sel 2 -453 58 588
#sel 1 -458 58 591
#sel 2 -458 58 591
```