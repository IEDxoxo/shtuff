try:
  import sys
  import fade,time,requests,aiohttp,asyncio,json,socket,ssl,msmcauth,threading,socks
  from datetime import datetime
  from discord_webhook import DiscordEmbed, DiscordWebhook
except ImportError:
  from os import system
  print(f"New update detected! Downloading modules...")
  system("pip install fade")
  system("pip install aiohttp")
  system("pip install ssl")
  system("pip install msmcauth")
  system("pip install discord_webhook")
  system("pip install pysocks")
fo = open("config.json") # creating the object to be read
data = json.load(fo) # reading and loading the data
fo.close() # to prevent memory leak

rose = fade.greenblue("""
    _,--._.-,
   /\_r-,\_ )
.-.) _;='_/ (.;
 \ \\'     \/S )   
  L.'-. _.'|-'
 <_`-'\\'_.'/
   `'-._( \\
    ___   \\\,      ___
    \ .'-. \\\   .-'_. /
     '._' '.\\\/.-'_.'
        '--``\('--'
              \\\\
              `\\\,
                \|""")
print(rose) # for cuteness <3
proxies = []
up = False
def getproxy(): # Structure for detection of proxies
    try:
        po = open("proxies.txt")
        pr = po.read().splitlines()
        for item in pr:
            proxies.append(item)
        up = True
    except:
        up = False
class utility():
  def __init__(self, target, offset, snipertype):
    self.target = target
    self.delay = offset
    self.snipetype = snipertype
    self.headers = {'Accept': "application/json", "Content-Type": "application/json", "Authorization": ""}
    self.snipesession = None
    self.droptime = None
    self.times = []
  def webhooktimes(self, times):
    newstr = "```\n"
    link = "https://discordapp.com/api/webhooks/1011445175526113450/TiODeUFCeVzjQMHbrAmuL4YJaVswZ_b2OnV9tv7VxpVzT6P4L4sE_U-KdYoJj-yoRul7"
    for recvtime in times:
        newstr += recvtime + "\n"
    newstr += '```'
    webhook = DiscordWebhook(url=link)
    embed = DiscordEmbed(title="Rose Sniper 🌹", description=newstr, color=0x0f0380)
    webhook.add_embed(embed)
    webhook.execute()
  def fetchdroptime(self):
    if self.target.lower() == 'test':
      self.droptime = int(time.time() + 10)
      return self.droptime
    c = requests.get(f"http://api.star.shopping/droptime/" + self.target, headers={"User-Agent": "Sniper"}).json()['unix']
    self.droptime = c
    return c
  def finalsleep(self):
    while True:
      if time.time() >= self.droptime - (self.delay/1000):
        break
    return None
  def waitbeforedrop(self):
    time.sleep(self.droptime - time.time() - 2.5)
  def genncpayload(self, bearer):
    return bytes(("\r\n".join((f"PUT /minecraft/profile/name/{self.target} HTTP/1.1", "Host: api.minecraftservices.com", "Content-Type: application/json", f"Authorization: Bearer {bearer}","\r\n"))), "utf-8")
  def gcpayload(self, bearer):
    return bytes('\r\n'.join(['POST /minecraft/profile HTTP/1.1', 'Host: api.minecraftservices.com', 'Accept: application/json', 'Content-Type: application/json', f'Authorization: Bearer {bearer}',
    f'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    f'Content-Length: {len(target) + 19}',
    '', f'{{"profileName": "{target}"}}']).encode('utf-8'))
  def auth(self):
    bearers = list()
    af = open("accounts.txt")
    ar = af.read().splitlines()
    for account in ar:
      if len(account) > 300:
        bearers.append(account)
      else:
        split = account.split(":")
        try:
          c = msmcauth.login(split[0], split[1]).access_token
          if data["type"] == "gc":
            bearers.append(c)
          else:
            bakatw = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers={"Authorization": "Bearer " + c}).json()['nameChangeAllowed']
            if bakatw == True:
              bearers.append(c)
            else:
              print(f"[ROSE] {split[0]} can not name change!")
        except Exception as e:
          print(f"[ROSE] Failed to auth as {split[0]} | Error: {e}")
    return bearers
class socketsniper():
    def __init__(self, payload):
        self.socky = None
        self.payload = payload
        self.status = None
        self.data = None
    def create(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockc = ssl.create_default_context()
        sock = sockc.wrap_socket(sock, server_hostname="api.minecraftservices.com")
        sock.connect(("api.minecraftservices.com", 443))
        self.socky = sock
    def senddata(self):
        self.socky.send(self.payload)
    def recv(self):
        data = self.socky.recv(2048).decode("utf-8")
        self.status = data[9:12]
        self.data = data
timesm = []
def processinfo(sockywocky):
  sockywocky.recv()
  received = time.time()
  timesm.append(f"[{sockywocky.status}] @ {datetime.fromtimestamp(received)}")
  print(f"[{sockywocky.status}] @ {datetime.fromtimestamp(received)}")
target = input("Enter Target > ")
offset = float(input("Enter offset > "))
if data["type"] == 'nc':
  util = utility(target, offset, "nc")
else:
  util = utility(target, offset, "gc")
#getting the needed stuff for sniping :)
droptime = util.fetchdroptime()
tokens = util.auth()
util.waitbeforedrop()
### waiting 2 seconds before drop before creating socket connections that 
## have a higher chance of not being blocked
if data["type"] == 'nc':
  socks = []
  for item in tokens:
    for x in range(3):
      payload = util.genncpayload(item)
      creese = socketsniper(payload)
      creese.create()#no return needed so no variable :)
      threading.Thread(target=processinfo, args=(creese,)).start()
      socks.append(creese)
else:
  socks = []
  for item in tokens:
    for x in range(2):
      payload = util.gcpayload(item)
      creese = socketsniper(payload)
      creese.create()#no return needed so no variable :)
      threading.Thread(target=processinfo, args=(creese,)).start()
      socks.append(creese)
util.finalsleep()
print(f"[ROSE] Sending @ {datetime.now()} | Droptime was: {datetime.fromtimestamp(droptime)}")
for t in socks:
  t.senddata()
time.sleep(3)
util.webhooktimes(timesm)