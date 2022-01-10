Sav Programming Challenge ReadMe

How To Run the Script

The first thing to mention is that to be able to run the script, you must have Python installed on your system. Once
you have confirmed its installation, you can download the zip file and extract the files using your favorite unzipping
program. Once this is done there are two ways that you can choose to run the script. The first is to open the project in
a Python IDE of your choice and set the configuration to the main.py script. From there, you can easily run the program
by hitting the run button. If you don't have any Python IDEs installed, you can go to the Command Prompt on Windows, or
the Apple/Linux equivalent, and cd to where the files were extracted, specifically the SavAPIProject folder. From here
all you need to type is "python main.py" and hit enter, starting the program.

Design Choices

While not required, I did want to talk about some specific design choices I made in my three methods to reduce CPU time.
The first method, generateTimeList, is simply used to replicate the sorted Time List that the problem describes. The
second method, convertListtoDict, converts the given List and makes it into a multilayered Dict with a Dict holding the
hour and minute values and a List holding the second values due to the need to get a count of the second instances
later. I chose to do this because Dicts are more time efficient than Lists and the time taken to convert the List into a
Dict would be worth it considering the amount of times I would need to access the Times later. In the third method,
sendCalls, I knew from the beginning that it would need a pseudo-continually running while loop, but that sort of
implementation is very costly. So I therefore decided to have the program sleep until it hit certain thresholds. For
example, say the current time was 10:00:00 and the next time in the list is 11:18:27, I would have the method recognize
that the next time isn't until hour 11, and therefore have the program sleep until 11:00:00. This was similarly done
for both minutes and seconds, reducing the CPU usage of the method.



