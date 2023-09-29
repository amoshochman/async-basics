# constant-living-notice

Performs some "heavy computation" while printing that is still alive, each 5 second
Instructions: run python main.py

Takeaways:
- While this could be "approximately" achieved with multiprocessing, there is no guaranty that the printing will be
called on time, due to the GIL.