# tosted
Win toast notification package for python.
Build your own toast starting from a readable human xml class natively implemented.

## Installation

```bash
pip install toasted
```

## Usage

### Fast toast
Send default notification rapidly to screen.

```python
import toasted as ts

reminder_toast = ts.Reminder("Hi. Please call me")
reminder_toast.send()

```

![image](https://github.com/MekJohn/toasted/blob/main/test/Incoming_call.png)


### Builder mode
Build your own xml tree document, self-checked structure, as you want.

```python
import toasted as ts

# create main nodes
toast = Element("toast")
visual = ts.Visual()
binding = ts.Binding()
actions = ts.Actions()
audio = ts.Audio("alarm3")

# generate 'visual' sub nodes
text1 = ts.Text("Conf Room 2001 / Building 135")
text2 = ts.Text("10:00 AM - 10:30 AM")
image = ts.Image(r"myfolder\img.png", position="logo", rounded=True)

# generate 'actions' sub nodes
## input type
sel = ts.SelectionBox("John", "Frank", "Robert", label="Send Invitation")
inp = ts.InputBox("textBox", placeholder="Choose one option")
## button type
butt = ts.Button("Ok", tip="clicca", inputbox="ins2")
butt2 = ts.Button("Send", tip="send", color="g")
butt3 = ts.Button("Cancel", tip="clicca", color="r")
# context type
menu = ts.Context("Premi per uscire")

# adding sub nodes to main tree node
binding.extend([text1, text2, image])
visual.append(binding)
toast.append(audio)
toast.append(visual)

# compose the tree
actions.append(sel)
actions.append(inp)
actions.append(menu)
actions.append(butt)
actions.append(butt2)
actions.append(butt3)
toast.append(actions)
xml = Tree(toast)

# get the Toast object and send notification to screen
t = Toast(xml)
t.send()
```

![image](https://github.com/MekJohn/toasted/blob/main/test/meeting.png)

```python
print(t)

# OUTPUT
<toast launch="http:" activationType="protocol" displayTimestamp="2024-05-06T22:52:58+00:00" useButtonStyle="true">
  <audio src="ms-winsoundevent:Notification.Looping.Alarm3" />
  <visual>
    <binding template="ToastGeneric">
      <text hint-align="default" hint-style="default" hint-minLines="1">Conf Room 2001 / Building 135</text>
      <text hint-align="default" hint-style="default" hint-minLines="1">10:00 AM - 10:30 AM</text>
      <image src="C:\Users\gaudi\Desktop\projects\tosted\img.png" placement="appLogoOverride" hint-crop="circle" />
    </binding>
  </visual>
  <actions>
    <input type="selection" id="SelectionBox" activationType="protocol" arguments="http:SelectionBox" title="Send Invitation" defaultInput="0">
      <selection id="0" content="John" />
      <selection id="1" content="Frank" />
      <selection id="2" content="Robert" />
    </input>
    <input type="text" id="textBox" activationType="protocol" arguments="http:textBox" placeHolderContent="Choose one option" />
    <action activationType="protocol" arguments="http:Premi per uscire" placement="contextMenu" content="Premi per uscire" />
    <action activationType="protocol" content="Ok" arguments="http:Ok" hint-toolTip="clicca" hint-inputId="ins2" />
    <action activationType="protocol" content="Send" arguments="http:Send" hint-toolTip="send" hint-buttonStyle="Success" />
    <action activationType="protocol" content="Cancel" arguments="http:Cancel" hint-toolTip="clicca" hint-buttonStyle="Critical" />
  </actions>
</toast>
```


