# ScamBgone
An IOS message anti-scam filter for SMS/MMS
vibe coding my way to understanding and getting rid of these damn scam texts.

**Using this as my public "to-do" list and vision board**
**Feel free to add suggestions, any idea is welcome because I don't know what I'm doing!

Iphone sends metadata to the app, including sender number, message type (sms, mms) and country codes.
Iphone will err on the side of "ALLOW" if the program takes longer than a few miliseconds.
IPhone user must opt in by Settings → Messages → Unknown & Spam → SMS Filtering → Your App. Hopefully I can automate this for users.
I want "per-user" events to be tracked and algorythmicly processed by ML to tailor anti-scam metrics to a user device. **Research this
I want a local ML algo to determine numeric float values for each "bad" word based on web-scraped data or other Publicly Available Information (PAI) This data will be packaged and sent to users. 


Reiterate:*
I want A webscrapper to pull the most common and well known scam messages to train my models on. Additionally, this data will be put into the lightweight json file that will be installed on users phones.
*

I'm not sure what the weights should be yet, I will need to think about my options more.


Mental Outline:

Let's reframe the vision, we've made good progress, but now it's time to consider my options.

he vision is as follows:

User installs app. Swift logic processes packaged datasets that contain bad words and their corresponding weights. These are prepackaged values that have been algorithmically determined to be examples of  bad messages.

The app will take sms/mms data and pass it through swift for logic testing, this will determine the messages value of:

JUNK
UNSURE
ALLOW

These return values will determine if the message is sent to the users inbox (allow) or send to the cloud and shown to users for data collection to refine the apps pool of weights (This means asking the user if the message should be marked spam). (UNSURE) and finally (JUNKED) for anything that doesn't meet the same standards.


the program sends a request to my cloud server periodically to check and see if there are updated keyword, value pairs on the home server, the logic flows as follows: 
if update exists or (yes), download updates to user app, if no, the apps periodic timer resets.
a
I want more development tools.

I need a tool, possibly ML, that can sort through web scraped tables of "scam mail" and determine which words should be classified as "likely scam" word sequences. Additionally,  I need it take the sorted data and assign it a float value based on the "bad" words severity

I've learned that statiscal learning is one of the ways I can keep make my app "light-weight" enough to interface with IOS.
