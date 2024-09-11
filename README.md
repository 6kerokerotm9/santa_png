# santa_png
Just a quick rundown on how the bot works:

Since this is hosted locally, I will have to run it from my machine
- from there it connects to discord and contiunes to stay connected, listening for events

Commands
- !uses: lists out the commands
- !umu: literally prints out umu
- !people: writes out a list of people in the channel (which I assume are the people participating)
- !me: bot will resend you your recepient 
- !roll: rolls the names and will not override the old list if used more than once in a server
- !juju: the name of that guy who keeps almost breaking the bot every year

About names picked
- so when roll is used the bot writes a name pairs to a json file in the same directory:
  ![image](https://user-images.githubusercontent.com/10038262/188301470-a6c51e28-1684-4d6a-8784-92c80f52a835.png)
- the bot host will not see the name pairs unless they specifically open the json file
