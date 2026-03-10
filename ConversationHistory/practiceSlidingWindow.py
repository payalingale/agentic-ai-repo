class SlidingWindow():
  def __init__(self,window_size=10):
    self.messages = []
    self.window_size = window_size
  def add_messages(self,role,content):
    self.messages.append({
      'role':role,
      'content':content
    })
    if(len(self.messages) > self.window_size):
      self.messages = self.messages[-self.window_size:]

  def history(self):
    return self.messages



window = SlidingWindow(window_size=2)
window.add_messages('user','Hello m name is payal')
window.add_messages('assistant','I stay in abudhabi')
window.add_messages('user','I like to build agents')
window.add_messages('user','i am 7 months pregnant')

print(f'')
