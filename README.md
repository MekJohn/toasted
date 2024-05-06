# tosted
Win toast notification package for python.
Build your own toast starting from a readable human xml class natively implemented.

## Installation

```bash
pip install toasted
```

## Usage

### Fast toast

```python
import toasted as ts

reminder_toast = ts.Reminder("Hi. Please call me")
reminder_toast.send()

```

![image](https://github.com/MekJohn/toasted/blob/main/test/Incoming_call.png)


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


