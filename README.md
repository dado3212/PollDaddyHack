# PollDaddy Hack

This is pretty easy to use.  Just download the Python script, and customize the variables for what form/answer/number of votes.  

It needs Python 2.7.6.
Also be sure to do pip2.7 install requests

### Disclaimer
This script will **not** work on polls that do not allow multiple votes from one person.  The useragents and proxy settings will help try and mask your mass voting, but they will not get you around IP blocks.  If someone wants to give a shot at forking this and adding that functionality, I will be happy to merge it in.

### Example
You want to rig this poll: https://polldaddy.com/poll/9206448/ for the answer "It's a great way to keep kids in line during a crazy time of year.", and you want to vote 1000 times.  The poll_id comes from the url: <code>https://polldaddy.com/poll/<b>9206448</b>/</code>.  The answer_id comes from the looking at the source code for the associated checkbox: <code>\<input type="radio" name="PDI_answer" id="PDI_answer41930288" value="**41930288**"></code>.


Thus, you would want the variables to be set to:
```
poll_id = 9206448
answer_id = 41930288
number_of_votes = 1000
```
